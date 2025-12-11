# Sentiment-Based Dynamic Backgrounds

**Phase 4.5** - Mood-reactive visual system for AI Council debates

Generate dynamic backgrounds that respond to debate sentiment, intensity, and emotional tone in real-time. Creates immersive visual experiences that enhance viewer engagement and reflect the mood of the discussion.

---

## 🎯 Overview

The Dynamic Backgrounds system consists of three main components:

1. **Sentiment Analyzer** - Analyzes debate content to determine mood
2. **Background Generator** - Creates visuals based on mood state
3. **Background Compositor** - Blends backgrounds with video content

Together, these create a reactive visual experience that:
- Adapts to debate intensity and controversy
- Reflects emotional tone through color and motion
- Provides smooth transitions between mood states
- Supports multiple visual styles
- Integrates seamlessly with video pipeline

---

## 📊 Features

### Sentiment Analysis
- ✅ Real-time mood detection (8 distinct moods)
- ✅ Intensity tracking (calm to intense)
- ✅ Controversy measurement
- ✅ Consensus level calculation
- ✅ Emotional arc tracking
- ✅ Smooth mood transitions

### Visual Styles
- ✅ **Gradient** - Animated color gradients with pulsing
- ✅ **Particles** - Physics-based particle systems
- ✅ **Geometric** - Rotating geometric patterns
- ✅ **Waves** - Flowing wave animations
- ✅ **Nebula** - Cloud/smoke effects
- ✅ **Matrix** - Digital rain effect
- ✅ **Neural** - Network node visualization

### Composition Features
- ✅ Multi-layer compositing
- ✅ Blending modes (normal, multiply, screen, overlay, etc.)
- ✅ Smooth cross-fade transitions
- ✅ Mood-based effects (vignette, glow, chromatic aberration)
- ✅ Picture-in-picture support
- ✅ Split-screen layouts
- ✅ Layer management and ordering

---

## 🎭 Debate Moods

The system recognizes 8 distinct debate moods:

| Mood | Description | Visual Characteristics |
|------|-------------|----------------------|
| **Calm Agreement** | Low intensity, high consensus | Cool blues and greens, slow gentle animations |
| **Thoughtful Analysis** | Moderate intensity, analytical | Purples and grays, steady controlled movement |
| **Heated Debate** | High intensity, moderate controversy | Warm reds and oranges, rapid energetic motion |
| **Consensus Building** | Moderate intensity, growing consensus | Teal and gold, converging patterns |
| **Consensus Reached** | High consensus achieved | Victory greens and gold, celebratory effects |
| **Intense Disagreement** | Extreme controversy and intensity | Deep reds, chaotic erratic movement |
| **Curious Exploration** | Moderate energy, exploratory | Blues and purples, flowing discovery patterns |
| **Passionate Advocacy** | High energy, strong conviction | Oranges, bold dynamic animations |

---

## 🚀 Quick Start

### Basic Usage

```python
from streaming.backgrounds import (
    SentimentAnalyzer,
    BackgroundGenerator,
    BackgroundCompositor,
    BackgroundConfig,
    CompositorConfig,
    BackgroundStyle
)

# Initialize components
analyzer = SentimentAnalyzer()
bg_config = BackgroundConfig(
    style=BackgroundStyle.PARTICLES,
    width=1920,
    height=1080,
    fps=30
)
generator = BackgroundGenerator(bg_config)

compositor_config = CompositorConfig(
    width=1920,
    height=1080,
    background_opacity=0.75
)
compositor = BackgroundCompositor(compositor_config)

# During debate
analyzer.add_reading(
    speaker="Agent1",
    text="This is a critical issue that requires immediate attention!",
    confidence=0.9
)

# Get current mood
mood = analyzer.get_current_mood()
print(f"Current mood: {mood.mood.value}")

# Generate background frame
bg_frame = generator.generate_frame(mood)

# Set background with transition
compositor.set_background(bg_frame, transition=True)

# Composite with video
video_frame = {"type": "video", "source": "debate_stream"}
composite = compositor.composite_frame(video_frame)
```

### Running the Demo

```bash
cd workspace/projects/ai-council-system
python examples/backgrounds_demo.py
```

The demo showcases:
- Sentiment analysis with mood progression
- All 7 background visual styles
- Mood transitions
- Multi-layer composition
- Advanced effects
- All 8 mood states

---

## 📖 API Reference

### SentimentAnalyzer

Analyzes debate content to determine visual mood.

