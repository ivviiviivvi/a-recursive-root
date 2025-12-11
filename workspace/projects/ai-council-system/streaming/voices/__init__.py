"""
Voice Cloning & Consistency System

Provides consistent, personality-matched voices for AI agents using
advanced TTS engines with voice cloning capabilities.

Author: AI Council System
Phase: 4.6 - Voice Cloning for Agent Consistency
Version: 1.0.0
"""

# Voice Profiles
from .profiles import (
    VoiceGender,
    VoiceAge,
    VoiceAccent,
    VoiceCharacteristics,
    VoiceProfile,
    VoiceProfileManager,
    DEFAULT_VOICE_PROFILES
)

# Voice Synthesis
from .synthesizer import (
    TTSEngine,
    SynthesisResult,
    VoiceSynthesizer,
    ElevenLabsSynthesizer,
    EdgeTTSSynthesizer,
    Pyttsx3Synthesizer,
    GTTSSynthesizer,
    MockSynthesizer,
    VoiceSynthesisManager
)

# Voice Cache
from .cache import (
    CacheEntry,
    VoiceCache
)

__all__ = [
    # Profiles
    "VoiceGender",
    "VoiceAge",
    "VoiceAccent",
    "VoiceCharacteristics",
    "VoiceProfile",
    "VoiceProfileManager",
    "DEFAULT_VOICE_PROFILES",

    # Synthesis
    "TTSEngine",
    "SynthesisResult",
    "VoiceSynthesizer",
    "ElevenLabsSynthesizer",
    "EdgeTTSSynthesizer",
    "Pyttsx3Synthesizer",
    "GTTSSynthesizer",
    "MockSynthesizer",
    "VoiceSynthesisManager",

    # Cache
    "CacheEntry",
    "VoiceCache",
]

__version__ = "1.0.0"
