#!/usr/bin/env python3
"""
Voice Cloning & Consistency Demo

Demonstrates the voice cloning system that provides unique, consistent voices
for each AI agent personality using advanced TTS engines.

Author: AI Council System
Phase: 4.6 - Voice Cloning for Agent Consistency
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streaming.voices import (
    VoiceProfileManager,
    VoiceSynthesisManager,
    VoiceCache,
    TTSEngine,
    DEFAULT_VOICE_PROFILES
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


async def demo_voice_profiles():
    """Demonstrate voice profile management"""
    print_section("1. Voice Profile Management")

    profile_manager = VoiceProfileManager()

    print("📋 Available Voice Profiles:\n")

    # Show all personalities
    personalities = profile_manager.list_profiles()
    print(f"Total Personalities: {len(personalities)}\n")

    # Show sample profiles
    sample_personalities = [
        "The Pragmatist",
        "The Idealist",
        "The Skeptic",
        "The Innovator",
        "The Philosopher"
    ]

    for personality in sample_personalities:
        profile = profile_manager.get_profile(personality)
        if profile:
            print(f"🎭 {personality}:")
            print(f"   Gender: {profile.gender.value.title()}")
            print(f"   Age: {profile.age.value.title()}")
            print(f"   Accent: {profile.accent.value.title()}")
            print(f"   Pitch: {profile.characteristics.pitch:.2f}x")
            print(f"   Speed: {profile.characteristics.speed:.2f}x")
            print(f"   Energy: {profile.characteristics.energy:.2f}")
            print(f"   Description: {profile.description}")
            if profile.elevenlabs_voice_id:
                print(f"   ElevenLabs ID: {profile.elevenlabs_voice_id[:20]}...")
            print()

    # Show statistics
    stats = profile_manager.get_statistics()
    print("📊 Profile Statistics:")
    print(f"   Total Profiles: {stats['total_profiles']}")
    print(f"   By Gender:")
    for gender, count in stats['by_gender'].items():
        print(f"      {gender.title()}: {count}")
    print(f"   With ElevenLabs: {stats['with_elevenlabs']}")
    print()


async def demo_tts_engines():
    """Demonstrate TTS engine availability"""
    print_section("2. TTS Engine Availability")

    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.MOCK  # Use mock for demo
    )

    print("🔧 Checking Available TTS Engines:\n")

    all_engines = [
        TTSEngine.ELEVENLABS,
        TTSEngine.EDGE_TTS,
        TTSEngine.PYTTSX3,
        TTSEngine.GTTS,
        TTSEngine.MOCK
    ]

    for engine in all_engines:
        synthesizer = synthesis_manager.synthesizers.get(engine)
        if synthesizer:
            available = synthesizer.is_available()
            status = "✅ Available" if available else "❌ Not Available"
            print(f"   {engine.value.upper():<15} {status}")

            if not available and engine != TTSEngine.MOCK:
                if engine == TTSEngine.ELEVENLABS:
                    print(f"      → Install: pip install elevenlabs")
                    print(f"      → Set: ELEVEN_API_KEY environment variable")
                elif engine == TTSEngine.EDGE_TTS:
                    print(f"      → Install: pip install edge-tts")
                elif engine == TTSEngine.PYTTSX3:
                    print(f"      → Install: pip install pyttsx3")
                elif engine == TTSEngine.GTTS:
                    print(f"      → Install: pip install gtts")

    print()


async def demo_voice_synthesis():
    """Demonstrate voice synthesis"""
    print_section("3. Voice Synthesis")

    profile_manager = VoiceProfileManager()
    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.MOCK
    )

    # Create output directory
    output_dir = Path("voice_output")
    output_dir.mkdir(exist_ok=True)

    print("🎤 Synthesizing Sample Speeches:\n")

    # Sample texts for different personalities
    samples = [
        ("The Pragmatist", "I believe we need to carefully analyze the facts before making a decision."),
        ("The Idealist", "This is our chance to make a real difference in the world!"),
        ("The Skeptic", "I'm not convinced this approach will work. We need more evidence."),
        ("The Innovator", "What if we completely reimagine how we approach this problem?"),
        ("The Philosopher", "Consider the deeper implications of this choice on our values."),
    ]

    for personality, text in samples:
        profile = profile_manager.get_profile(personality)
        if not profile:
            continue

        output_path = output_dir / f"{personality.replace(' ', '_').lower()}.mp3"

        print(f"🎭 {personality}:")
        print(f'   "{text}"')

        result = await synthesis_manager.synthesize(
            text=text,
            voice_profile=profile,
            output_path=output_path
        )

        if result.success:
            print(f"   ✅ Success! Audio saved to: {output_path.name}")
            print(f"   Engine: {result.engine_used.value}")
            if result.duration_seconds:
                print(f"   Duration: {result.duration_seconds:.1f}s")
        else:
            print(f"   ❌ Failed: {result.error}")

        print()

    print(f"💾 Audio files saved to: {output_dir}/")
    print()


async def demo_voice_cache():
    """Demonstrate voice caching"""
    print_section("4. Voice Cache System")

    cache_dir = Path("voice_cache")
    cache = VoiceCache(
        cache_dir=cache_dir,
        max_size_mb=100,
        max_age_days=30
    )

    profile_manager = VoiceProfileManager()
    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.MOCK
    )

    print("💾 Testing Voice Cache:\n")

    # Synthesize and cache
    profile = profile_manager.get_profile("The Pragmatist")
    text = "This is a test of the voice caching system."

    output_path = Path("voice_output/cache_test.mp3")
    output_path.parent.mkdir(exist_ok=True)

    # First synthesis
    print("🔄 First synthesis (not cached):")
    has_cache = cache.has(text, profile)
    print(f"   Cached: {has_cache}")

    result = await synthesis_manager.synthesize(text, profile, output_path)

    if result.success:
        # Add to cache
        cached = cache.put(text, profile, output_path)
        print(f"   Synthesized: ✅")
        print(f"   Cached: {'✅' if cached else '❌'}")
        print()

    # Second request (should be cached)
    print("🔄 Second request (should be cached):")
    cached_path = cache.get(text, profile)

    if cached_path:
        print(f"   Cache HIT! ✅")
        print(f"   Cached file: {cached_path.name}")
    else:
        print(f"   Cache MISS ❌")

    print()

    # Show cache statistics
    stats = cache.get_statistics()
    print("📊 Cache Statistics:")
    print(f"   Total Entries: {stats['total_entries']}")
    print(f"   Cache Size: {stats['cache_size_mb']:.2f} MB")
    print(f"   Cache Usage: {stats['cache_size_percent']:.1f}%")
    if stats.get('by_personality'):
        print(f"   By Personality:")
        for personality, count in stats['by_personality'].items():
            print(f"      {personality}: {count}")
    print()


async def demo_fallback_chain():
    """Demonstrate TTS engine fallback"""
    print_section("5. TTS Engine Fallback Chain")

    print("🔄 Testing Automatic Fallback:\n")

    # Create synthesis manager with fallback chain
    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.ELEVENLABS,  # Unlikely to be available
        fallback_chain=[
            TTSEngine.ELEVENLABS,
            TTSEngine.EDGE_TTS,
            TTSEngine.PYTTSX3,
            TTSEngine.GTTS,
            TTSEngine.MOCK  # Always available
        ]
    )

    profile_manager = VoiceProfileManager()
    profile = profile_manager.get_profile("The Idealist")

    text = "Testing the fallback system with unavailable engines."
    output_path = Path("voice_output/fallback_test.mp3")

    print("Attempting synthesis with fallback chain:")
    print("   1. ElevenLabs (likely unavailable)")
    print("   2. Edge TTS")
    print("   3. pyttsx3")
    print("   4. gTTS")
    print("   5. Mock (always works)")
    print()

    result = await synthesis_manager.synthesize(
        text=text,
        voice_profile=profile,
        output_path=output_path,
        try_fallback=True
    )

    if result.success:
        print(f"✅ Synthesis succeeded!")
        print(f"   Engine used: {result.engine_used.value.upper()}")
        print(f"   Output: {output_path.name}")
    else:
        print(f"❌ All engines failed!")
        print(f"   Error: {result.error}")

    print()

    # Show engine usage statistics
    stats = synthesis_manager.get_statistics()
    print("📊 Synthesis Statistics:")
    print(f"   Total Syntheses: {stats['total_syntheses']}")
    print(f"   Preferred Engine: {stats['preferred_engine'].upper()}")
    print(f"   Available Engines: {', '.join(e.upper() for e in stats['available_engines'])}")
    if stats['engine_usage']:
        print(f"   Engine Usage:")
        for engine, count in stats['engine_usage'].items():
            print(f"      {engine.upper()}: {count}")
    print()


async def demo_all_personalities():
    """Demonstrate voices for all personalities"""
    print_section("6. All Personality Voices")

    profile_manager = VoiceProfileManager()
    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.MOCK
    )

    print("🎭 Generating Voices for All Personalities:\n")

    output_dir = Path("voice_output/all_personalities")
    output_dir.mkdir(parents=True, exist_ok=True)

    personalities = profile_manager.list_profiles()
    success_count = 0

    for personality in personalities:
        profile = profile_manager.get_profile(personality)
        if not profile:
            continue

        # Create personality-appropriate text
        text = f"Hello, I am {personality}. {profile.description}"

        output_path = output_dir / f"{personality.replace(' ', '_').replace('The_', '').lower()}.mp3"

        result = await synthesis_manager.synthesize(
            text=text,
            voice_profile=profile,
            output_path=output_path
        )

        status = "✅" if result.success else "❌"
        print(f"   {status} {personality:<25} ({profile.gender.value}, {profile.age.value})")

        if result.success:
            success_count += 1

    print()
    print(f"✅ Successfully generated {success_count}/{len(personalities)} voices")
    print(f"💾 Saved to: {output_dir}/")
    print()


async def demo_characteristic_variations():
    """Demonstrate voice characteristic variations"""
    print_section("7. Voice Characteristic Variations")

    profile_manager = VoiceProfileManager()
    synthesis_manager = VoiceSynthesisManager(
        preferred_engine=TTSEngine.MOCK
    )

    print("🎛️  Testing Voice Characteristic Variations:\n")

    # Get base profile
    base_profile = profile_manager.get_profile("The Pragmatist")
    text = "This is a test of voice characteristic variations."

    variations = [
        ("Normal", 1.0, 1.0, 1.0),
        ("High Pitch", 1.3, 1.0, 1.0),
        ("Fast Speed", 1.0, 1.5, 1.0),
        ("High Energy", 1.0, 1.0, 1.5),
        ("Low Pitch", 0.7, 1.0, 1.0),
        ("Slow Speed", 1.0, 0.7, 1.0),
    ]

    output_dir = Path("voice_output/variations")
    output_dir.mkdir(parents=True, exist_ok=True)

    for var_name, pitch, speed, energy in variations:
        # Update characteristics
        modified_profile = profile_manager.get_profile("The Pragmatist")
        modified_profile.characteristics.pitch = pitch
        modified_profile.characteristics.speed = speed
        modified_profile.characteristics.energy = energy

        output_path = output_dir / f"variation_{var_name.replace(' ', '_').lower()}.mp3"

        result = await synthesis_manager.synthesize(
            text=text,
            voice_profile=modified_profile,
            output_path=output_path
        )

        print(f"   {var_name:<15} Pitch:{pitch:.1f}x Speed:{speed:.1f}x Energy:{energy:.1f}x")
        print(f"      → {output_path.name} {'✅' if result.success else '❌'}")

    print()
    print(f"💾 Variations saved to: {output_dir}/")
    print()


async def main():
    """Run all demos"""
    print()
    print_separator("=")
    print("  🎤 VOICE CLONING & CONSISTENCY DEMO")
    print("  Unique Voices for AI Agent Personalities")
    print_separator("=")
    print()

    print("This demo showcases the voice cloning system that provides")
    print("consistent, personality-matched voices for each AI agent using")
    print("advanced TTS engines with fallback support.")
    print()

    input("Press Enter to start demo...")

    try:
        # Run demos
        await demo_voice_profiles()
        await demo_tts_engines()
        await demo_voice_synthesis()
        await demo_voice_cache()
        await demo_fallback_chain()
        await demo_all_personalities()
        await demo_characteristic_variations()

        # Final summary
        print_section("Demo Complete!")

        print("✅ Successfully demonstrated:")
        print("   • Voice profile management (15 personalities)")
        print("   • TTS engine integration (5 engines)")
        print("   • Voice synthesis with fallback")
        print("   • Voice caching for consistency")
        print("   • Automatic fallback chain")
        print("   • All personality voices")
        print("   • Voice characteristic variations")
        print()

        print("🎬 The voice system is ready for integration with:")
        print("   • Live debate streaming")
        print("   • Video generation pipeline")
        print("   • Multi-agent conversations")
        print("   • Real-time synthesis")
        print()

        print("📁 Generated Files:")
        print("   • voice_output/ - Sample audio files")
        print("   • voice_cache/ - Cached audio for consistency")
        print()

        print_separator("=")
        print("  Phase 4.6: Voice Cloning for Agent Consistency ✅ COMPLETE")
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
    asyncio.run(main())
