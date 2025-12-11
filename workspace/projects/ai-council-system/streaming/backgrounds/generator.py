"""
Dynamic Background Generator

Generates mood-reactive backgrounds based on debate sentiment. Supports multiple
visual styles including gradients, particles, geometric patterns, and generative art.

Author: AI Council System
Phase: 4.5 - Sentiment-Based Dynamic Backgrounds
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math
import random
from enum import Enum

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from .sentiment import DebateMood, MoodState


class BackgroundStyle(Enum):
    """Visual styles for backgrounds"""
    GRADIENT = "gradient"
    PARTICLES = "particles"
    GEOMETRIC = "geometric"
    WAVES = "waves"
    NEBULA = "nebula"
    MATRIX = "matrix"
    NEURAL = "neural"


@dataclass
class ColorPalette:
    """Color palette for a mood"""
    primary: str  # Hex color
    secondary: str
    accent: str
    particles: str
    glow: str

    def to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_primary_rgb(self) -> Tuple[int, int, int]:
        return self.to_rgb(self.primary)

    def get_secondary_rgb(self) -> Tuple[int, int, int]:
        return self.to_rgb(self.secondary)

    def get_accent_rgb(self) -> Tuple[int, int, int]:
        return self.to_rgb(self.accent)


# Mood-based color palettes
MOOD_PALETTES: Dict[DebateMood, ColorPalette] = {
    DebateMood.CALM_AGREEMENT: ColorPalette(
        primary="#3498db",    # Calm blue
        secondary="#2ecc71",  # Peaceful green
        accent="#ecf0f1",     # Light gray
        particles="#5dade2",  # Light blue
        glow="#a9cce3"
    ),
    DebateMood.THOUGHTFUL_ANALYSIS: ColorPalette(
        primary="#9b59b6",    # Deep purple
        secondary="#34495e",  # Dark gray
        accent="#7f8c8d",     # Medium gray
        particles="#bb8fce",  # Light purple
        glow="#d7bde2"
    ),
    DebateMood.HEATED_DEBATE: ColorPalette(
        primary="#e74c3c",    # Hot red
        secondary="#f39c12",  # Orange
        accent="#c0392b",     # Dark red
        particles="#ec7063",  # Light red
        glow="#f5b7b1"
    ),
    DebateMood.CONSENSUS_BUILDING: ColorPalette(
        primary="#16a085",    # Teal
        secondary="#27ae60",  # Green
        accent="#f39c12",     # Gold accent
        particles="#48c9b0",  # Light teal
        glow="#a3e4d7"
    ),
    DebateMood.CONSENSUS_REACHED: ColorPalette(
        primary="#2ecc71",    # Victory green
        secondary="#27ae60",  # Deep green
        accent="#f1c40f",     # Gold
        particles="#58d68d",  # Light green
        glow="#abebc6"
    ),
    DebateMood.INTENSE_DISAGREEMENT: ColorPalette(
        primary="#c0392b",    # Deep red
        secondary="#e74c3c",  # Bright red
        accent="#34495e",     # Dark contrast
        particles="#e74c3c",  # Red particles
        glow="#f1948a"
    ),
    DebateMood.CURIOUS_EXPLORATION: ColorPalette(
        primary="#3498db",    # Explorer blue
        secondary="#9b59b6",  # Mystery purple
        accent="#1abc9c",     # Curiosity teal
        particles="#85c1e9",  # Sky blue
        glow="#aed6f1"
    ),
    DebateMood.PASSIONATE_ADVOCACY: ColorPalette(
        primary="#e67e22",    # Passionate orange
        secondary="#d35400",  # Deep orange
        accent="#f39c12",     # Bright accent
        particles="#f0b27a",  # Light orange
        glow="#f8c471"
    ),
}


@dataclass
class Particle:
    """Individual particle for particle system"""
    x: float
    y: float
    vx: float  # Velocity X
    vy: float  # Velocity Y
    size: float
    alpha: float  # Opacity
    color: Tuple[int, int, int]
    lifetime: float = 1.0


@dataclass
class BackgroundConfig:
    """Configuration for background generation"""
    style: BackgroundStyle
    width: int
    height: int
    fps: int = 30
    particle_count: int = 100
    animation_speed: float = 1.0


class BackgroundGenerator:
    """
    Generates dynamic backgrounds based on debate mood

    Features:
    - Multiple visual styles (gradient, particles, geometric, waves)
    - Mood-reactive color palettes
    - Intensity-based animation speed
    - Smooth transitions between states
    - Particle systems with physics
    """

    def __init__(self, config: BackgroundConfig):
        """
        Initialize background generator

        Args:
            config: Background configuration
        """
        self.config = config
        self.particles: List[Particle] = []
        self.frame_count = 0
        self.current_palette: Optional[ColorPalette] = None
        self.transition_progress = 1.0  # 0.0 to 1.0

        # Initialize particles
        self._init_particles()

    def _init_particles(self):
        """Initialize particle system"""
        self.particles.clear()

        for _ in range(self.config.particle_count):
            particle = Particle(
                x=random.uniform(0, self.config.width),
                y=random.uniform(0, self.config.height),
                vx=random.uniform(-1, 1),
                vy=random.uniform(-1, 1),
                size=random.uniform(1, 4),
                alpha=random.uniform(0.3, 0.8),
                color=(255, 255, 255),
                lifetime=random.uniform(0.5, 1.0)
            )
            self.particles.append(particle)

    def generate_frame(self, mood_state: MoodState) -> Dict:
        """
        Generate a single frame based on current mood

        Args:
            mood_state: Current mood state from sentiment analyzer

        Returns:
            Dictionary describing the frame (for rendering engines)
        """
        # Get palette for current mood
        palette = MOOD_PALETTES.get(mood_state.mood, MOOD_PALETTES[DebateMood.THOUGHTFUL_ANALYSIS])

        # Update transition if mood changed
        if self.current_palette != palette:
            self.transition_progress = 0.0
            self.current_palette = palette

        # Advance transition
        if self.transition_progress < 1.0:
            self.transition_progress = min(1.0, self.transition_progress + 0.05 * mood_state.transition_speed)

        # Generate frame based on style
        if self.config.style == BackgroundStyle.GRADIENT:
            frame = self._generate_gradient_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.PARTICLES:
            frame = self._generate_particle_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.GEOMETRIC:
            frame = self._generate_geometric_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.WAVES:
            frame = self._generate_wave_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.NEBULA:
            frame = self._generate_nebula_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.MATRIX:
            frame = self._generate_matrix_frame(mood_state, palette)
        elif self.config.style == BackgroundStyle.NEURAL:
            frame = self._generate_neural_frame(mood_state, palette)
        else:
            frame = self._generate_gradient_frame(mood_state, palette)

        self.frame_count += 1
        return frame

    def _generate_gradient_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate animated gradient background"""
        # Calculate gradient angle based on time and intensity
        angle = (self.frame_count * mood.intensity * 0.5) % 360

        # Pulsing effect based on energy
        pulse = 0.8 + (0.2 * math.sin(self.frame_count * mood.energy_level * 0.1))

        return {
            "type": "gradient",
            "angle": angle,
            "colors": [
                palette.primary,
                palette.secondary,
                palette.accent
            ],
            "stops": [0.0, 0.5, 1.0],
            "pulse": pulse,
            "transition_progress": self.transition_progress
        }

    def _generate_particle_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate particle system background"""
        # Update particles based on mood
        particle_data = []

        for particle in self.particles:
            # Apply mood-based velocity multiplier
            speed_mult = 1.0 + (mood.intensity * 2.0)

            # Update position
            particle.x += particle.vx * speed_mult
            particle.y += particle.vy * speed_mult

            # Wrap around screen
            if particle.x < 0:
                particle.x = self.config.width
            elif particle.x > self.config.width:
                particle.x = 0

            if particle.y < 0:
                particle.y = self.config.height
            elif particle.y > self.config.height:
                particle.y = 0

            # Update color based on palette
            particle.color = palette.to_rgb(palette.particles)

            # Controversy creates erratic movement
            if mood.controversy_level > 0.5:
                particle.vx += random.uniform(-0.1, 0.1) * mood.controversy_level
                particle.vy += random.uniform(-0.1, 0.1) * mood.controversy_level

            # Consensus creates ordered movement
            if mood.consensus_level > 0.7:
                # Attract to center
                center_x, center_y = self.config.width / 2, self.config.height / 2
                dx = center_x - particle.x
                dy = center_y - particle.y
                particle.vx += dx * 0.0001 * mood.consensus_level
                particle.vy += dy * 0.0001 * mood.consensus_level

            # Update lifetime and respawn if needed
            particle.lifetime -= 0.01
            if particle.lifetime <= 0:
                particle.lifetime = 1.0
                particle.alpha = random.uniform(0.3, 0.8)

            particle_data.append({
                "x": particle.x,
                "y": particle.y,
                "size": particle.size * (1.0 + mood.intensity * 0.5),
                "alpha": particle.alpha,
                "color": particle.color
            })

        return {
            "type": "particles",
            "particles": particle_data,
            "background_color": palette.primary,
            "glow": mood.energy_level > 0.7
        }

    def _generate_geometric_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate geometric pattern background"""
        # Number of shapes based on intensity
        shape_count = int(5 + (mood.intensity * 10))

        # Rotation based on controversy
        rotation = (self.frame_count * mood.controversy_level * 2.0) % 360

        # Scale based on consensus (consensus = smaller, focused shapes)
        scale = 0.5 + (0.5 * (1.0 - mood.consensus_level))

        shapes = []
        for i in range(shape_count):
            angle = (i / shape_count) * 360
            radius = 100 + (i * 20 * scale)

            shapes.append({
                "type": "polygon",
                "sides": 6,  # Hexagon
                "center_x": self.config.width / 2,
                "center_y": self.config.height / 2,
                "radius": radius,
                "rotation": rotation + angle,
                "color": palette.primary if i % 2 == 0 else palette.secondary,
                "alpha": 0.3 + (mood.energy_level * 0.3)
            })

        return {
            "type": "geometric",
            "shapes": shapes,
            "background_color": palette.accent
        }

    def _generate_wave_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate animated wave background"""
        # Number of waves based on intensity
        wave_count = int(3 + (mood.intensity * 5))

        waves = []
        for i in range(wave_count):
            # Wave parameters affected by mood
            amplitude = 30 + (mood.energy_level * 50)
            frequency = 0.01 + (mood.controversy_level * 0.02)
            phase = (self.frame_count * mood.intensity * 0.05) + (i * 0.5)

            waves.append({
                "amplitude": amplitude,
                "frequency": frequency,
                "phase": phase,
                "color": palette.primary if i % 3 == 0 else (palette.secondary if i % 3 == 1 else palette.accent),
                "alpha": 0.4 + (mood.consensus_level * 0.3),
                "y_offset": (i / wave_count) * self.config.height
            })

        return {
            "type": "waves",
            "waves": waves,
            "background_color": palette.accent
        }

    def _generate_nebula_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate nebula-like background (cloud/smoke effect)"""
        # Swirl intensity based on controversy
        swirl = mood.controversy_level * 2.0

        # Brightness based on energy
        brightness = 0.5 + (mood.energy_level * 0.5)

        # Time-based evolution
        time_offset = self.frame_count * 0.01 * mood.intensity

        return {
            "type": "nebula",
            "colors": [palette.primary, palette.secondary, palette.glow],
            "swirl": swirl,
            "brightness": brightness,
            "time_offset": time_offset,
            "turbulence": mood.intensity,
            "scale": 100 + (mood.controversy_level * 100)
        }

    def _generate_matrix_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate Matrix-style digital rain"""
        # Column count based on intensity
        column_count = int(20 + (mood.intensity * 30))

        # Speed based on energy
        speed = 1.0 + (mood.energy_level * 3.0)

        columns = []
        for i in range(column_count):
            columns.append({
                "x": (i / column_count) * self.config.width,
                "speed": speed * random.uniform(0.8, 1.2),
                "length": random.randint(10, 30),
                "offset": random.randint(0, self.config.height),
                "characters": "01" if mood.consensus_level > 0.7 else "01?!",
                "color": palette.primary
            })

        return {
            "type": "matrix",
            "columns": columns,
            "background_color": "#000000",
            "glow": mood.intensity > 0.7
        }

    def _generate_neural_frame(self, mood: MoodState, palette: ColorPalette) -> Dict:
        """Generate neural network visualization"""
        # Node count based on complexity
        node_count = int(10 + (mood.intensity * 20))

        # Connection probability based on consensus
        connection_prob = 0.2 + (mood.consensus_level * 0.5)

        nodes = []
        connections = []

        # Generate nodes
        for i in range(node_count):
            nodes.append({
                "x": random.uniform(50, self.config.width - 50),
                "y": random.uniform(50, self.config.height - 50),
                "size": 5 + (mood.energy_level * 10),
                "color": palette.particles,
                "pulse_phase": random.uniform(0, 2 * math.pi)
            })

        # Generate connections
        for i in range(node_count):
            for j in range(i + 1, node_count):
                if random.random() < connection_prob:
                    # Calculate distance for connection strength
                    dx = nodes[i]["x"] - nodes[j]["x"]
                    dy = nodes[i]["y"] - nodes[j]["y"]
                    distance = math.sqrt(dx * dx + dy * dy)

                    connections.append({
                        "from": i,
                        "to": j,
                        "alpha": max(0.1, 1.0 - (distance / self.config.width)),
                        "color": palette.accent
                    })

        # Pulse based on frame count
        pulse_phase = (self.frame_count * mood.intensity * 0.1) % (2 * math.pi)

        return {
            "type": "neural",
            "nodes": nodes,
            "connections": connections,
            "background_color": palette.secondary,
            "pulse_phase": pulse_phase,
            "activity_level": mood.energy_level
        }

    def reset(self):
        """Reset generator state"""
        self.frame_count = 0
        self.current_palette = None
        self.transition_progress = 1.0
        self._init_particles()

    def get_statistics(self) -> Dict:
        """Get generator statistics"""
        return {
            "frames_generated": self.frame_count,
            "particle_count": len(self.particles),
            "style": self.config.style.value,
            "current_palette": self.current_palette.primary if self.current_palette else "none",
            "transition_progress": self.transition_progress
        }
