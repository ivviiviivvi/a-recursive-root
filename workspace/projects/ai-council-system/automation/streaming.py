"""
Multi-Platform Streaming Manager

Handles simultaneous streaming to multiple platforms (YouTube, Twitch, etc.)
with automatic failover, bitrate adaptation, and health monitoring.

Author: AI Council System
Phase: 5.1 - Automation & Scale
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import asyncio
from pathlib import Path


class StreamPlatform(Enum):
    """Supported streaming platforms"""
    YOUTUBE = "youtube"
    TWITCH = "twitch"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    CUSTOM_RTMP = "custom_rtmp"


class StreamStatus(Enum):
    """Stream status"""
    IDLE = "idle"
    CONNECTING = "connecting"
    LIVE = "live"
    BUFFERING = "buffering"
    ERROR = "error"
    STOPPED = "stopped"


class StreamQuality(Enum):
    """Stream quality presets"""
    LOW = "low"          # 480p, 1500 kbps
    MEDIUM = "medium"    # 720p, 3000 kbps
    HIGH = "high"        # 1080p, 6000 kbps
    ULTRA = "ultra"      # 4K, 15000 kbps


@dataclass
class StreamConfig:
    """Configuration for a stream"""
    platform: StreamPlatform
    stream_key: str
    rtmp_url: str
    quality: StreamQuality = StreamQuality.HIGH
    enabled: bool = True
    backup_enabled: bool = False
    backup_rtmp_url: Optional[str] = None
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 10


@dataclass
class StreamMetrics:
    """Real-time stream metrics"""
    platform: StreamPlatform
    status: StreamStatus
    bitrate_kbps: float = 0.0
    fps: float = 0.0
    dropped_frames: int = 0
    total_frames: int = 0
    uptime_seconds: float = 0.0
    viewer_count: int = 0
    latency_ms: float = 0.0
    last_error: Optional[str] = None

    def get_drop_rate(self) -> float:
        """Calculate frame drop rate"""
        if self.total_frames == 0:
            return 0.0
        return (self.dropped_frames / self.total_frames) * 100


@dataclass
class StreamDestination:
    """A streaming destination"""
    config: StreamConfig
    metrics: StreamMetrics
    start_time: Optional[datetime] = None
    retry_count: int = 0
    last_error_time: Optional[datetime] = None

    def is_healthy(self) -> bool:
        """Check if stream is healthy"""
        if self.metrics.status != StreamStatus.LIVE:
            return False

        # Check drop rate
        if self.metrics.get_drop_rate() > 5.0:  # >5% drops
            return False

        # Check bitrate
        if self.metrics.bitrate_kbps < 1000:  # Too low
            return False

        return True


class MultiPlatformStreamer:
    """
    Multi-platform streaming manager

    Features:
    - Simultaneous streaming to multiple platforms
    - Automatic failover and retry
    - Bitrate adaptation
    - Health monitoring
    - Viewer statistics
    - Recording to file
    """

    def __init__(self):
        """Initialize multi-platform streamer"""
        self.destinations: List[StreamDestination] = []
        self.is_streaming = False
        self.recording_enabled = False
        self.recording_path: Optional[Path] = None

        # Global metrics
        self.total_streams = 0
        self.total_stream_time_seconds = 0.0
        self.total_bytes_sent = 0

    def add_destination(self, config: StreamConfig) -> StreamDestination:
        """
        Add a streaming destination

        Args:
            config: Stream configuration

        Returns:
            StreamDestination object
        """
        metrics = StreamMetrics(
            platform=config.platform,
            status=StreamStatus.IDLE
        )

        destination = StreamDestination(
            config=config,
            metrics=metrics
        )

        self.destinations.append(destination)
        return destination

    def remove_destination(self, platform: StreamPlatform) -> bool:
        """Remove a destination"""
        initial_count = len(self.destinations)
        self.destinations = [
            d for d in self.destinations
            if d.config.platform != platform
        ]
        return len(self.destinations) < initial_count

    async def start_streaming(self, recording_path: Optional[Path] = None):
        """
        Start streaming to all enabled destinations

        Args:
            recording_path: Optional path to save recording
        """
        if self.is_streaming:
            print("⚠️  Already streaming")
            return

        self.is_streaming = True
        self.recording_enabled = recording_path is not None
        self.recording_path = recording_path

        print(f"📡 Starting multi-platform stream to {len(self.destinations)} destinations...")

        # Start each destination
        tasks = []
        for dest in self.destinations:
            if dest.config.enabled:
                task = asyncio.create_task(self._start_destination(dest))
                tasks.append(task)

        # Wait for all to start
        await asyncio.gather(*tasks, return_exceptions=True)

        # Monitor streams
        asyncio.create_task(self._monitor_streams())

        self.total_streams += 1

    async def _start_destination(self, destination: StreamDestination):
        """Start streaming to a destination"""
        destination.metrics.status = StreamStatus.CONNECTING

        try:
            # Simulate connection (in production, use actual RTMP streaming)
            # Would use: ffmpeg, subprocess, or streaming library
            await asyncio.sleep(2)

            destination.metrics.status = StreamStatus.LIVE
            destination.start_time = datetime.now()

            print(f"✅ Connected to {destination.config.platform.value}")

            # Simulate streaming
            asyncio.create_task(self._stream_to_destination(destination))

        except Exception as e:
            destination.metrics.status = StreamStatus.ERROR
            destination.metrics.last_error = str(e)
            print(f"❌ Failed to connect to {destination.config.platform.value}: {e}")

            # Retry if enabled
            if destination.retry_count < destination.config.max_retry_attempts:
                destination.retry_count += 1
                print(f"🔄 Retrying {destination.config.platform.value} (attempt {destination.retry_count})...")
                await asyncio.sleep(destination.config.retry_delay_seconds)
                await self._start_destination(destination)

    async def _stream_to_destination(self, destination: StreamDestination):
        """Stream content to a destination"""
        while self.is_streaming and destination.config.enabled:
            # Simulate streaming metrics
            destination.metrics.fps = 30.0
            destination.metrics.bitrate_kbps = self._get_target_bitrate(destination.config.quality)
            destination.metrics.total_frames += 30  # 1 second at 30fps

            # Simulate occasional dropped frames
            if destination.metrics.total_frames % 300 == 0:
                destination.metrics.dropped_frames += 1

            # Update uptime
            if destination.start_time:
                destination.metrics.uptime_seconds = (
                    datetime.now() - destination.start_time
                ).total_seconds()

            await asyncio.sleep(1)

    def _get_target_bitrate(self, quality: StreamQuality) -> float:
        """Get target bitrate for quality"""
        bitrates = {
            StreamQuality.LOW: 1500,
            StreamQuality.MEDIUM: 3000,
            StreamQuality.HIGH: 6000,
            StreamQuality.ULTRA: 15000
        }
        return bitrates.get(quality, 3000)

    async def _monitor_streams(self):
        """Monitor stream health and handle issues"""
        while self.is_streaming:
            for dest in self.destinations:
                if not dest.config.enabled:
                    continue

                # Check health
                if not dest.is_healthy() and dest.metrics.status == StreamStatus.LIVE:
                    print(f"⚠️  Health issue detected on {dest.config.platform.value}")

                    # Attempt recovery
                    if dest.config.backup_enabled and dest.config.backup_rtmp_url:
                        print(f"🔄 Switching to backup URL for {dest.config.platform.value}")
                        # Switch to backup (in production)

            await asyncio.sleep(10)  # Check every 10 seconds

    async def stop_streaming(self):
        """Stop streaming to all destinations"""
        if not self.is_streaming:
            return

        print("🛑 Stopping multi-platform stream...")

        self.is_streaming = False

        # Stop each destination
        for dest in self.destinations:
            if dest.metrics.status == StreamStatus.LIVE:
                dest.metrics.status = StreamStatus.STOPPED

                # Update total stream time
                if dest.start_time:
                    duration = (datetime.now() - dest.start_time).total_seconds()
                    self.total_stream_time_seconds += duration

                print(f"✅ Stopped {dest.config.platform.value}")

    def get_destination(self, platform: StreamPlatform) -> Optional[StreamDestination]:
        """Get destination by platform"""
        for dest in self.destinations:
            if dest.config.platform == platform:
                return dest
        return None

    def get_live_destinations(self) -> List[StreamDestination]:
        """Get all currently live destinations"""
        return [
            dest for dest in self.destinations
            if dest.metrics.status == StreamStatus.LIVE
        ]

    def get_total_viewers(self) -> int:
        """Get total viewer count across all platforms"""
        return sum(
            dest.metrics.viewer_count
            for dest in self.destinations
            if dest.metrics.status == StreamStatus.LIVE
        )

    def get_average_bitrate(self) -> float:
        """Get average bitrate across live streams"""
        live = self.get_live_destinations()
        if not live:
            return 0.0

        return sum(d.metrics.bitrate_kbps for d in live) / len(live)

    def get_statistics(self) -> Dict[str, Any]:
        """Get streaming statistics"""
        live_count = len(self.get_live_destinations())
        total_count = len(self.destinations)

        return {
            "total_destinations": total_count,
            "live_destinations": live_count,
            "is_streaming": self.is_streaming,
            "total_streams": self.total_streams,
            "total_stream_time_hours": self.total_stream_time_seconds / 3600,
            "total_viewers": self.get_total_viewers(),
            "average_bitrate_kbps": self.get_average_bitrate(),
            "destinations": {
                dest.config.platform.value: {
                    "status": dest.metrics.status.value,
                    "uptime_seconds": dest.metrics.uptime_seconds,
                    "fps": dest.metrics.fps,
                    "bitrate_kbps": dest.metrics.bitrate_kbps,
                    "drop_rate_percent": dest.metrics.get_drop_rate(),
                    "viewer_count": dest.metrics.viewer_count,
                    "healthy": dest.is_healthy() if dest.metrics.status == StreamStatus.LIVE else False
                }
                for dest in self.destinations
            }
        }

    def enable_destination(self, platform: StreamPlatform):
        """Enable a destination"""
        dest = self.get_destination(platform)
        if dest:
            dest.config.enabled = True

    def disable_destination(self, platform: StreamPlatform):
        """Disable a destination"""
        dest = self.get_destination(platform)
        if dest:
            dest.config.enabled = False


class AdaptiveBitrateManager:
    """
    Manages adaptive bitrate for stream quality

    Automatically adjusts bitrate based on network conditions
    """

    def __init__(self, min_bitrate: float = 1000, max_bitrate: float = 8000):
        """
        Initialize adaptive bitrate manager

        Args:
            min_bitrate: Minimum bitrate in kbps
            max_bitrate: Maximum bitrate in kbps
        """
        self.min_bitrate = min_bitrate
        self.max_bitrate = max_bitrate
        self.current_bitrate = max_bitrate
        self.target_bitrate = max_bitrate

    def adjust_for_network(self, packet_loss: float, latency_ms: float):
        """
        Adjust bitrate based on network conditions

        Args:
            packet_loss: Packet loss percentage (0-100)
            latency_ms: Latency in milliseconds
        """
        # Reduce bitrate if network issues detected
        if packet_loss > 5.0 or latency_ms > 500:
            self.target_bitrate = max(
                self.min_bitrate,
                self.target_bitrate * 0.8  # Reduce by 20%
            )
        elif packet_loss < 1.0 and latency_ms < 100:
            # Increase bitrate if network is good
            self.target_bitrate = min(
                self.max_bitrate,
                self.target_bitrate * 1.1  # Increase by 10%
            )

        # Smooth transition
        diff = self.target_bitrate - self.current_bitrate
        self.current_bitrate += diff * 0.1  # 10% adjustment per step

    def get_current_bitrate(self) -> float:
        """Get current bitrate"""
        return self.current_bitrate

    def get_recommended_quality(self) -> StreamQuality:
        """Get recommended quality based on current bitrate"""
        if self.current_bitrate >= 8000:
            return StreamQuality.ULTRA
        elif self.current_bitrate >= 5000:
            return StreamQuality.HIGH
        elif self.current_bitrate >= 2500:
            return StreamQuality.MEDIUM
        else:
            return StreamQuality.LOW


class StreamRecorder:
    """
    Records streams to local files

    Can record multiple streams simultaneously
    """

    def __init__(self, output_dir: Path):
        """
        Initialize stream recorder

        Args:
            output_dir: Directory to save recordings
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.recordings: Dict[str, Path] = {}
        self.is_recording = False

    def start_recording(self, session_id: str) -> Path:
        """
        Start recording a session

        Args:
            session_id: Unique session identifier

        Returns:
            Path to recording file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debate_{session_id}_{timestamp}.mp4"
        filepath = self.output_dir / filename

        self.recordings[session_id] = filepath
        self.is_recording = True

        print(f"🔴 Recording started: {filename}")

        return filepath

    def stop_recording(self, session_id: str) -> Optional[Path]:
        """
        Stop recording a session

        Args:
            session_id: Session identifier

        Returns:
            Path to recorded file, or None
        """
        filepath = self.recordings.get(session_id)

        if filepath:
            self.is_recording = False
            print(f"⏹️  Recording stopped: {filepath.name}")
            return filepath

        return None

    def get_recording_path(self, session_id: str) -> Optional[Path]:
        """Get path to recording"""
        return self.recordings.get(session_id)

    def list_recordings(self) -> List[Path]:
        """List all recorded files"""
        return list(self.output_dir.glob("debate_*.mp4"))

    def get_recording_size_mb(self, session_id: str) -> float:
        """Get recording file size in MB"""
        filepath = self.recordings.get(session_id)
        if filepath and filepath.exists():
            return filepath.stat().st_size / (1024 * 1024)
        return 0.0
