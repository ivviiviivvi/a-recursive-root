# Voice Cloning & Consistency System

**Phase 4.6** - Unique, consistent voices for AI agent personalities

Provides advanced voice synthesis with personality matching, ensuring each AI agent has a distinct, consistent voice across all generated speech. Supports multiple TTS engines with intelligent fallback.

---

## 🎯 Overview

The Voice Cloning system consists of three main components:

1. **Voice Profile Manager** - Personality-based voice configuration
2. **Voice Synthesizer** - Multi-engine TTS integration
3. **Voice Cache** - Consistency and performance optimization

Together, these ensure:
- Each AI personality has a unique, recognizable voice
- Consistent voice characteristics across all speech
- Intelligent fallback across multiple TTS engines
- Efficient caching to reduce API costs
- High-quality, natural-sounding speech

---

## 📊 Features

### Voice Profiles (15 Personalities)
- ✅ Predefined profiles for all 15 AI personalities
- ✅ Gender, age, and accent specification
- ✅ Fine-grained voice characteristics (pitch, speed, energy)
- ✅ Multi-provider voice ID mapping
- ✅ Persistent storage and management

### TTS Engine Support
- ✅ **ElevenLabs** - Premium AI voice cloning
- ✅ **Edge TTS** - Free Microsoft neural voices
- ✅ **pyttsx3** - Offline system voices
- ✅ **gTTS** - Google Text-to-Speech
- ✅ **Mock** - Testing without dependencies
- ✅ Automatic fallback chain
- ✅ Extensible architecture

### Voice Caching
- ✅ Hash-based lookup (text + profile)
- ✅ Automatic size management
- ✅ LRU eviction policy
- ✅ Access statistics
- ✅ Persistent cache index
- ✅ Optimization utilities

---

## 🚀 Quick Start

### Basic Usage

```python
from streaming.voices import (
    VoiceProfileManager,
    VoiceSynthesisManager,
    VoiceCache,
    TTSEngine
)
from pathlib import Path

# Initialize components
profile_manager = VoiceProfileManager()
synthesis_manager = VoiceSynthesisManager(
    preferred_engine=TTSEngine.ELEVENLABS
)
cache = VoiceCache(cache_dir=Path("voice_cache"))

# Get voice profile for personality
profile = profile_manager.get_profile("The Pragmatist")

# Synthesize speech
text = "I believe we should analyze this carefully."
output_path = Path("output.mp3")

# Check cache first
cached_audio = cache.get(text, profile)
if cached_audio:
    print(f"Using cached audio: {cached_audio}")
else:
    # Synthesize
    result = await synthesis_manager.synthesize(
        text=text,
        voice_profile=profile,
        output_path=output_path
    )

    if result.success:
        # Add to cache
        cache.put(text, profile, output_path)
        print(f"Synthesized and cached: {output_path}")
```

### Running the Demo

```bash
cd workspace/projects/ai-council-system
python examples/voice_cloning_demo.py
```

The demo showcases:
- Voice profile management
- TTS engine availability check
- Voice synthesis for multiple personalities
- Caching system
- Fallback chain
- All 15 personality voices
- Voice characteristic variations

---

## 📖 API Reference

### VoiceProfileManager

Manages voice profiles for AI agent personalities.

```python
manager = VoiceProfileManager(profiles_dir=Path("profiles"))
```

#### Methods

**get_profile(personality_name) → VoiceProfile**

Get voice profile for a personality.

```python
profile = manager.get_profile("The Idealist")
print(f"Gender: {profile.gender.value}")
print(f"Pitch: {profile.characteristics.pitch}")
```

**add_profile(profile, overwrite=False) → bool**

Add a custom voice profile.

```python
from streaming.voices import VoiceProfile, VoiceGender, VoiceAge

custom_profile = VoiceProfile(
    personality_name="Custom Agent",
    gender=VoiceGender.NEUTRAL,
    age=VoiceAge.YOUNG,
    ...
)
manager.add_profile(custom_profile)
```

**list_profiles() → List[str]**

List all personality names.

```python
personalities = manager.list_profiles()
# ['The Pragmatist', 'The Idealist', ...]
```

**get_statistics() → Dict**

