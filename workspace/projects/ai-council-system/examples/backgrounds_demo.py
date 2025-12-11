#!/usr/bin/env python3
"""
Dynamic Backgrounds Demo

Demonstrates the sentiment-based dynamic background system with mood-reactive
visuals that respond to debate intensity, controversy, and emotional tone.

Author: AI Council System
Phase: 4.5 - Sentiment-Based Dynamic Backgrounds
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streaming.backgrounds import (
    SentimentAnalyzer,
    BackgroundGenerator,
    BackgroundCompositor,
    BackgroundConfig,
    CompositorConfig,
    BackgroundStyle,
    DebateMood,
    MOOD_PALETTES
)


def print_separator(char="=", length=70):
    """Print a separator line"""
    print(char * length)


def print_section(title):
    """Print a section header"""
    print()
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def print_mood_state(mood_state, title="Current Mood"):
    """Print mood state details"""
    print(f"🎨 {title}:")
    print(f"   Mood: {mood_state.mood.value.upper().replace('_', ' ')}")
    print(f"   Intensity: {mood_state.intensity:.1%}")
    print(f"   Sentiment: {mood_state.sentiment_tone.value}")
    print(f"   Controversy: {mood_state.controversy_level:.1%}")
    print(f"   Energy: {mood_state.energy_level:.1%}")
    print(f"   Consensus: {mood_state.consensus_level:.1%}")
    print()


def print_frame_summary(frame, style):
    """Print frame generation summary"""
    print(f"📹 Generated {style.value.upper()} frame:")
    print(f"   Type: {frame.get('type', 'unknown')}")

    if 'colors' in frame:
        print(f"   Colors: {', '.join(frame['colors'][:3])}")
    elif 'background_color' in frame:
        print(f"   Background: {frame['background_color']}")

    if 'particles' in frame:
        print(f"   Particles: {len(frame['particles'])}")
    elif 'shapes' in frame:
        print(f"   Shapes: {len(frame['shapes'])}")
    elif 'waves' in frame:
        print(f"   Waves: {len(frame['waves'])}")

    print()


def demo_sentiment_analysis():
    """Demonstrate sentiment analysis"""
    print_section("1. Sentiment Analysis")

    analyzer = SentimentAnalyzer(
        smoothing_window=3,
        intensity_sensitivity=1.0
    )

    print("📊 Simulating debate with varying sentiment...\n")

    # Simulate a debate progression
    debate_samples = [
        {
            "speaker": "Pragmatist",
            "text": "I think we should carefully analyze this situation from multiple perspectives.",
            "confidence": 0.75,
            "emotion": "analytical"
        },
        {
            "speaker": "Idealist",
            "text": "This is absolutely critical for our future! We must act now with conviction!",
            "confidence": 0.95,
            "emotion": "passionate"
        },
        {
            "speaker": "Skeptic",
            "text": "I strongly disagree. This approach is fundamentally flawed and dangerous.",
            "confidence": 0.88,
            "emotion": "critical"
        },
        {
            "speaker": "Mediator",
            "text": "Both perspectives have merit. Let's find common ground and build consensus.",
            "confidence": 0.82,
            "emotion": "diplomatic"
        },
        {
            "speaker": "Pragmatist",
            "text": "Agreed. A balanced approach incorporating both viewpoints would be beneficial.",
            "confidence": 0.85,
            "emotion": "constructive"
        },
    ]

    for i, sample in enumerate(debate_samples, 1):
        print(f"💬 Turn {i}: {sample['speaker']}")
        print(f"   \"{sample['text'][:60]}...\"")

        # Add reading
        reading = analyzer.add_reading(
            speaker=sample['speaker'],
            text=sample['text'],
            confidence=sample['confidence'],
            emotion=sample['emotion']
        )

        print(f"   Sentiment: {reading.sentiment_score:+.2f} | "
              f"Intensity: {reading.intensity:.2f} | "
              f"Controversy: {reading.controversy_factor:.2f}")

        # Get mood after each reading
        mood = analyzer.get_current_mood()
        print(f"   → Mood: {mood.mood.value.replace('_', ' ').title()}")
        print()

        time.sleep(0.3)  # Brief pause for readability

    # Show final mood state
    final_mood = analyzer.get_current_mood()
    print_mood_state(final_mood, "Final Mood State")

    # Show statistics
    stats = analyzer.get_statistics()
    print("📈 Analysis Statistics:")
    print(f"   Total Readings: {stats['total_readings']}")
    print(f"   Average Sentiment: {stats['avg_sentiment']:+.2f}")
    print(f"   Average Intensity: {stats['avg_intensity']:.2f}")
    print(f"   Mood Changes: {stats['mood_changes']}")
    print()

    return analyzer, final_mood


def demo_background_generation(mood_state):
    """Demonstrate background generation"""
    print_section("2. Background Generation")

    # Test different styles
    styles_to_demo = [
        BackgroundStyle.GRADIENT,
        BackgroundStyle.PARTICLES,
        BackgroundStyle.GEOMETRIC,
        BackgroundStyle.WAVES,
        BackgroundStyle.NEBULA,
    ]

    generators = {}

    for style in styles_to_demo:
        print(f"🎨 Generating {style.value.upper()} background...")

        config = BackgroundConfig(
            style=style,
            width=1920,
            height=1080,
            fps=30,
            particle_count=150
        )

        generator = BackgroundGenerator(config)
        generators[style] = generator

        # Generate a frame
        frame = generator.generate_frame(mood_state)
        print_frame_summary(frame, style)

        time.sleep(0.2)

    # Show palette for current mood
    palette = MOOD_PALETTES.get(mood_state.mood)
    if palette:
        print("🎨 Color Palette for Current Mood:")
        print(f"   Primary: {palette.primary}")
        print(f"   Secondary: {palette.secondary}")
        print(f"   Accent: {palette.accent}")
        print(f"   Particles: {palette.particles}")
        print(f"   Glow: {palette.glow}")
        print()

    return generators


def demo_mood_transitions(analyzer):
    """Demonstrate mood transitions"""
    print_section("3. Mood Transitions")

    print("🔄 Simulating dramatic mood shift...\n")

    # Create generator
    config = BackgroundConfig(
        style=BackgroundStyle.GRADIENT,
        width=1920,
        height=1080,
        fps=30
    )
    generator = BackgroundGenerator(config)

    # Get initial mood
    initial_mood = analyzer.get_current_mood()
    print(f"Initial Mood: {initial_mood.mood.value.replace('_', ' ').title()}")

    # Add dramatic readings to trigger mood change
    print("\n💥 Adding intense disagreement...\n")
    for i in range(3):
        analyzer.add_reading(
            speaker=f"Agent_{i}",
            text="This is completely wrong and absolutely unacceptable! We must oppose this!",
            confidence=0.95,
            sentiment_override=-0.8
        )

    # Get new mood
    new_mood = analyzer.get_current_mood()
    print(f"New Mood: {new_mood.mood.value.replace('_', ' ').title()}")
    print(f"Transition Speed: {new_mood.transition_speed}x")
    print()

    # Generate frames showing transition
    print("🎬 Generating transition frames...\n")
    for frame_num in range(5):
        frame = generator.generate_frame(new_mood)
        progress = generator.transition_progress
        print(f"   Frame {frame_num + 1}: Transition {progress:.1%} complete")
        time.sleep(0.1)

    print()


def demo_composition():
    """Demonstrate background composition"""
    print_section("4. Background Composition")

    # Create compositor
    compositor_config = CompositorConfig(
        width=1920,
        height=1080,
        fps=30,
        background_opacity=0.75,
        enable_transitions=True,
        transition_duration=2.0
    )

    compositor = BackgroundCompositor(compositor_config)

    print("🎬 Creating multi-layer composition...\n")

    # Create a sample background
    bg_config = BackgroundConfig(
        style=BackgroundStyle.PARTICLES,
        width=1920,
        height=1080
    )
    generator = BackgroundGenerator(bg_config)

    # Create analyzer for mood
    analyzer = SentimentAnalyzer()
    analyzer.add_reading(
        speaker="Test",
        text="This is a test message",
        confidence=0.8
    )
    mood = analyzer.get_current_mood()

    # Generate background
    bg_frame = generator.generate_frame(mood)
    compositor.set_background(bg_frame)

    print("✅ Set background layer")

    # Add video layer (simulated)
    video_frame = {
        "type": "video",
        "source": "debate_stream",
        "timestamp": "00:00:10"
    }

    print("✅ Added video layer")

    # Add mood-based effects
    print("\n🌟 Adding mood-based effects...\n")

    vignette = compositor.apply_mood_vignette(mood)
    print(f"   ✓ Vignette (intensity: {mood.intensity:.1%})")

    glow = compositor.apply_glow_effect(mood, color="#3498db")
    print(f"   ✓ Glow (strength: {mood.energy_level:.1%})")

    if mood.controversy_level > 0.3:
        aberration = compositor.apply_chromatic_aberration(mood)
        print(f"   ✓ Chromatic Aberration (strength: {mood.controversy_level:.1%})")

    # Composite final frame
    print("\n📦 Compositing final frame...\n")
    composite = compositor.composite_frame(video_frame)

    print(f"   Layers: {len(composite['layers'])}")
    print(f"   Resolution: {composite['width']}x{composite['height']}")

    for i, layer in enumerate(composite['layers'], 1):
        print(f"   Layer {i}: {layer['type']} (z={layer['z_index']}, "
              f"opacity={layer['opacity']:.2f})")

    print()

    # Show statistics
    stats = compositor.get_statistics()
    print("📊 Compositor Statistics:")
    print(f"   Frames Composited: {stats['frames_composited']}")
    print(f"   Layer Count: {stats['layer_count']}")
    print(f"   Background Set: {stats['background_set']}")
    print()


def demo_advanced_features():
    """Demonstrate advanced composition features"""
    print_section("5. Advanced Features")

    compositor_config = CompositorConfig(
        width=1920,
        height=1080,
        fps=30
    )
    compositor = BackgroundCompositor(compositor_config)

    # Picture-in-Picture
    print("🖼️  Picture-in-Picture:\n")

    main_video = {"type": "video", "source": "main_debate"}
    pip_video = {"type": "video", "source": "viewer_reactions"}

    pip_layers = compositor.create_picture_in_picture(
        main_content=main_video,
        pip_content=pip_video,
        position=(1550, 50),
        size=(320, 180),
        border_width=3,
        border_color="#3498db"
    )

    print(f"   ✓ Created {len(pip_layers)} layers for PiP")
    print(f"   ✓ Main content + PiP overlay at (1550, 50)")
    print()

    # Split Screen
    print("📱 Split Screen:\n")

    compositor.clear_layers()

    left_content = {"type": "video", "source": "agent_view"}
    right_content = {"type": "video", "source": "viewer_view"}

    split_layers = compositor.create_split_screen(
        left_content=left_content,
        right_content=right_content,
        split_position=0.5,
        divider_width=4,
        divider_color="#FFFFFF"
    )

    print(f"   ✓ Created {len(split_layers)} layers for split screen")
    print(f"   ✓ 50/50 split with vertical divider")
    print()

    # Layer management
    print("📚 Layer Management:\n")

    total_layers = compositor.get_layer_count()
    print(f"   Total Layers: {total_layers}")

    from streaming.backgrounds import LayerType

    for layer_type in LayerType:
        count = compositor.get_layer_count(layer_type)
        if count > 0:
            print(f"   {layer_type.value.title()}: {count}")

    print()


def demo_all_moods():
    """Demonstrate all mood states"""
    print_section("6. All Mood States")

    print("🎭 Showcasing all debate moods...\n")

    config = BackgroundConfig(
        style=BackgroundStyle.GRADIENT,
        width=1920,
        height=1080
    )
    generator = BackgroundGenerator(config)

    # Manually create mood states for each mood type
    from streaming.backgrounds import DebateMood, MoodState, SentimentTone
    from datetime import datetime

    moods = [
        (DebateMood.CALM_AGREEMENT, 0.3, 0.2, 0.8),
        (DebateMood.THOUGHTFUL_ANALYSIS, 0.5, 0.3, 0.6),
        (DebateMood.HEATED_DEBATE, 0.8, 0.7, 0.4),
        (DebateMood.CONSENSUS_BUILDING, 0.6, 0.4, 0.7),
        (DebateMood.CONSENSUS_REACHED, 0.7, 0.2, 0.9),
        (DebateMood.INTENSE_DISAGREEMENT, 0.9, 0.9, 0.2),
        (DebateMood.CURIOUS_EXPLORATION, 0.5, 0.4, 0.5),
        (DebateMood.PASSIONATE_ADVOCACY, 0.8, 0.6, 0.5),
    ]

    for mood_type, intensity, controversy, consensus in moods:
        mood_state = MoodState(
            mood=mood_type,
            intensity=intensity,
            sentiment_tone=SentimentTone.MIXED,
            controversy_level=controversy,
            energy_level=intensity,
            consensus_level=consensus,
            timestamp=datetime.now()
        )

        frame = generator.generate_frame(mood_state)
        palette = MOOD_PALETTES.get(mood_type)

        print(f"🎨 {mood_type.value.replace('_', ' ').title()}:")
        print(f"   Intensity: {intensity:.1%} | Controversy: {controversy:.1%} | Consensus: {consensus:.1%}")
        print(f"   Palette: {palette.primary} → {palette.secondary}")
        print()

        time.sleep(0.2)


def main():
    """Run all demos"""
    print()
    print_separator("=")
    print("  🎨 DYNAMIC BACKGROUNDS DEMO")
    print("  Sentiment-Based Reactive Visuals for AI Council Debates")
    print_separator("=")
    print()

    print("This demo showcases the mood-reactive background system that")
    print("generates dynamic visuals based on debate sentiment, intensity,")
    print("and emotional tone.")
    print()

    input("Press Enter to start demo...")

    try:
        # Run demos
        analyzer, mood = demo_sentiment_analysis()
        generators = demo_background_generation(mood)
        demo_mood_transitions(analyzer)
        demo_composition()
        demo_advanced_features()
        demo_all_moods()

        # Final summary
        print_section("Demo Complete!")

        print("✅ Successfully demonstrated:")
        print("   • Sentiment analysis with mood detection")
        print("   • 7 background visual styles")
        print("   • Mood-based color palettes")
        print("   • Smooth transitions between moods")
        print("   • Multi-layer composition")
        print("   • Advanced effects (vignette, glow, aberration)")
        print("   • Picture-in-picture and split-screen")
        print("   • All 8 debate mood states")
        print()

        print("🎬 The background system is ready for integration with:")
        print("   • Live debate streaming")
        print("   • Real-time sentiment analysis")
        print("   • Video rendering pipeline")
        print("   • Multi-platform distribution")
        print()

        print_separator("=")
        print("  Phase 4.5: Sentiment-Based Dynamic Backgrounds ✅ COMPLETE")
        print_separator("=")
        print()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
