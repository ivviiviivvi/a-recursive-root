"""
Sentiment-Based Mood Analyzer for Dynamic Backgrounds

This module analyzes debate sentiment in real-time to determine the visual mood
for dynamic background generation. It tracks emotional intensity, controversy,
and debate flow to create reactive visual experiences.

Author: AI Council System
Phase: 4.5 - Sentiment-Based Dynamic Backgrounds
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
import statistics


class DebateMood(Enum):
    """Visual mood states for debates"""
    CALM_AGREEMENT = "calm_agreement"
    THOUGHTFUL_ANALYSIS = "thoughtful_analysis"
    HEATED_DEBATE = "heated_debate"
    CONSENSUS_BUILDING = "consensus_building"
    CONSENSUS_REACHED = "consensus_reached"
    INTENSE_DISAGREEMENT = "intense_disagreement"
    CURIOUS_EXPLORATION = "curious_exploration"
    PASSIONATE_ADVOCACY = "passionate_advocacy"


class SentimentTone(Enum):
    """Sentiment tones detected in debate"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


@dataclass
class SentimentReading:
    """Individual sentiment reading from a debate contribution"""
    timestamp: datetime
    speaker: str
    sentiment_score: float  # -1.0 (very negative) to 1.0 (very positive)
    intensity: float  # 0.0 (calm) to 1.0 (intense)
    confidence: float  # Agent's confidence level
    emotion: str  # Primary emotion detected
    controversy_factor: float  # 0.0 to 1.0


@dataclass
class MoodState:
    """Current mood state of the debate"""
    mood: DebateMood
    intensity: float  # 0.0 to 1.0
    sentiment_tone: SentimentTone
    controversy_level: float  # 0.0 to 1.0
    energy_level: float  # 0.0 to 1.0
    consensus_level: float  # 0.0 (no consensus) to 1.0 (full consensus)
    timestamp: datetime
    transition_speed: float = 1.0  # Multiplier for transition speed

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "mood": self.mood.value,
            "intensity": self.intensity,
            "sentiment_tone": self.sentiment_tone.value,
            "controversy_level": self.controversy_level,
            "energy_level": self.energy_level,
            "consensus_level": self.consensus_level,
            "timestamp": self.timestamp.isoformat(),
            "transition_speed": self.transition_speed
        }