Get profile statistics.

```python
stats = manager.get_statistics()
print(f"Total: {stats['total_profiles']}")
print(f"By gender: {stats['by_gender']}")
```

### VoiceSynthesisManager

Manages voice synthesis with multiple TTS engines.

```python
manager = VoiceSynthesisManager(
    preferred_engine=TTSEngine.ELEVENLABS,
    fallback_chain=[
        TTSEngine.ELEVENLABS,
        TTSEngine.EDGE_TTS,
        TTSEngine.GTTS,
        TTSEngine.MOCK
    ]
)
```

#### Methods

**synthesize(text, voice_profile, output_path, try_fallback=True) → SynthesisResult**

Synthesize speech from text.

```python
result = await manager.synthesize(
    text="Hello world",
    voice_profile=profile,
    output_path=Path("output.mp3"),
    try_fallback=True
)

if result.success:
    print(f"Success! Engine: {result.engine_used.value}")
    print(f"File: {result.audio_path}")
else:
    print(f"Failed: {result.error}")
```

**get_available_engines() → List[TTSEngine]**

Get list of available engines.

```python
engines = manager.get_available_engines()
# [TTSEngine.EDGE_TTS, TTSEngine.MOCK]
```

### VoiceCache

Persistent cache for synthesized audio.

```python
cache = VoiceCache(
    cache_dir=Path("voice_cache"),
    max_size_mb=500,
    max_age_days=30,
    auto_cleanup=True
)
```

#### Methods

**get(text, voice_profile) → Optional[Path]**

Get cached audio for text/profile.

```python
cached = cache.get("Hello", profile)
if cached:
    print(f"Cache hit: {cached}")
```

**put(text, voice_profile, audio_path, duration_seconds=None) → bool**

Add audio to cache.

```python
success = cache.put(
    text="Hello",
    voice_profile=profile,
    audio_path=Path("audio.mp3"),
    duration_seconds=2.5
)
```

**has(text, voice_profile) → bool**

Check if cached.

```python
if cache.has("Hello", profile):
    print("Already cached!")
```

**clear()**

Clear all cache entries.

```python
cache.clear()
```

**get_statistics() → Dict**

Get cache statistics.

```python
stats = cache.get_statistics()
print(f"Entries: {stats['total_entries']}")
print(f"Size: {stats['cache_size_mb']:.2f} MB")
print(f"Usage: {stats['cache_size_percent']:.1f}%")
```

---

## 🎭 Personality Voice Profiles

All 15 AI personalities have predefined voice profiles:

| Personality | Gender | Age | Accent | Pitch | Speed | Description |
|-------------|--------|-----|--------|-------|-------|-------------|
| **The Pragmatist** | Male | Middle | American | 0.95x | 1.0x | Measured, professional, analytical |
| **The Idealist** | Female | Young | American | 1.1x | 1.05x | Warm, optimistic, passionate |
| **The Skeptic** | Male | Mature | British | 0.85x | 0.95x | Deep, questioning, critical |
| **The Innovator** | Neutral | Young | American | 1.05x | 1.15x | Energetic, creative, fast-paced |
| **The Historian** | Male | Mature | British | 0.9x | 0.9x | Authoritative, wise, educational |
| **The Ethicist** | Female | Middle | Neutral | 1.0x | 0.95x | Clear, principled, composed |
| **The Contrarian** | Male | Middle | American | 1.0x | 1.1x | Sharp, challenging, provocative |
| **The Mediator** | Female | Middle | Neutral | 1.05x | 0.95x | Soothing, diplomatic, balanced |
| **The Scientist** | Neutral | Middle | Neutral | 0.98x | 1.0x | Precise, factual, methodical |
| **The Futurist** | Male | Young | American | 1.1x | 1.15x | Visionary, excited, dynamic |
| **The Economist** | Female | Middle | American | 0.95x | 1.0x | Professional, analytical, confident |
| **The Philosopher** | Male | Mature | Neutral | 0.88x | 0.85x | Contemplative, deep, reflective |
| **The Activist** | Female | Young | American | 1.15x | 1.1x | Passionate, urgent, compelling |
| **The Traditionalist** | Male | Mature | British | 0.9x | 0.9x | Dignified, authoritative, formal |
| **The Populist** | Male | Middle | American | 1.05x | 1.05x | Relatable, direct, conversational |

