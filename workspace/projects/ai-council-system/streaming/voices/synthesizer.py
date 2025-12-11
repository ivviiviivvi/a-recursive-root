"""
Voice Synthesis Integration

Integrates multiple TTS engines for consistent voice generation across
AI agent personalities. Supports ElevenLabs, edge-tts, pyttsx3, and gTTS.

Author: AI Council System
Phase: 4.6 - Voice Cloning for Agent Consistency
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import os

from .profiles import VoiceProfile, VoiceCharacteristics


class TTSEngine(Enum):
    """Supported TTS engines"""
    ELEVENLABS = "elevenlabs"
    EDGE_TTS = "edge_tts"
    PYTTSX3 = "pyttsx3"
    GTTS = "gtts"
    COQUI = "coqui"
    MOCK = "mock"  # For testing


@dataclass
class SynthesisResult:
    """Result of speech synthesis"""
    success: bool
    audio_path: Optional[Path] = None
    duration_seconds: Optional[float] = None
    error: Optional[str] = None
    engine_used: Optional[TTSEngine] = None
    cached: bool = False


class VoiceSynthesizer(ABC):
    """
    Abstract base class for voice synthesizers

    All TTS engine integrations must implement this interface
    """

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """
        Synthesize speech from text using voice profile

        Args:
            text: Text to synthesize
            voice_profile: Voice profile with characteristics
            output_path: Where to save audio file

        Returns:
            SynthesisResult with status and file path
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this synthesizer is available (dependencies installed)"""
        pass

    @abstractmethod
    def get_engine_name(self) -> TTSEngine:
        """Get the engine type"""
        pass


class ElevenLabsSynthesizer(VoiceSynthesizer):
    """
    ElevenLabs TTS integration

    High-quality AI voice synthesis with voice cloning support
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ElevenLabs synthesizer

        Args:
            api_key: ElevenLabs API key (or set ELEVEN_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ELEVEN_API_KEY")
        self._available = None

    def is_available(self) -> bool:
        """Check if ElevenLabs API is available"""
        if self._available is not None:
            return self._available

        try:
            import elevenlabs
            self._available = self.api_key is not None
        except ImportError:
            self._available = False

        return self._available

    def get_engine_name(self) -> TTSEngine:
        return TTSEngine.ELEVENLABS

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """Synthesize using ElevenLabs API"""
        if not self.is_available():
            return SynthesisResult(
                success=False,
                error="ElevenLabs not available (missing API key or library)"
            )

        try:
            from elevenlabs import generate, set_api_key, Voice, VoiceSettings

            set_api_key(self.api_key)

            # Use profile's ElevenLabs voice ID or default
            voice_id = voice_profile.elevenlabs_voice_id or voice_profile.voice_id

            if not voice_id:
                return SynthesisResult(
                    success=False,
                    error=f"No ElevenLabs voice ID for {voice_profile.personality_name}"
                )

            # Convert profile characteristics to ElevenLabs settings
            settings = VoiceSettings(
                stability=voice_profile.characteristics.stability,
                similarity_boost=voice_profile.characteristics.similarity_boost,
                style=voice_profile.characteristics.style,
                use_speaker_boost=True
            )

            # Generate audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=settings
                )
            )

            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(audio)

            return SynthesisResult(
                success=True,
                audio_path=output_path,
                engine_used=TTSEngine.ELEVENLABS
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error=f"ElevenLabs synthesis failed: {str(e)}"
            )


