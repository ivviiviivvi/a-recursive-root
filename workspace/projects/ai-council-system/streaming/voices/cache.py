"""
Voice Cache System

Caches synthesized audio to ensure consistency and reduce API costs.
Maintains a persistent cache of generated voice clips keyed by text and voice profile.

Author: AI Council System
Phase: 4.6 - Voice Cloning for Agent Consistency
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
import hashlib
import json
import shutil

from .profiles import VoiceProfile


@dataclass
class CacheEntry:
    """Cached audio entry"""
    audio_path: Path
    text_hash: str
    profile_hash: str
    personality_name: str
    created_at: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    file_size_bytes: Optional[int] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "audio_path": str(self.audio_path),
            "text_hash": self.text_hash,
            "profile_hash": self.profile_hash,
            "personality_name": self.personality_name,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "duration_seconds": self.duration_seconds,
            "file_size_bytes": self.file_size_bytes
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CacheEntry':
        """Create from dictionary"""
        data = data.copy()
        data["audio_path"] = Path(data["audio_path"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("last_accessed"):
            data["last_accessed"] = datetime.fromisoformat(data["last_accessed"])
        return cls(**data)


class VoiceCache:
    """
    Persistent cache for synthesized voice audio

    Features:
    - Hash-based lookup (text + voice profile)
    - Automatic cache invalidation
    - Size management
    - Access statistics
    - Persistent storage
    """

    def __init__(
        self,
        cache_dir: Path,
        max_size_mb: int = 500,
        max_age_days: int = 30,
        auto_cleanup: bool = True
    ):
        """
        Initialize voice cache

        Args:
            cache_dir: Directory for cache storage
            max_size_mb: Maximum cache size in MB
            max_age_days: Maximum age of cache entries in days
            auto_cleanup: Automatically cleanup old entries
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_age = timedelta(days=max_age_days)
        self.auto_cleanup = auto_cleanup

        # Cache index
        self.index_path = self.cache_dir / "cache_index.json"
        self.entries: Dict[str, CacheEntry] = {}

        # Load existing cache
        self.load_index()

        # Cleanup if enabled
        if self.auto_cleanup:
            self.cleanup_old_entries()

    def _generate_cache_key(self, text: str, voice_profile: VoiceProfile) -> str:
        """
        Generate cache key from text and voice profile

        Args:
            text: Text to synthesize
            voice_profile: Voice profile

        Returns:
            Cache key (hash)
        """
        # Combine text with relevant profile characteristics
        profile_str = (
            f"{voice_profile.personality_name}:"
            f"{voice_profile.gender.value}:"
            f"{voice_profile.age.value}:"
            f"{voice_profile.characteristics.pitch}:"
            f"{voice_profile.characteristics.speed}:"
            f"{voice_profile.characteristics.energy}"
        )

        combined = f"{text}|{profile_str}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _generate_text_hash(self, text: str) -> str:
        """Generate hash for text only"""
        return hashlib.md5(text.encode()).hexdigest()[:16]

    def _generate_profile_hash(self, voice_profile: VoiceProfile) -> str:
        """Generate hash for voice profile"""
        profile_str = (
            f"{voice_profile.personality_name}:"
            f"{voice_profile.characteristics.pitch}:"
            f"{voice_profile.characteristics.speed}"
        )
        return hashlib.md5(profile_str.encode()).hexdigest()[:16]

    def get(
        self,
        text: str,
        voice_profile: VoiceProfile
    ) -> Optional[Path]:
        """
        Get cached audio for text and voice profile

        Args:
            text: Text that was synthesized
            voice_profile: Voice profile used

        Returns:
            Path to cached audio file, or None if not cached
        """
        cache_key = self._generate_cache_key(text, voice_profile)

        entry = self.entries.get(cache_key)
        if not entry:
            return None

        # Verify file still exists
        if not entry.audio_path.exists():
            # Remove stale entry
            del self.entries[cache_key]
            self.save_index()
            return None

        # Update access stats
        entry.access_count += 1
        entry.last_accessed = datetime.now()
        self.save_index()

        return entry.audio_path

    def put(
        self,
        text: str,
        voice_profile: VoiceProfile,
        audio_path: Path,
        duration_seconds: Optional[float] = None
    ) -> bool:
        """
        Add audio to cache

        Args:
            text: Text that was synthesized
            voice_profile: Voice profile used
            audio_path: Path to audio file
            duration_seconds: Duration of audio (optional)

        Returns:
            True if cached successfully
        """
        if not audio_path.exists():
            return False

        cache_key = self._generate_cache_key(text, voice_profile)

        # Generate cache filename
        text_hash = self._generate_text_hash(text)
        profile_hash = self._generate_profile_hash(voice_profile)
        cache_filename = f"{voice_profile.personality_name}_{profile_hash}_{text_hash}.mp3"
        cached_path = self.cache_dir / cache_filename

        # Copy to cache
        try:
            shutil.copy2(audio_path, cached_path)
        except Exception as e:
            print(f"Error caching audio: {e}")
            return False

        # Create entry
        file_size = cached_path.stat().st_size
        entry = CacheEntry(
            audio_path=cached_path,
            text_hash=text_hash,
            profile_hash=profile_hash,
            personality_name=voice_profile.personality_name,
            created_at=datetime.now(),
            access_count=0,
            duration_seconds=duration_seconds,
            file_size_bytes=file_size
        )

        self.entries[cache_key] = entry
        self.save_index()

        # Check if cache needs cleanup
        if self.auto_cleanup and self.get_cache_size() > self.max_size_bytes:
            self.cleanup_by_size()

        return True

    def has(self, text: str, voice_profile: VoiceProfile) -> bool:
        """Check if text/profile combination is cached"""
        cache_key = self._generate_cache_key(text, voice_profile)
        entry = self.entries.get(cache_key)

        if not entry:
            return False

        # Verify file exists
        if not entry.audio_path.exists():
            del self.entries[cache_key]
            self.save_index()
            return False

        return True

    def remove(self, text: str, voice_profile: VoiceProfile) -> bool:
        """Remove entry from cache"""
        cache_key = self._generate_cache_key(text, voice_profile)
        entry = self.entries.get(cache_key)

        if not entry:
            return False

        # Delete file
        try:
            if entry.audio_path.exists():
                entry.audio_path.unlink()
        except Exception as e:
            print(f"Error deleting cache file: {e}")

        # Remove from index
        del self.entries[cache_key]
        self.save_index()

        return True

    def clear(self):
        """Clear all cache entries"""
        # Delete all cached files
        for entry in self.entries.values():
            try:
                if entry.audio_path.exists():
                    entry.audio_path.unlink()
            except Exception as e:
                print(f"Error deleting cache file: {e}")

        # Clear index
        self.entries.clear()
        self.save_index()

    def cleanup_old_entries(self):
        """Remove entries older than max_age"""
        cutoff = datetime.now() - self.max_age
        to_remove = []

        for key, entry in self.entries.items():
            if entry.created_at < cutoff:
                to_remove.append(key)

        for key in to_remove:
            entry = self.entries[key]
            try:
                if entry.audio_path.exists():
                    entry.audio_path.unlink()
            except Exception as e:
                print(f"Error deleting old cache file: {e}")
            del self.entries[key]

        if to_remove:
            self.save_index()
            print(f"Cleaned up {len(to_remove)} old cache entries")

    def cleanup_by_size(self):
        """Remove least recently used entries to fit within max size"""
        current_size = self.get_cache_size()

        if current_size <= self.max_size_bytes:
            return

        # Sort by last accessed (LRU)
        sorted_entries = sorted(
            self.entries.items(),
            key=lambda x: x[1].last_accessed or x[1].created_at
        )

        # Remove entries until we're under the limit
        removed_count = 0
        for key, entry in sorted_entries:
            if current_size <= self.max_size_bytes:
                break

            # Remove entry
            try:
                if entry.audio_path.exists():
                    file_size = entry.audio_path.stat().st_size
                    entry.audio_path.unlink()
                    current_size -= file_size
            except Exception as e:
                print(f"Error deleting cache file: {e}")

            del self.entries[key]
            removed_count += 1

        if removed_count > 0:
            self.save_index()
            print(f"Removed {removed_count} cache entries to fit size limit")

    def get_cache_size(self) -> int:
        """Get total cache size in bytes"""
        total = 0
        for entry in self.entries.values():
            if entry.file_size_bytes:
                total += entry.file_size_bytes
            elif entry.audio_path.exists():
                total += entry.audio_path.stat().st_size
        return total

    def get_entries_by_personality(self, personality_name: str) -> List[CacheEntry]:
        """Get all cache entries for a personality"""
        return [
            entry for entry in self.entries.values()
            if entry.personality_name == personality_name
        ]

    def load_index(self):
        """Load cache index from disk"""
        if not self.index_path.exists():
            return

        try:
            with open(self.index_path, 'r') as f:
                data = json.load(f)
                self.entries = {
                    key: CacheEntry.from_dict(entry_data)
                    for key, entry_data in data.items()
                }
        except Exception as e:
            print(f"Error loading cache index: {e}")
            self.entries = {}

    def save_index(self):
        """Save cache index to disk"""
        try:
            data = {
                key: entry.to_dict()
                for key, entry in self.entries.items()
            }
            with open(self.index_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache index: {e}")

    def get_statistics(self) -> Dict:
        """Get cache statistics"""
        if not self.entries:
            return {
                "total_entries": 0,
                "cache_size_mb": 0.0,
                "cache_size_percent": 0.0
            }

        cache_size = self.get_cache_size()

        # Count by personality
        by_personality = {}
        for entry in self.entries.values():
            by_personality[entry.personality_name] = by_personality.get(entry.personality_name, 0) + 1

        # Total accesses
        total_accesses = sum(entry.access_count for entry in self.entries.values())

        return {
            "total_entries": len(self.entries),
            "cache_size_bytes": cache_size,
            "cache_size_mb": cache_size / (1024 * 1024),
            "cache_size_percent": (cache_size / self.max_size_bytes) * 100,
            "by_personality": by_personality,
            "total_accesses": total_accesses,
            "avg_accesses_per_entry": total_accesses / len(self.entries) if self.entries else 0,
            "oldest_entry": min(
                (entry.created_at for entry in self.entries.values()),
                default=None
            ),
            "newest_entry": max(
                (entry.created_at for entry in self.entries.values()),
                default=None
            )
        }

    def optimize(self):
        """Optimize cache by removing unused entries"""
        # Remove entries with 0 accesses older than 7 days
        cutoff = datetime.now() - timedelta(days=7)
        to_remove = []

        for key, entry in self.entries.items():
            if entry.access_count == 0 and entry.created_at < cutoff:
                to_remove.append(key)

        for key in to_remove:
            entry = self.entries[key]
            try:
                if entry.audio_path.exists():
                    entry.audio_path.unlink()
            except Exception:
                pass
            del self.entries[key]

        if to_remove:
            self.save_index()

        return len(to_remove)