### Voice Characteristics

Each profile includes fine-tuned characteristics:

- **Pitch** (0.5-2.0): Voice pitch multiplier
- **Speed** (0.5-2.0): Speaking rate
- **Energy** (0.5-1.5): Enthusiasm/vigor level
- **Stability** (0.0-1.0): Voice consistency
- **Clarity** (0.0-1.0): Pronunciation clarity
- **Similarity Boost** (0.0-1.0): For cloned voices
- **Style** (0.0-1.0): Style exaggeration

---

## 🔧 TTS Engine Details

### ElevenLabs

**Best for**: High-quality, natural-sounding AI voices

**Setup**:
```bash
pip install elevenlabs
export ELEVEN_API_KEY="your-api-key"
```

**Features**:
- Professional voice cloning
- Emotion and style control
- Multilingual support
- High quality output

**Limitations**:
- Requires API key
- Usage costs
- Rate limits

### Edge TTS

**Best for**: Free, high-quality neural voices

**Setup**:
```bash
pip install edge-tts
```

**Features**:
- Free to use
- Microsoft neural voices
- No API key required
- Good quality

**Limitations**:
- Limited customization
- Internet required
- Voice selection limited

### pyttsx3

**Best for**: Offline synthesis

**Setup**:
```bash
pip install pyttsx3
```

**Features**:
- Works offline
- No API required
- Fast synthesis
- System voice access

**Limitations**:
- Lower quality
- Limited voices
- Platform-dependent

### gTTS

**Best for**: Simple, reliable synthesis

**Setup**:
```bash
pip install gtts
```

**Features**:
- Google TTS quality
- Multiple accents
- Easy to use
- Free

**Limitations**:
- Internet required
- Limited customization
- No real-time

---

## 💾 Voice Caching

The caching system ensures consistency and reduces costs:

### How It Works

1. **Hash Generation**: Text + voice profile → unique hash
2. **Cache Lookup**: Check if hash exists in cache
3. **Synthesis**: Generate if not cached
4. **Storage**: Save to cache with metadata
5. **Retrieval**: Return cached file on future requests

### Cache Management

```python
# Initialize cache
cache = VoiceCache(
    cache_dir=Path("voice_cache"),
    max_size_mb=500,       # Max 500 MB
    max_age_days=30,       # Keep for 30 days
    auto_cleanup=True      # Auto remove old entries
)

# Manual cleanup
cache.cleanup_old_entries()  # Remove entries older than max_age
cache.cleanup_by_size()      # Remove LRU entries to fit size limit
cache.optimize()             # Remove unused entries

# Clear specific entry
cache.remove(text, profile)

# Clear all
cache.clear()
```

### Cache Statistics

```python
stats = cache.get_statistics()

# {
#     'total_entries': 127,
#     'cache_size_mb': 45.3,
#     'cache_size_percent': 9.1,
#     'by_personality': {
#         'The Pragmatist': 15,
#         'The Idealist': 12,
#         ...
#     },
#     'total_accesses': 340,
#     'avg_accesses_per_entry': 2.7
# }
```

---

## 🔄 Fallback Chain

The synthesis manager automatically tries engines in order:

```python
manager = VoiceSynthesisManager(
    preferred_engine=TTSEngine.ELEVENLABS,
    fallback_chain=[
        TTSEngine.ELEVENLABS,    # Try first (best quality)
        TTSEngine.EDGE_TTS,      # Try second (good quality, free)
        TTSEngine.PYTTSX3,       # Try third (offline)
        TTSEngine.GTTS,          # Try fourth (reliable)
        TTSEngine.MOCK           # Always works (testing)
    ]
)

# Synthesis automatically tries fallback on failure
result = await manager.synthesize(text, profile, output_path)

# Result includes which engine succeeded
print(f"Used engine: {result.engine_used.value}")
```

**Fallback Behavior**:
- Tries preferred engine first
- On failure, tries next in fallback chain
- Returns first successful result
- Tracks which engine was used
- Updates usage statistics

---

## 🎬 Integration Example

### With Debate System