```python
analyzer = SentimentAnalyzer(
    smoothing_window=5,           # Number of readings to smooth over
    mood_transition_threshold=0.3, # Minimum change for mood switch
    intensity_sensitivity=1.0      # Intensity multiplier
)
```

#### Methods

**add_reading(speaker, text, confidence, emotion=None, sentiment_override=None)**

Add a new sentiment reading from debate content.

```python
reading = analyzer.add_reading(
    speaker="Pragmatist",
    text="I think we should carefully consider all perspectives.",
    confidence=0.75
)
```

**get_current_mood() → MoodState**

Calculate and return current debate mood.

```python
mood = analyzer.get_current_mood()
print(f"Mood: {mood.mood.value}")
print(f"Intensity: {mood.intensity}")
print(f"Controversy: {mood.controversy_level}")
```

**get_mood_arc(duration_seconds) → List[MoodState]**

Get emotional arc over time.

```python
arc = analyzer.get_mood_arc(duration_seconds=60)
```

### BackgroundGenerator

Generates mood-reactive background visuals.

```python
config = BackgroundConfig(
    style=BackgroundStyle.PARTICLES,
    width=1920,
    height=1080,
    fps=30,
    particle_count=100,
    animation_speed=1.0
)
generator = BackgroundGenerator(config)
```

#### Methods

**generate_frame(mood_state) → Dict**

Generate a single frame based on current mood.

```python
frame = generator.generate_frame(mood_state)
```

Returns a dictionary describing the frame with rendering parameters.

### BackgroundCompositor

Composites backgrounds with video content.

```python
config = CompositorConfig(
    width=1920,
    height=1080,
    fps=30,
    background_opacity=0.8,
    enable_transitions=True,
    transition_duration=2.0
)
compositor = BackgroundCompositor(config)
```

#### Methods

**set_background(background_frame, transition=True)**

Set new background with optional smooth transition.

```python
compositor.set_background(bg_frame, transition=True)
```

**composite_frame(video_frame=None) → Dict**

Composite complete frame with all layers.

```python
composite = compositor.composite_frame(video_frame)
```

**apply_mood_vignette(mood_state) → Layer**

Add mood-based vignette effect.

```python
vignette = compositor.apply_mood_vignette(mood)
```

**apply_glow_effect(mood_state, color) → Layer**

Add glow effect based on energy level.

```python
glow = compositor.apply_glow_effect(mood, color="#3498db")
```

**apply_chromatic_aberration(mood_state) → Layer**

Add chromatic aberration based on controversy.

```python
aberration = compositor.apply_chromatic_aberration(mood)
```

**create_picture_in_picture(main_content, pip_content, position, size) → List[Layer]**

Create picture-in-picture layout.

```python
layers = compositor.create_picture_in_picture(
    main_content=main_video,
    pip_content=pip_video,
    position=(1550, 50),
    size=(320, 180)
)
```

**create_split_screen(left_content, right_content, split_position) → List[Layer]**

Create split-screen layout.

```python
layers = compositor.create_split_screen(
    left_content=left_video,
    right_content=right_video,
    split_position=0.5  # 50/50 split
)
```

---

## 🎨 Color Palettes

Each mood has a predefined color palette optimized for visual impact:

```python
from streaming.backgrounds import MOOD_PALETTES, DebateMood

palette = MOOD_PALETTES[DebateMood.HEATED_DEBATE]
print(palette.primary)    # "#e74c3c" (hot red)
print(palette.secondary)  # "#f39c12" (orange)
print(palette.accent)     # "#c0392b" (dark red)
```

Palettes include:
- **primary** - Main background color
- **secondary** - Secondary/gradient color
- **accent** - Accent/highlight color
- **particles** - Particle system color
- **glow** - Glow/halo color

---

## 🔧 Integration Example

### With Debate System

```python
from core.council import DebateSessionManager
from streaming.backgrounds import SentimentAnalyzer, BackgroundGenerator

# Initialize
debate_manager = DebateSessionManager(...)
sentiment_analyzer = SentimentAnalyzer()
bg_generator = BackgroundGenerator(bg_config)

# During debate round
for response in debate_round.responses:
    # Analyze sentiment
    sentiment_analyzer.add_reading(
        speaker=response.agent.name,
        text=response.content,
        confidence=response.confidence
    )

    # Update background
    mood = sentiment_analyzer.get_current_mood()
    bg_frame = bg_generator.generate_frame(mood)

    # Use in video rendering
    render_frame_with_background(bg_frame, response)
```

### With Video Pipeline