class SentimentAnalyzer:
    """
    Analyzes debate sentiment to determine visual mood for backgrounds

    Features:
    - Real-time sentiment tracking
    - Emotional arc detection
    - Controversy measurement
    - Consensus tracking
    - Intensity scaling
    - Smooth mood transitions
    """

    def __init__(
        self,
        smoothing_window: int = 5,
        mood_transition_threshold: float = 0.3,
        intensity_sensitivity: float = 1.0
    ):
        """
        Initialize sentiment analyzer

        Args:
            smoothing_window: Number of recent readings to smooth over
            mood_transition_threshold: Minimum change required to switch moods
            intensity_sensitivity: Multiplier for intensity calculations
        """
        self.smoothing_window = smoothing_window
        self.mood_transition_threshold = mood_transition_threshold
        self.intensity_sensitivity = intensity_sensitivity

        self.readings: List[SentimentReading] = []
        self.current_mood: Optional[MoodState] = None
        self.mood_history: List[MoodState] = []

    def add_reading(
        self,
        speaker: str,
        text: str,
        confidence: float,
        emotion: Optional[str] = None,
        sentiment_override: Optional[float] = None
    ) -> SentimentReading:
        """
        Add a new sentiment reading from a debate contribution

        Args:
            speaker: Name of the speaker
            text: The text content
            confidence: Speaker's confidence level (0-1)
            emotion: Optional emotion override
            sentiment_override: Optional manual sentiment score

        Returns:
            SentimentReading object
        """
        # Analyze sentiment from text (simplified - in production use NLP)
        sentiment_score = sentiment_override if sentiment_override is not None else self._analyze_text_sentiment(text)

        # Calculate intensity from text features
        intensity = self._calculate_intensity(text, confidence)

        # Detect primary emotion
        primary_emotion = emotion or self._detect_emotion(text, sentiment_score)

        # Calculate controversy factor
        controversy = self._calculate_controversy(sentiment_score, intensity)

        reading = SentimentReading(
            timestamp=datetime.now(),
            speaker=speaker,
            sentiment_score=sentiment_score,
            intensity=intensity,
            confidence=confidence,
            emotion=primary_emotion,
            controversy_factor=controversy
        )

        self.readings.append(reading)

        # Keep only recent readings for performance
        if len(self.readings) > 100:
            self.readings = self.readings[-100:]

        return reading

    def get_current_mood(self) -> MoodState:
        """
        Calculate current debate mood based on recent readings

        Returns:
            MoodState object representing current mood
        """
        if not self.readings:
            # Default calm state
            return MoodState(
                mood=DebateMood.THOUGHTFUL_ANALYSIS,
                intensity=0.3,
                sentiment_tone=SentimentTone.NEUTRAL,
                controversy_level=0.0,
                energy_level=0.3,
                consensus_level=1.0,
                timestamp=datetime.now()
            )

        # Get recent readings for analysis
        recent = self.readings[-self.smoothing_window:]

        # Calculate aggregate metrics
        avg_sentiment = statistics.mean(r.sentiment_score for r in recent)
        avg_intensity = statistics.mean(r.intensity for r in recent)
        avg_controversy = statistics.mean(r.controversy_factor for r in recent)

        # Calculate sentiment variance (measure of disagreement)
        sentiment_variance = statistics.variance(r.sentiment_score for r in recent) if len(recent) > 1 else 0.0

        # Calculate energy level from intensity and confidence
        avg_confidence = statistics.mean(r.confidence for r in recent)
        energy_level = (avg_intensity + avg_confidence) / 2.0

        # Calculate consensus level (inverse of variance)
        consensus_level = max(0.0, 1.0 - (sentiment_variance * 2.0))

        # Determine sentiment tone
        sentiment_tone = self._classify_sentiment_tone(avg_sentiment)

        # Determine mood based on all factors
        mood = self._determine_mood(
            avg_sentiment,
            avg_intensity,
            avg_controversy,
            consensus_level,
            energy_level
        )

        # Calculate transition speed (faster for sudden changes)
        transition_speed = 1.0
        if self.current_mood and self.current_mood.mood != mood:
            transition_speed = 2.0  # Speed up transitions on mood changes

        new_mood_state = MoodState(
            mood=mood,
            intensity=min(1.0, avg_intensity * self.intensity_sensitivity),
            sentiment_tone=sentiment_tone,
            controversy_level=avg_controversy,
            energy_level=energy_level,
            consensus_level=consensus_level,
            timestamp=datetime.now(),
            transition_speed=transition_speed
        )

        # Update current mood and history
        self.current_mood = new_mood_state
        self.mood_history.append(new_mood_state)

        # Keep history manageable
        if len(self.mood_history) > 50:
            self.mood_history = self.mood_history[-50:]

        return new_mood_state

    def get_mood_arc(self, duration_seconds: int = 60) -> List[MoodState]:
        """
        Get the emotional arc over the last N seconds

        Args:
            duration_seconds: How far back to look

        Returns:
            List of mood states in chronological order
        """
        cutoff_time = datetime.now().timestamp() - duration_seconds

        return [
            mood for mood in self.mood_history
            if mood.timestamp.timestamp() >= cutoff_time
        ]

    def _analyze_text_sentiment(self, text: str) -> float:
        """
        Analyze sentiment from text (simplified version)
        In production, use proper NLP models

        Returns:
            Sentiment score from -1.0 to 1.0
        """
        # Simple keyword-based sentiment (replace with NLP in production)
        positive_words = {
            'good', 'great', 'excellent', 'agree', 'support', 'benefit',
            'positive', 'helpful', 'important', 'necessary', 'progress',
            'improve', 'better', 'constructive', 'valuable', 'promising'
        }

        negative_words = {
            'bad', 'wrong', 'disagree', 'oppose', 'harmful', 'negative',
            'problematic', 'dangerous', 'risky', 'concerning', 'worse',
            'damage', 'threat', 'issue', 'problem', 'failure'
        }

        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        # Calculate score
        score = (positive_count - negative_count) / len(words)
        return max(-1.0, min(1.0, score * 10))  # Scale and clamp

    def _calculate_intensity(self, text: str, confidence: float) -> float:
        """Calculate intensity based on text features and confidence"""
        # Check for intensity markers
        intensity_markers = ['!', '!!', 'very', 'extremely', 'absolutely', 'must', 'critical']
        intensity_count = sum(text.count(marker) for marker in intensity_markers)

        # Length can indicate thoroughness/intensity
        word_count = len(text.split())
        length_factor = min(1.0, word_count / 100)  # Normalize to 0-1

        # Combine factors
        base_intensity = min(1.0, (intensity_count * 0.15) + (confidence * 0.5) + (length_factor * 0.35))

        return base_intensity

    def _detect_emotion(self, text: str, sentiment: float) -> str:
        """Detect primary emotion (simplified)"""
        text_lower = text.lower()

        # Check for specific emotional indicators
        if any(word in text_lower for word in ['must', 'critical', 'urgent', 'essential']):
            return 'determined'
        elif any(word in text_lower for word in ['concerned', 'worried', 'risky', 'dangerous']):
            return 'concerned'
        elif any(word in text_lower for word in ['excited', 'promising', 'opportunity']):
            return 'enthusiastic'
        elif any(word in text_lower for word in ['careful', 'consider', 'analyze']):
            return 'analytical'
        elif sentiment > 0.5:
            return 'optimistic'
        elif sentiment < -0.5:
            return 'critical'
        else:
            return 'neutral'

    def _calculate_controversy(self, sentiment: float, intensity: float) -> float:
        """Calculate controversy factor"""
        # High intensity with extreme sentiment indicates controversy
        sentiment_extremity = abs(sentiment)
        return min(1.0, (sentiment_extremity * 0.6) + (intensity * 0.4))

    def _classify_sentiment_tone(self, sentiment: float) -> SentimentTone:
        """Classify overall sentiment tone"""
        if sentiment > 0.3:
            return SentimentTone.POSITIVE
        elif sentiment < -0.3:
            return SentimentTone.NEGATIVE
        elif abs(sentiment) < 0.1:
            return SentimentTone.NEUTRAL
        else:
            return SentimentTone.MIXED

    def _determine_mood(
        self,
        sentiment: float,
        intensity: float,
        controversy: float,
        consensus: float,
        energy: float
    ) -> DebateMood:
        """
        Determine debate mood from aggregate metrics

        Uses a decision tree based on key factors
        """
        # High consensus moods
        if consensus > 0.7:
            if sentiment > 0.3:
                return DebateMood.CONSENSUS_REACHED
            elif intensity < 0.4:
                return DebateMood.CALM_AGREEMENT
            else:
                return DebateMood.CONSENSUS_BUILDING

        # High controversy/disagreement
        if controversy > 0.7 or consensus < 0.3:
            if intensity > 0.7:
                return DebateMood.INTENSE_DISAGREEMENT
            else:
                return DebateMood.HEATED_DEBATE

        # Medium intensity analytical discussion
        if intensity < 0.5 and abs(sentiment) < 0.3:
            return DebateMood.THOUGHTFUL_ANALYSIS

        # Curious exploration (neutral sentiment, moderate energy)
        if abs(sentiment) < 0.2 and 0.3 < energy < 0.7:
            return DebateMood.CURIOUS_EXPLORATION

        # Passionate advocacy (strong sentiment, high energy)
        if abs(sentiment) > 0.5 and energy > 0.6:
            return DebateMood.PASSIONATE_ADVOCACY

        # Default to thoughtful analysis
        return DebateMood.THOUGHTFUL_ANALYSIS

    def reset(self):
        """Reset analyzer state"""
        self.readings.clear()
        self.current_mood = None
        self.mood_history.clear()

    def get_statistics(self) -> Dict:
        """Get statistics about sentiment analysis"""
        if not self.readings:
            return {"total_readings": 0}

        return {
            "total_readings": len(self.readings),
            "avg_sentiment": statistics.mean(r.sentiment_score for r in self.readings),
            "avg_intensity": statistics.mean(r.intensity for r in self.readings),
            "avg_controversy": statistics.mean(r.controversy_factor for r in self.readings),
            "current_mood": self.current_mood.mood.value if self.current_mood else "unknown",
            "mood_changes": len(self.mood_history),
            "speakers": len(set(r.speaker for r in self.readings))
        }