```python
from core.council import DebateSessionManager
from streaming.voices import (
    VoiceProfileManager,
    VoiceSynthesisManager,
    VoiceCache
)

# Initialize
profile_manager = VoiceProfileManager()
synthesis_manager = VoiceSynthesisManager()
cache = VoiceCache(cache_dir=Path("voice_cache"))

# During debate
debate = DebateSessionManager(...)

for response in debate_round.responses:
    # Get voice profile for agent
    profile = profile_manager.get_profile(response.agent.personality)

    # Check cache
    audio_path = cache.get(response.content, profile)

    if not audio_path:
        # Synthesize
        audio_path = Path(f"audio/{response.agent.name}_{response.round}.mp3")
        result = await synthesis_manager.synthesize(
            text=response.content,
            voice_profile=profile,
            output_path=audio_path
        )

        if result.success:
            cache.put(response.content, profile, audio_path)

    # Use audio in video/stream
    add_audio_to_video(audio_path, response.timestamp)
```

### With Video Pipeline

```python
from streaming.video import VideoGenerator
from streaming.voices import VoiceSynthesisManager

video_gen = VideoGenerator(...)
voice_synth = VoiceSynthesisManager()

# Generate video with voiceover
for scene in scenes:
    # Generate voice
    audio = await voice_synth.synthesize(
        text=scene.narration,
        voice_profile=scene.speaker_profile,
        output_path=Path(f"audio/scene_{scene.id}.mp3")
    )

    # Add to video
    video_gen.add_audio_track(audio.audio_path, scene.timestamp)

# Render final video
video_gen.render(output_path="final.mp4")
```

---

## 📈 Performance Optimization

### Best Practices

1. **Use Caching**: Always enable caching to avoid re-synthesis
   ```python
   cache = VoiceCache(cache_dir=Path("cache"), auto_cleanup=True)
   ```

2. **Batch Synthesis**: Group similar requests
   ```python
   tasks = [
       synthesis_manager.synthesize(text, profile, path)
       for text, profile, path in batch
   ]
   results = await asyncio.gather(*tasks)
   ```

3. **Preload Profiles**: Load frequently used profiles once
   ```python
   # At startup
   common_profiles = {
       name: profile_manager.get_profile(name)
       for name in ["The Pragmatist", "The Idealist", "The Skeptic"]
   }
   ```

4. **Choose Appropriate Engine**: Match engine to use case
   - High quality needed → ElevenLabs
   - Free synthesis → Edge TTS
   - Offline required → pyttsx3
   - Simple/fast → gTTS

### Performance Metrics

```python
# Synthesis manager stats
stats = synthesis_manager.get_statistics()
print(f"Total syntheses: {stats['total_syntheses']}")
print(f"Engine usage: {stats['engine_usage']}")

# Cache stats
cache_stats = cache.get_statistics()
print(f"Cache hit rate: {cache_stats['total_accesses'] / max(1, cache_stats['total_entries']):.1%}")
```

---

## 🔮 Advanced Features

### Custom Voice Profiles

Create custom profiles for new personalities:

```python
from streaming.voices import (
    VoiceProfile,
    VoiceGender,
    VoiceAge,
    VoiceAccent,
    VoiceCharacteristics
)

custom = VoiceProfile(
    personality_name="The Revolutionary",
    gender=VoiceGender.FEMALE,
    age=VoiceAge.YOUNG,
    accent=VoiceAccent.NEUTRAL,
    characteristics=VoiceCharacteristics(
        pitch=1.2,
        speed=1.3,
        energy=1.4,
        stability=0.6,
        clarity=0.85
    ),
    description="Fiery, passionate, revolutionary spirit",
    tags=["passionate", "revolutionary", "energetic"],
    elevenlabs_voice_id="custom-voice-id"
)

profile_manager.add_profile(custom)
```

### Voice Characteristic Tuning

Fine-tune voice characteristics:

```python
# Get profile
profile = profile_manager.get_profile("The Pragmatist")

# Adjust characteristics
profile.characteristics.pitch = 0.9    # Slightly lower
profile.characteristics.speed = 1.1    # Slightly faster
profile.characteristics.energy = 1.2   # More energetic

# Use modified profile
result = await synthesis_manager.synthesize(text, profile, output_path)
```