```python
from streaming.video import VideoGenerator
from streaming.backgrounds import BackgroundCompositor

# Initialize
video_gen = VideoGenerator(...)
compositor = BackgroundCompositor(compositor_config)

# During streaming
while streaming:
    # Get background from generator
    bg_frame = bg_generator.generate_frame(current_mood)
    compositor.set_background(bg_frame)

    # Get video frame
    video_frame = video_gen.generate_frame()

    # Composite
    final_frame = compositor.composite_frame(video_frame)

    # Stream to platform
    stream_to_youtube(final_frame)
```

---

## 🎬 Visual Styles in Detail

### Gradient
Smooth animated color gradients with pulsing based on energy level.

**Best for**: Calm discussions, smooth transitions
**Parameters**: angle (rotating), colors, pulse intensity

### Particles
Physics-based particle systems that react to mood.

**Best for**: Energetic debates, dynamic visuals
**Behavior**:
- High intensity → faster particle movement
- High controversy → erratic random motion
- High consensus → particles converge to center

### Geometric
Rotating geometric patterns (hexagons, polygons).

**Best for**: Analytical discussions, structured debates
**Parameters**: shape count (varies with intensity), rotation speed

### Waves
Flowing wave animations with frequency and amplitude variation.

**Best for**: Flowing discussions, natural transitions
**Parameters**: wave count, amplitude (energy), frequency (controversy)

### Nebula
Cloud/smoke-like effects with swirling turbulence.

**Best for**: Abstract concepts, philosophical debates
**Parameters**: swirl intensity, turbulence, time evolution

### Matrix
Digital "Matrix-style" falling code/characters.

**Best for**: Technical debates, cyberpunk aesthetic
**Parameters**: column count, falling speed, character set

### Neural
Network node visualization with connections.

**Best for**: Showing consensus, network thinking
**Parameters**: node count, connection density, pulse activity

---

## 📈 Performance Considerations

### Optimization Tips

1. **Particle Count**: Reduce for lower-end hardware
   ```python
   config = BackgroundConfig(
       style=BackgroundStyle.PARTICLES,
       particle_count=50  # Reduced from default 100
   )
   ```

2. **Frame Rate**: Match video output FPS
   ```python
   config = BackgroundConfig(fps=30)  # or 60 for smoother
   ```

3. **Transition Duration**: Balance smoothness vs responsiveness
   ```python
   compositor_config = CompositorConfig(
       transition_duration=1.0  # Faster transitions
   )
   ```

4. **Layer Count**: Minimize unnecessary layers
   ```python
   # Clear unused layers
   compositor.clear_layers(LayerType.OVERLAY)
   ```

### Performance Stats

```python
# Generator stats
stats = generator.get_statistics()
print(f"Frames generated: {stats['frames_generated']}")

# Compositor stats
stats = compositor.get_statistics()
print(f"Frames composited: {stats['frames_composited']}")
print(f"Layer count: {stats['layer_count']}")
```

---

## 🔮 Future Enhancements

Potential additions for future versions:

- **3D Backgrounds**: WebGL-based 3D environments
- **AI-Generated Art**: Real-time AI art generation
- **Audio Reactivity**: Respond to audio frequency/amplitude
- **User Themes**: Custom color palette creation
- **Preset Library**: Pre-made background templates
- **Performance Modes**: Quality presets (low/medium/high/ultra)
- **Recording Optimization**: Specialized settings for recording vs live
- **Multi-Monitor**: Different backgrounds per screen

---

## 🐛 Troubleshooting

### Background not updating
- Ensure you're calling `generate_frame()` each frame
- Check that `mood_state` is being updated from analyzer

### Transitions too fast/slow
- Adjust `CompositorConfig.transition_duration`
- Modify `mood.transition_speed` for dynamic control

### Colors don't match mood
- Verify mood detection with `analyzer.get_current_mood()`
- Check palette mapping in `MOOD_PALETTES`

### Performance issues
- Reduce particle count
- Lower FPS
- Simplify visual style (gradient is lightest)
- Clear unnecessary layers

---

## 📊 Statistics & Analytics

Track background system performance:

```python
# Sentiment analyzer
stats = analyzer.get_statistics()
print(f"Total readings: {stats['total_readings']}")
print(f"Average sentiment: {stats['avg_sentiment']}")
print(f"Mood changes: {stats['mood_changes']}")

# Background generator
stats = generator.get_statistics()
print(f"Frames generated: {stats['frames_generated']}")
print(f"Current palette: {stats['current_palette']}")

# Compositor
stats = compositor.get_statistics()
print(f"Frames composited: {stats['frames_composited']}")
print(f"Layer count: {stats['layer_count']}")
print(f"Transition active: {stats['transition_active']}")
```