class EdgeTTSSynthesizer(VoiceSynthesizer):
    """
    Microsoft Edge TTS integration

    Free, high-quality neural voices
    """

    def __init__(self):
        """Initialize Edge TTS synthesizer"""
        self._available = None

    def is_available(self) -> bool:
        """Check if edge-tts is available"""
        if self._available is not None:
            return self._available

        try:
            import edge_tts
            self._available = True
        except ImportError:
            self._available = False

        return self._available

    def get_engine_name(self) -> TTSEngine:
        return TTSEngine.EDGE_TTS

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """Synthesize using Edge TTS"""
        if not self.is_available():
            return SynthesisResult(
                success=False,
                error="edge-tts not installed (pip install edge-tts)"
            )

        try:
            import edge_tts

            # Map profile to Edge voice
            voice_name = self._get_edge_voice(voice_profile)

            # Calculate rate and pitch from characteristics
            rate = self._calculate_rate(voice_profile.characteristics.speed)
            pitch = self._calculate_pitch(voice_profile.characteristics.pitch)

            # Generate audio
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_name,
                rate=rate,
                pitch=pitch
            )

            output_path.parent.mkdir(parents=True, exist_ok=True)
            await communicate.save(str(output_path))

            return SynthesisResult(
                success=True,
                audio_path=output_path,
                engine_used=TTSEngine.EDGE_TTS
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error=f"Edge TTS synthesis failed: {str(e)}"
            )

    def _get_edge_voice(self, profile: VoiceProfile) -> str:
        """Map voice profile to Edge TTS voice name"""
        # Simple mapping based on gender and accent
        # In production, could be more sophisticated
        voices = {
            ("male", "american"): "en-US-GuyNeural",
            ("male", "british"): "en-GB-RyanNeural",
            ("female", "american"): "en-US-JennyNeural",
            ("female", "british"): "en-GB-SoniaNeural",
            ("neutral", "american"): "en-US-AriaNeural",
        }

        key = (profile.gender.value, profile.accent.value)
        return voices.get(key, "en-US-AriaNeural")

    def _calculate_rate(self, speed: float) -> str:
        """Convert speed multiplier to Edge TTS rate string"""
        # speed: 0.5 to 2.0 → rate: -50% to +100%
        percent = int((speed - 1.0) * 100)
        if percent > 0:
            return f"+{percent}%"
        elif percent < 0:
            return f"{percent}%"
        return "+0%"

    def _calculate_pitch(self, pitch: float) -> str:
        """Convert pitch multiplier to Edge TTS pitch string"""
        # pitch: 0.5 to 2.0 → pitch: -50Hz to +50Hz (approximation)
        hz = int((pitch - 1.0) * 50)
        if hz > 0:
            return f"+{hz}Hz"
        elif hz < 0:
            return f"{hz}Hz"
        return "+0Hz"


class Pyttsx3Synthesizer(VoiceSynthesizer):
    """
    Pyttsx3 TTS integration

    Offline TTS using system voices
    """

    def __init__(self):
        """Initialize pyttsx3 synthesizer"""
        self._available = None
        self._engine = None

    def is_available(self) -> bool:
        """Check if pyttsx3 is available"""
        if self._available is not None:
            return self._available

        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._available = True
        except Exception:
            self._available = False

        return self._available

    def get_engine_name(self) -> TTSEngine:
        return TTSEngine.PYTTSX3

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """Synthesize using pyttsx3"""
        if not self.is_available():
            return SynthesisResult(
                success=False,
                error="pyttsx3 not available"
            )

        try:
            import pyttsx3

            if not self._engine:
                self._engine = pyttsx3.init()

            # Apply voice characteristics
            chars = voice_profile.characteristics

            # Set rate (words per minute)
            base_rate = 150
            self._engine.setProperty('rate', int(base_rate * chars.speed))

            # Set volume (0.0 to 1.0)
            self._engine.setProperty('volume', chars.energy * 0.8)

            # Try to select appropriate voice
            voices = self._engine.getProperty('voices')
            if voices:
                # Simple gender matching
                for voice in voices:
                    if voice_profile.gender.value in voice.name.lower():
                        self._engine.setProperty('voice', voice.id)
                        break

            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self._engine.save_to_file(text, str(output_path))
            self._engine.runAndWait()

            return SynthesisResult(
                success=True,
                audio_path=output_path,
                engine_used=TTSEngine.PYTTSX3
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error=f"pyttsx3 synthesis failed: {str(e)}"
            )


class GTTSSynthesizer(VoiceSynthesizer):
    """
    Google TTS (gTTS) integration

    Simple, free online TTS
    """

    def __init__(self):
        """Initialize gTTS synthesizer"""
        self._available = None

    def is_available(self) -> bool:
        """Check if gTTS is available"""
        if self._available is not None:
            return self._available

        try:
            from gtts import gTTS
            self._available = True
        except ImportError:
            self._available = False

        return self._available

    def get_engine_name(self) -> TTSEngine:
        return TTSEngine.GTTS

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """Synthesize using gTTS"""
        if not self.is_available():
            return SynthesisResult(
                success=False,
                error="gTTS not installed (pip install gtts)"
            )

        try:
            from gtts import gTTS

            # gTTS has limited customization
            # Use slow=True for more deliberate voices
            slow = voice_profile.characteristics.speed < 0.9

            # Map accent to language code
            lang = 'en'  # Default
            if voice_profile.accent.value == 'british':
                tld = 'co.uk'
            elif voice_profile.accent.value == 'australian':
                tld = 'com.au'
            else:
                tld = 'com'

            # Generate
            tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            tts.save(str(output_path))

            return SynthesisResult(
                success=True,
                audio_path=output_path,
                engine_used=TTSEngine.GTTS
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error=f"gTTS synthesis failed: {str(e)}"
            )


