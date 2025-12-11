"""
Sentiment-Based Dynamic Backgrounds System

Generates and composites mood-reactive backgrounds for debate videos.
Analyzes debate sentiment in real-time and creates visually responsive
backgrounds that reflect the emotional tone and intensity of discussions.

Author: AI Council System
Phase: 4.5 - Sentiment-Based Dynamic Backgrounds
Version: 1.0.0
"""

# Sentiment Analysis
from .sentiment import (
    DebateMood,
    SentimentTone,
    SentimentReading,
    MoodState,
    SentimentAnalyzer
)

# Background Generation
from .generator import (
    BackgroundStyle,
    ColorPalette,
    Particle,
    BackgroundConfig,
    BackgroundGenerator,
    MOOD_PALETTES
)

# Composition
from .compositor import (
    BlendMode,
    LayerType,
    Layer,
    CompositorConfig,
    BackgroundCompositor
)

__all__ = [
    # Sentiment
    "DebateMood",
    "SentimentTone",
    "SentimentReading",
    "MoodState",
    "SentimentAnalyzer",

    # Generator
    "BackgroundStyle",
    "ColorPalette",
    "Particle",
    "BackgroundConfig",
    "BackgroundGenerator",
    "MOOD_PALETTES",

    # Compositor
    "BlendMode",
    "LayerType",
    "Layer",
    "CompositorConfig",
    "BackgroundCompositor",
]

__version__ = "1.0.0"