---

## 📝 Examples

### Example 1: Simple Background

```python
from streaming.backgrounds import *

# Minimal setup
analyzer = SentimentAnalyzer()
generator = BackgroundGenerator(BackgroundConfig(
    style=BackgroundStyle.GRADIENT,
    width=1920,
    height=1080
))

# Add some readings
analyzer.add_reading("Agent1", "Let's discuss this carefully.", 0.7)
analyzer.add_reading("Agent2", "I strongly agree!", 0.9)

# Generate
mood = analyzer.get_current_mood()
frame = generator.generate_frame(mood)
```

### Example 2: Advanced Composition

```python
from streaming.backgrounds import *

# Full setup
compositor = BackgroundCompositor(CompositorConfig(
    width=1920,
    height=1080,
    background_opacity=0.75,
    enable_transitions=True
))

# Set background
bg_frame = generator.generate_frame(mood)
compositor.set_background(bg_frame)

# Add effects
compositor.apply_mood_vignette(mood)
compositor.apply_glow_effect(mood, color="#3498db")

# Add video
video = {"type": "video", "source": "debate"}
composite = compositor.composite_frame(video)
```

### Example 3: Real-time Updates

```python
import time

while debate_active:
    # Update every frame
    mood = analyzer.get_current_mood()
    bg_frame = generator.generate_frame(mood)
    compositor.set_background(bg_frame, transition=True)

    # Update transition
    compositor.update_transition(delta_time=1/30)  # 30 FPS

    # Composite
    final = compositor.composite_frame(video_frame)

    # Render
    render_to_output(final)

    time.sleep(1/30)
```

---

## ✅ Testing

Run the comprehensive demo to verify all features:

```bash
python examples/backgrounds_demo.py
```

Tests include:
- ✅ Sentiment analysis with 5 debate turns
- ✅ All 7 visual styles
- ✅ Mood transitions
- ✅ Multi-layer composition
- ✅ Advanced effects (vignette, glow, aberration)
- ✅ PiP and split-screen layouts
- ✅ All 8 mood states

---

## 📚 Architecture

```
streaming/backgrounds/
├── sentiment.py          # Sentiment analysis and mood detection
├── generator.py          # Background visual generation
├── compositor.py         # Multi-layer composition
├── __init__.py          # Package exports
└── README.md            # This file

examples/
└── backgrounds_demo.py  # Comprehensive demonstration
```

**Key Classes**:
- `SentimentAnalyzer` - Analyzes debate sentiment → mood
- `BackgroundGenerator` - Generates visuals from mood
- `BackgroundCompositor` - Composites layers into final frame

**Data Flow**:
```
Debate Text → SentimentAnalyzer → MoodState → BackgroundGenerator → Frame
                                                      ↓
                                              BackgroundCompositor → Composite Frame
                                                      ↑
                                                 Video Content
```

---

## 🎓 Best Practices

1. **Smoothing**: Use appropriate `smoothing_window` for your use case
   - Shorter (3-5) for responsive changes
   - Longer (7-10) for smoother, stable moods

2. **Transitions**: Enable for better UX
   ```python
   CompositorConfig(enable_transitions=True, transition_duration=2.0)
   ```

3. **Style Selection**: Match style to content
   - Analytical debates → Geometric, Neural
   - Emotional debates → Particles, Nebula
   - Formal debates → Gradient, Waves

4. **Performance**: Monitor and optimize
   - Check `get_statistics()` regularly
   - Adjust quality based on hardware
   - Clear unused layers

5. **Testing**: Use the demo to validate
   ```bash
   python examples/backgrounds_demo.py
   ```

---

## 🤝 Integration Points

Works seamlessly with:

- ✅ **Phase 1-3**: Core debate system
- ✅ **Phase 4.1**: Avatar system (avatars over backgrounds)
- ✅ **Phase 4.2**: Video effects (combine with transitions)
- ✅ **Phase 4.3**: Viewer voting (show voting mood)
- ✅ Streaming pipeline (real-time generation)
- ✅ Video rendering (composited output)

---

**Phase 4.5 Complete** ✅

Sentiment-based dynamic backgrounds provide immersive, mood-reactive visuals that enhance viewer engagement and create a professional broadcast experience.

**Next**: Phase 4.4 (Multi-Language Support) or Phase 4.6 (Voice Cloning)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