class MockSynthesizer(VoiceSynthesizer):
    """
    Mock synthesizer for testing

    Creates empty audio files without actual synthesis
    """

    def is_available(self) -> bool:
        return True

    def get_engine_name(self) -> TTSEngine:
        return TTSEngine.MOCK

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path
    ) -> SynthesisResult:
        """Create mock audio file"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a small dummy file
            with open(output_path, 'wb') as f:
                f.write(b'MOCK_AUDIO_DATA')

            return SynthesisResult(
                success=True,
                audio_path=output_path,
                duration_seconds=len(text.split()) * 0.5,  # Rough estimate
                engine_used=TTSEngine.MOCK
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error=f"Mock synthesis failed: {str(e)}"
            )


class VoiceSynthesisManager:
    """
    Manages voice synthesis with fallback support

    Features:
    - Multiple TTS engine support
    - Automatic fallback chain
    - Voice profile integration
    - Error handling
    """

    def __init__(
        self,
        preferred_engine: TTSEngine = TTSEngine.ELEVENLABS,
        fallback_chain: Optional[list] = None
    ):
        """
        Initialize synthesis manager

        Args:
            preferred_engine: Preferred TTS engine
            fallback_chain: Ordered list of fallback engines
        """
        self.preferred_engine = preferred_engine
        self.fallback_chain = fallback_chain or [
            TTSEngine.ELEVENLABS,
            TTSEngine.EDGE_TTS,
            TTSEngine.PYTTSX3,
            TTSEngine.GTTS,
            TTSEngine.MOCK
        ]

        # Initialize synthesizers
        self.synthesizers: Dict[TTSEngine, VoiceSynthesizer] = {
            TTSEngine.ELEVENLABS: ElevenLabsSynthesizer(),
            TTSEngine.EDGE_TTS: EdgeTTSSynthesizer(),
            TTSEngine.PYTTSX3: Pyttsx3Synthesizer(),
            TTSEngine.GTTS: GTTSSynthesizer(),
            TTSEngine.MOCK: MockSynthesizer()
        }

        # Statistics
        self.synthesis_count = 0
        self.engine_usage: Dict[TTSEngine, int] = {engine: 0 for engine in TTSEngine}

    async def synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path,
        try_fallback: bool = True
    ) -> SynthesisResult:
        """
        Synthesize speech using voice profile

        Args:
            text: Text to synthesize
            voice_profile: Voice profile with characteristics
            output_path: Where to save audio
            try_fallback: Whether to try fallback engines on failure

        Returns:
            SynthesisResult with status
        """
        # Try preferred engine first
        result = await self._try_synthesize(
            text,
            voice_profile,
            output_path,
            self.preferred_engine
        )

        if result.success:
            self.synthesis_count += 1
            return result

        # Try fallback chain if enabled
        if try_fallback:
            for engine in self.fallback_chain:
                if engine == self.preferred_engine:
                    continue  # Already tried

                result = await self._try_synthesize(
                    text,
                    voice_profile,
                    output_path,
                    engine
                )

                if result.success:
                    self.synthesis_count += 1
                    return result

        # All engines failed
        return result

    async def _try_synthesize(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path,
        engine: TTSEngine
    ) -> SynthesisResult:
        """Try synthesis with specific engine"""
        synthesizer = self.synthesizers.get(engine)

        if not synthesizer:
            return SynthesisResult(
                success=False,
                error=f"Synthesizer not found for {engine.value}"
            )

        if not synthesizer.is_available():
            return SynthesisResult(
                success=False,
                error=f"{engine.value} not available"
            )

        result = await synthesizer.synthesize(text, voice_profile, output_path)

        if result.success:
            self.engine_usage[engine] = self.engine_usage.get(engine, 0) + 1

        return result

    def get_available_engines(self) -> list[TTSEngine]:
        """Get list of available TTS engines"""
        return [
            engine for engine, synth in self.synthesizers.items()
            if synth.is_available()
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get synthesis statistics"""
        return {
            "total_syntheses": self.synthesis_count,
            "preferred_engine": self.preferred_engine.value,
            "available_engines": [e.value for e in self.get_available_engines()],
            "engine_usage": {
                engine.value: count
                for engine, count in self.engine_usage.items()
                if count > 0
            }
        }