### Multiple Language Support

```python
# Create profile with different accent for language
spanish_profile = VoiceProfile(
    personality_name="The Idealist (Spanish)",
    ...
    azure_voice_name="es-ES-ElviraNeural"
)

# Use with appropriate TTS engine
result = await synthesis_manager.synthesize(
    text="Hola, ¿cómo estás?",
    voice_profile=spanish_profile,
    output_path=output_path
)
```

---

## 🐛 Troubleshooting

### No audio generated

**Check engine availability**:
```python
available = synthesis_manager.get_available_engines()
print(f"Available engines: {available}")
```

**Solution**: Install missing TTS libraries or enable fallback

### Poor voice quality

**Issue**: Voice doesn't match personality

**Solution**: Adjust voice characteristics or try different engine
```python
profile.characteristics.pitch = 0.9
profile.characteristics.clarity = 1.0
```

### Cache not working

**Issue**: Same text generates new audio every time

**Solution**: Ensure cache directory is writable and auto_cleanup is enabled
```python
cache = VoiceCache(cache_dir=Path("cache"), auto_cleanup=True)
cache.save_index()  # Force save
```

### ElevenLabs API errors

**Issue**: "API key not found" or rate limit errors

**Solution**:
```python
# Set API key
import os
os.environ["ELEVEN_API_KEY"] = "your-key"

# Or use fallback
manager = VoiceSynthesisManager(
    preferred_engine=TTSEngine.EDGE_TTS  # Free alternative
)
```

---

## 📊 Statistics & Monitoring

### Synthesis Statistics

```python
stats = synthesis_manager.get_statistics()

# {
#     'total_syntheses': 342,
#     'preferred_engine': 'elevenlabs',
#     'available_engines': ['elevenlabs', 'edge_tts', 'mock'],
#     'engine_usage': {
#         'elevenlabs': 280,
#         'edge_tts': 52,
#         'mock': 10
#     }
# }
```

### Cache Statistics

```python
stats = cache.get_statistics()

# {
#     'total_entries': 127,
#     'cache_size_mb': 45.3,
#     'cache_size_percent': 9.1,
#     'by_personality': {...},
#     'total_accesses': 340,
#     'avg_accesses_per_entry': 2.7,
#     'oldest_entry': datetime(...),
#     'newest_entry': datetime(...)
# }
```

---

## ✅ Testing

Run the comprehensive demo:

```bash
python examples/voice_cloning_demo.py
```

Tests include:
- ✅ Voice profile management
- ✅ TTS engine availability
- ✅ Voice synthesis for all personalities
- ✅ Caching system
- ✅ Fallback chain
- ✅ Characteristic variations

---

## 📚 Architecture

```
streaming/voices/
├── profiles.py          # Voice profile management
├── synthesizer.py       # TTS engine integrations
├── cache.py            # Voice caching system
├── __init__.py         # Package exports
└── README.md           # This file

examples/
└── voice_cloning_demo.py  # Comprehensive demo
```

**Key Classes**:
- `VoiceProfileManager` - Manages personality voice profiles
- `VoiceSynthesisManager` - Handles TTS with fallback
- `VoiceCache` - Persistent audio caching

**Data Flow**:
```
Text + Personality → VoiceProfile → Synthesizer → Audio File
                                        ↓
                                    Cache System
                                        ↓
                                  Consistent Voice
```

---

## 🤝 Integration Points

Works seamlessly with:

- ✅ **Phase 4.1**: Avatar system (avatar + voice sync)
- ✅ **Phase 4.2**: Video effects (audio + video timing)
- ✅ **Phase 4.3**: Viewer voting (announce results)
- ✅ **Phase 4.5**: Dynamic backgrounds (mood + voice)
- ✅ Streaming pipeline (real-time audio generation)
- ✅ Video rendering (audio tracks)

---

**Phase 4.6 Complete** ✅

Voice cloning provides unique, consistent voices for each AI personality, enhancing agent identity and viewer engagement.

**Phase 4 Progress**: 83% Complete (5/6 sub-phases)

**Remaining**: Phase 4.4 (Multi-Language Support)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
