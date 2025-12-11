"""
Voice Profile Manager

Manages voice profiles for AI agent personalities, ensuring consistent
voice characteristics across all generated speech.

Author: AI Council System
Phase: 4.6 - Voice Cloning for Agent Consistency
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import json
from pathlib import Path


class VoiceGender(Enum):
    """Voice gender categories"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class VoiceAge(Enum):
    """Voice age categories"""
    YOUNG = "young"        # 20-30
    MIDDLE = "middle"      # 30-50
    MATURE = "mature"      # 50+


class VoiceAccent(Enum):
    """Voice accent/dialect options"""
    AMERICAN = "american"
    BRITISH = "british"
    AUSTRALIAN = "australian"
    NEUTRAL = "neutral"
    INDIAN = "indian"
    CANADIAN = "canadian"


@dataclass
class VoiceCharacteristics:
    """Detailed voice characteristics"""
    pitch: float = 1.0           # 0.5 to 2.0 (1.0 = normal)
    speed: float = 1.0           # 0.5 to 2.0 (1.0 = normal)
    energy: float = 1.0          # 0.5 to 1.5 (enthusiasm level)
    stability: float = 0.5       # 0.0 to 1.0 (voice consistency)
    clarity: float = 0.75        # 0.0 to 1.0 (pronunciation clarity)
    similarity_boost: float = 0.75  # 0.0 to 1.0 (for cloned voices)
    style: float = 0.0           # 0.0 to 1.0 (style exaggeration)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "pitch": self.pitch,
            "speed": self.speed,
            "energy": self.energy,
            "stability": self.stability,
            "clarity": self.clarity,
            "similarity_boost": self.similarity_boost,
            "style": self.style
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'VoiceCharacteristics':
        """Create from dictionary"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class VoiceProfile:
    """
    Complete voice profile for an AI agent personality

    Defines all characteristics needed to generate consistent
    speech for a specific agent across all TTS engines.
    """
    personality_name: str
    voice_id: Optional[str] = None  # External TTS provider voice ID
    gender: VoiceGender = VoiceGender.NEUTRAL
    age: VoiceAge = VoiceAge.MIDDLE
    accent: VoiceAccent = VoiceAccent.NEUTRAL
    characteristics: VoiceCharacteristics = field(default_factory=VoiceCharacteristics)
    description: str = ""
    tags: List[str] = field(default_factory=list)

    # Provider-specific IDs
    elevenlabs_voice_id: Optional[str] = None
    coqui_speaker_id: Optional[str] = None
    azure_voice_name: Optional[str] = None
    google_voice_name: Optional[str] = None

    # Sample audio reference (optional)
    reference_audio_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "personality_name": self.personality_name,
            "voice_id": self.voice_id,
            "gender": self.gender.value,
            "age": self.age.value,
            "accent": self.accent.value,
            "characteristics": self.characteristics.to_dict(),
            "description": self.description,
            "tags": self.tags,
            "elevenlabs_voice_id": self.elevenlabs_voice_id,
            "coqui_speaker_id": self.coqui_speaker_id,
            "azure_voice_name": self.azure_voice_name,
            "google_voice_name": self.google_voice_name,
            "reference_audio_path": self.reference_audio_path
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceProfile':
        """Create from dictionary"""
        # Convert enums
        if "gender" in data and isinstance(data["gender"], str):
            data["gender"] = VoiceGender(data["gender"])
        if "age" in data and isinstance(data["age"], str):
            data["age"] = VoiceAge(data["age"])
        if "accent" in data and isinstance(data["accent"], str):
            data["accent"] = VoiceAccent(data["accent"])

        # Convert characteristics
        if "characteristics" in data and isinstance(data["characteristics"], dict):
            data["characteristics"] = VoiceCharacteristics.from_dict(data["characteristics"])

        return cls(**data)


# Predefined voice profiles for all 15 AI personalities
DEFAULT_VOICE_PROFILES: Dict[str, VoiceProfile] = {
    "The Pragmatist": VoiceProfile(
        personality_name="The Pragmatist",
        gender=VoiceGender.MALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=0.95,
            speed=1.0,
            energy=0.8,
            stability=0.8,
            clarity=0.9
        ),
        description="Measured, professional, calm and analytical",
        tags=["professional", "balanced", "analytical"],
        elevenlabs_voice_id="pNInz6obpgDQGcFmaJgB",  # Adam (balanced)
    ),

    "The Idealist": VoiceProfile(
        personality_name="The Idealist",
        gender=VoiceGender.FEMALE,
        age=VoiceAge.YOUNG,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.1,
            speed=1.05,
            energy=1.3,
            stability=0.7,
            clarity=0.85
        ),
        description="Warm, optimistic, passionate and hopeful",
        tags=["passionate", "optimistic", "warm"],
        elevenlabs_voice_id="EXAVITQu4vr4xnSDxMaL",  # Bella (soft female)
    ),

    "The Skeptic": VoiceProfile(
        personality_name="The Skeptic",
        gender=VoiceGender.MALE,
        age=VoiceAge.MATURE,
        accent=VoiceAccent.BRITISH,
        characteristics=VoiceCharacteristics(
            pitch=0.85,
            speed=0.95,
            energy=0.9,
            stability=0.9,
            clarity=0.95
        ),
        description="Deep, questioning, critical and deliberate",
        tags=["critical", "thoughtful", "precise"],
        elevenlabs_voice_id="TxGEqnHWrfWFTfGW9XjX",  # Josh (deep male)
    ),

    "The Innovator": VoiceProfile(
        personality_name="The Innovator",
        gender=VoiceGender.NEUTRAL,
        age=VoiceAge.YOUNG,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.05,
            speed=1.15,
            energy=1.4,
            stability=0.6,
            clarity=0.8
        ),
        description="Energetic, creative, fast-paced and enthusiastic",
        tags=["energetic", "creative", "dynamic"],
        elevenlabs_voice_id="ErXwobaYiN019PkySvjV",  # Antoni (upbeat)
    ),

    "The Historian": VoiceProfile(
        personality_name="The Historian",
        gender=VoiceGender.MALE,
        age=VoiceAge.MATURE,
        accent=VoiceAccent.BRITISH,
        characteristics=VoiceCharacteristics(
            pitch=0.9,
            speed=0.9,
            energy=0.7,
            stability=0.95,
            clarity=1.0
        ),
        description="Authoritative, measured, educational and wise",
        tags=["authoritative", "educational", "wise"],
        elevenlabs_voice_id="VR6AewLTigWG4xSOukaG",  # Arnold (narrative)
    ),

    "The Ethicist": VoiceProfile(
        personality_name="The Ethicist",
        gender=VoiceGender.FEMALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.NEUTRAL,
        characteristics=VoiceCharacteristics(
            pitch=1.0,
            speed=0.95,
            energy=0.9,
            stability=0.85,
            clarity=0.95
        ),
        description="Clear, principled, thoughtful and composed",
        tags=["principled", "thoughtful", "clear"],
        elevenlabs_voice_id="ThT5KcBeYPX3keUQqHPh",  # Dorothy (calm female)
    ),

    "The Contrarian": VoiceProfile(
        personality_name="The Contrarian",
        gender=VoiceGender.MALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.0,
            speed=1.1,
            energy=1.2,
            stability=0.65,
            clarity=0.85
        ),
        description="Sharp, challenging, provocative and direct",
        tags=["provocative", "sharp", "challenging"],
        elevenlabs_voice_id="yoZ06aMxZJJ28mfd3POQ",  # Sam (assertive)
    ),

    "The Mediator": VoiceProfile(
        personality_name="The Mediator",
        gender=VoiceGender.FEMALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.NEUTRAL,
        characteristics=VoiceCharacteristics(
            pitch=1.05,
            speed=0.95,
            energy=0.8,
            stability=0.9,
            clarity=0.9
        ),
        description="Soothing, diplomatic, balanced and gentle",
        tags=["diplomatic", "soothing", "balanced"],
        elevenlabs_voice_id="jsCqWAovK2LkecY7zXl4",  # Freya (gentle)
    ),

    "The Scientist": VoiceProfile(
        personality_name="The Scientist",
        gender=VoiceGender.NEUTRAL,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.NEUTRAL,
        characteristics=VoiceCharacteristics(
            pitch=0.98,
            speed=1.0,
            energy=0.85,
            stability=0.9,
            clarity=0.95
        ),
        description="Precise, factual, methodical and clear",
        tags=["precise", "factual", "methodical"],
        elevenlabs_voice_id="pqHfZKP75CvOlQylNhV4",  # Bill (neutral clear)
    ),

    "The Futurist": VoiceProfile(
        personality_name="The Futurist",
        gender=VoiceGender.MALE,
        age=VoiceAge.YOUNG,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.1,
            speed=1.15,
            energy=1.3,
            stability=0.7,
            clarity=0.85
        ),
        description="Forward-looking, excited, visionary and dynamic",
        tags=["visionary", "excited", "forward-thinking"],
        elevenlabs_voice_id="N2lVS1w4EtoT3dr4eOWO",  # Callum (enthusiastic)
    ),

    "The Economist": VoiceProfile(
        personality_name="The Economist",
        gender=VoiceGender.FEMALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=0.95,
            speed=1.0,
            energy=0.9,
            stability=0.85,
            clarity=0.95
        ),
        description="Professional, data-driven, confident and articulate",
        tags=["professional", "analytical", "confident"],
        elevenlabs_voice_id="jBpfuIE2acCO8z3wKNLl",  # Gigi (professional)
    ),

    "The Philosopher": VoiceProfile(
        personality_name="The Philosopher",
        gender=VoiceGender.MALE,
        age=VoiceAge.MATURE,
        accent=VoiceAccent.NEUTRAL,
        characteristics=VoiceCharacteristics(
            pitch=0.88,
            speed=0.85,
            energy=0.75,
            stability=0.95,
            clarity=0.95
        ),
        description="Contemplative, deep, reflective and profound",
        tags=["contemplative", "deep", "reflective"],
        elevenlabs_voice_id="ZQe5CZNOzWyzPSCn5a3c",  # Patrick (deep contemplative)
    ),

    "The Activist": VoiceProfile(
        personality_name="The Activist",
        gender=VoiceGender.FEMALE,
        age=VoiceAge.YOUNG,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.15,
            speed=1.1,
            energy=1.4,
            stability=0.65,
            clarity=0.85
        ),
        description="Passionate, urgent, motivated and compelling",
        tags=["passionate", "urgent", "compelling"],
        elevenlabs_voice_id="XB0fDUnXU5powFXDhCwa",  # Charlotte (passionate)
    ),

    "The Traditionalist": VoiceProfile(
        personality_name="The Traditionalist",
        gender=VoiceGender.MALE,
        age=VoiceAge.MATURE,
        accent=VoiceAccent.BRITISH,
        characteristics=VoiceCharacteristics(
            pitch=0.9,
            speed=0.9,
            energy=0.8,
            stability=0.95,
            clarity=0.95
        ),
        description="Dignified, steady, authoritative and formal",
        tags=["dignified", "formal", "authoritative"],
        elevenlabs_voice_id="onwK4e9ZLuTAKqWW03F9",  # Daniel (formal British)
    ),

    "The Populist": VoiceProfile(
        personality_name="The Populist",
        gender=VoiceGender.MALE,
        age=VoiceAge.MIDDLE,
        accent=VoiceAccent.AMERICAN,
        characteristics=VoiceCharacteristics(
            pitch=1.05,
            speed=1.05,
            energy=1.2,
            stability=0.75,
            clarity=0.85
        ),
        description="Relatable, direct, energetic and conversational",
        tags=["relatable", "direct", "conversational"],
        elevenlabs_voice_id="JBFqnCBsd6RMkjVDRZzb",  # George (conversational)
    ),
}


class VoiceProfileManager:
    """
    Manages voice profiles for all AI agent personalities

    Features:
    - Profile creation and management
    - Persistence to disk
    - Profile lookup by personality
    - Characteristic customization
    - Multi-provider support
    """

    def __init__(self, profiles_dir: Optional[Path] = None):
        """
        Initialize voice profile manager

        Args:
            profiles_dir: Directory to store voice profiles (optional)
        """
        self.profiles: Dict[str, VoiceProfile] = {}
        self.profiles_dir = profiles_dir

        # Load default profiles
        self.profiles.update(DEFAULT_VOICE_PROFILES)

        # Load from disk if directory provided
        if self.profiles_dir:
            self.profiles_dir.mkdir(parents=True, exist_ok=True)
            self.load_profiles()

    def get_profile(self, personality_name: str) -> Optional[VoiceProfile]:
        """
        Get voice profile for a personality

        Args:
            personality_name: Name of the personality

        Returns:
            VoiceProfile or None if not found
        """
        return self.profiles.get(personality_name)

    def add_profile(self, profile: VoiceProfile, overwrite: bool = False) -> bool:
        """
        Add a new voice profile

        Args:
            profile: VoiceProfile to add
            overwrite: Whether to overwrite existing profile

        Returns:
            True if added, False if already exists and overwrite=False
        """
        if profile.personality_name in self.profiles and not overwrite:
            return False

        self.profiles[profile.personality_name] = profile

        # Save to disk if configured
        if self.profiles_dir:
            self.save_profile(profile)

        return True

    def remove_profile(self, personality_name: str) -> bool:
        """
        Remove a voice profile

        Args:
            personality_name: Name of personality to remove

        Returns:
            True if removed, False if not found
        """
        if personality_name not in self.profiles:
            return False

        del self.profiles[personality_name]

        # Remove from disk if configured
        if self.profiles_dir:
            profile_path = self.profiles_dir / f"{personality_name}.json"
            if profile_path.exists():
                profile_path.unlink()

        return True

    def list_profiles(self) -> List[str]:
        """
        List all personality names with profiles

        Returns:
            List of personality names
        """
        return list(self.profiles.keys())

    def save_profile(self, profile: VoiceProfile):
        """
        Save a profile to disk

        Args:
            profile: Profile to save
        """
        if not self.profiles_dir:
            return

        profile_path = self.profiles_dir / f"{profile.personality_name}.json"
        with open(profile_path, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)

    def save_all_profiles(self):
        """Save all profiles to disk"""
        if not self.profiles_dir:
            return

        for profile in self.profiles.values():
            self.save_profile(profile)

    def load_profile(self, personality_name: str) -> Optional[VoiceProfile]:
        """
        Load a profile from disk

        Args:
            personality_name: Name of personality

        Returns:
            VoiceProfile or None if not found
        """
        if not self.profiles_dir:
            return None

        profile_path = self.profiles_dir / f"{personality_name}.json"
        if not profile_path.exists():
            return None

        with open(profile_path, 'r') as f:
            data = json.load(f)
            return VoiceProfile.from_dict(data)

    def load_profiles(self):
        """Load all profiles from disk"""
        if not self.profiles_dir:
            return

        for profile_path in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_path, 'r') as f:
                    data = json.load(f)
                    profile = VoiceProfile.from_dict(data)
                    self.profiles[profile.personality_name] = profile
            except Exception as e:
                print(f"Error loading profile {profile_path}: {e}")

    def update_characteristics(
        self,
        personality_name: str,
        **characteristics
    ) -> bool:
        """
        Update voice characteristics for a profile

        Args:
            personality_name: Personality to update
            **characteristics: Characteristic values to update

        Returns:
            True if updated, False if profile not found
        """
        profile = self.get_profile(personality_name)
        if not profile:
            return False

        for key, value in characteristics.items():
            if hasattr(profile.characteristics, key):
                setattr(profile.characteristics, key, value)

        # Save to disk if configured
        if self.profiles_dir:
            self.save_profile(profile)

        return True

    def get_profiles_by_tag(self, tag: str) -> List[VoiceProfile]:
        """
        Get all profiles with a specific tag

        Args:
            tag: Tag to filter by

        Returns:
            List of matching profiles
        """
        return [
            profile for profile in self.profiles.values()
            if tag in profile.tags
        ]

    def get_profiles_by_gender(self, gender: VoiceGender) -> List[VoiceProfile]:
        """
        Get all profiles of a specific gender

        Args:
            gender: Gender to filter by

        Returns:
            List of matching profiles
        """
        return [
            profile for profile in self.profiles.values()
            if profile.gender == gender
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about voice profiles"""
        return {
            "total_profiles": len(self.profiles),
            "by_gender": {
                gender.value: len(self.get_profiles_by_gender(gender))
                for gender in VoiceGender
            },
            "by_age": {
                age.value: len([p for p in self.profiles.values() if p.age == age])
                for age in VoiceAge
            },
            "by_accent": {
                accent.value: len([p for p in self.profiles.values() if p.accent == accent])
                for accent in VoiceAccent
            },
            "with_elevenlabs": len([p for p in self.profiles.values() if p.elevenlabs_voice_id]),
            "with_reference_audio": len([p for p in self.profiles.values() if p.reference_audio_path])
        }
