"""
Background Compositor

Composites dynamic backgrounds with video content, managing layers, blending,
and smooth transitions between mood states.

Author: AI Council System
Phase: 4.5 - Sentiment-Based Dynamic Backgrounds
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math

from .sentiment import MoodState
from .generator import BackgroundGenerator, BackgroundConfig, BackgroundStyle


class BlendMode(Enum):
    """Blending modes for background composition"""
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    SOFT_LIGHT = "soft_light"
    ADD = "add"


class LayerType(Enum):
    """Types of layers in the composite"""
    BACKGROUND = "background"
    VIDEO = "video"
    OVERLAY = "overlay"
    FOREGROUND = "foreground"


@dataclass
class Layer:
    """Compositing layer"""
    layer_type: LayerType
    content: Dict  # Frame data or video reference
    opacity: float = 1.0
    blend_mode: BlendMode = BlendMode.NORMAL
    z_index: int = 0
    enabled: bool = True

    def __lt__(self, other):
        """Compare layers by z-index for sorting"""
        return self.z_index < other.z_index


@dataclass
class CompositorConfig:
    """Configuration for background compositor"""
    width: int
    height: int
    fps: int = 30
    background_opacity: float = 0.8
    enable_transitions: bool = True
    transition_duration: float = 2.0  # seconds
    blur_background: bool = False
    blur_amount: int = 5


class BackgroundCompositor:
    """
    Composites dynamic backgrounds with video content

    Features:
    - Multi-layer composition
    - Smooth transitions between moods
    - Blending modes
    - Opacity control
    - Layer management
    - Cross-fade support
    """

    def __init__(self, config: CompositorConfig):
        """
        Initialize background compositor

        Args:
            config: Compositor configuration
        """
        self.config = config
        self.layers: List[Layer] = []
        self.transition_active = False
        self.transition_progress = 0.0
        self.previous_background: Optional[Dict] = None
        self.current_background: Optional[Dict] = None

        # Performance tracking
        self.frames_composited = 0

    def add_layer(
        self,
        layer_type: LayerType,
        content: Dict,
        opacity: float = 1.0,
        blend_mode: BlendMode = BlendMode.NORMAL,
        z_index: int = 0
    ) -> Layer:
        """
        Add a new layer to the composition

        Args:
            layer_type: Type of layer
            content: Layer content (frame data or reference)
            opacity: Layer opacity (0.0 to 1.0)
            blend_mode: Blending mode
            z_index: Layer order (lower = behind)

        Returns:
            The created Layer object
        """
        layer = Layer(
            layer_type=layer_type,
            content=content,
            opacity=opacity,
            blend_mode=blend_mode,
            z_index=z_index
        )

        self.layers.append(layer)
        self._sort_layers()

        return layer

    def remove_layer(self, layer: Layer):
        """Remove a layer from the composition"""
        if layer in self.layers:
            self.layers.remove(layer)

    def _sort_layers(self):
        """Sort layers by z-index"""
        self.layers.sort()

    def set_background(self, background_frame: Dict, transition: bool = True):
        """
        Set new background with optional transition

        Args:
            background_frame: New background frame data
            transition: Whether to transition smoothly
        """
        if transition and self.config.enable_transitions and self.current_background:
            # Start transition
            self.previous_background = self.current_background
            self.current_background = background_frame
            self.transition_active = True
            self.transition_progress = 0.0
        else:
            # Immediate change
            self.current_background = background_frame
            self.previous_background = None
            self.transition_active = False

    def update_transition(self, delta_time: float):
        """
        Update transition state

        Args:
            delta_time: Time elapsed since last update (seconds)
        """
        if not self.transition_active:
            return

        # Advance transition
        progress_step = delta_time / self.config.transition_duration
        self.transition_progress += progress_step

        if self.transition_progress >= 1.0:
            # Transition complete
            self.transition_progress = 1.0
            self.transition_active = False
            self.previous_background = None

    def composite_frame(self, video_frame: Optional[Dict] = None) -> Dict:
        """
        Composite a complete frame with background and video

        Args:
            video_frame: Optional video content to overlay

        Returns:
            Composite frame description
        """
        composite = {
            "width": self.config.width,
            "height": self.config.height,
            "layers": []
        }

        # Add background layer(s)
        if self.transition_active and self.previous_background:
            # Transitioning between two backgrounds
            # Add fading-out previous background
            composite["layers"].append({
                "type": "background_previous",
                "content": self.previous_background,
                "opacity": (1.0 - self.transition_progress) * self.config.background_opacity,
                "blend_mode": BlendMode.NORMAL.value,
                "z_index": 0
            })

            # Add fading-in current background
            composite["layers"].append({
                "type": "background_current",
                "content": self.current_background,
                "opacity": self.transition_progress * self.config.background_opacity,
                "blend_mode": BlendMode.NORMAL.value,
                "z_index": 1
            })
        elif self.current_background:
            # Single background
            composite["layers"].append({
                "type": "background",
                "content": self.current_background,
                "opacity": self.config.background_opacity,
                "blend_mode": BlendMode.NORMAL.value,
                "z_index": 0,
                "blur": self.config.blur_amount if self.config.blur_background else 0
            })

        # Add video layer if provided
        if video_frame:
            composite["layers"].append({
                "type": "video",
                "content": video_frame,
                "opacity": 1.0,
                "blend_mode": BlendMode.NORMAL.value,
                "z_index": 10
            })

        # Add custom layers
        for layer in self.layers:
            if layer.enabled:
                composite["layers"].append({
                    "type": layer.layer_type.value,
                    "content": layer.content,
                    "opacity": layer.opacity,
                    "blend_mode": layer.blend_mode.value,
                    "z_index": layer.z_index
                })

        # Sort layers by z-index
        composite["layers"].sort(key=lambda x: x["z_index"])

        self.frames_composited += 1

        return composite

    def apply_mood_vignette(self, mood_state: MoodState) -> Layer:
        """
        Add a mood-based vignette overlay

        Args:
            mood_state: Current mood state

        Returns:
            The created vignette layer
        """
        # Vignette intensity based on controversy and intensity
        intensity = (mood_state.controversy_level + mood_state.intensity) / 2.0

        vignette = {
            "type": "vignette",
            "intensity": intensity * 0.5,  # Scale down for subtlety
            "color": "#000000",
            "feather": 0.6  # Soft edges
        }

        return self.add_layer(
            layer_type=LayerType.OVERLAY,
            content=vignette,
            opacity=0.4,
            blend_mode=BlendMode.MULTIPLY,
            z_index=100
        )

    def apply_glow_effect(self, mood_state: MoodState, color: str = "#FFFFFF") -> Layer:
        """
        Add a glow effect based on energy level

        Args:
            mood_state: Current mood state
            color: Glow color (hex)

        Returns:
            The created glow layer
        """
        # Glow intensity based on energy
        glow_strength = mood_state.energy_level * 0.3

        glow = {
            "type": "glow",
            "color": color,
            "strength": glow_strength,
            "radius": 20,
            "quality": "high"
        }

        return self.add_layer(
            layer_type=LayerType.OVERLAY,
            content=glow,
            opacity=glow_strength,
            blend_mode=BlendMode.ADD,
            z_index=90
        )

    def apply_chromatic_aberration(self, mood_state: MoodState) -> Layer:
        """
        Add chromatic aberration based on controversy

        Args:
            mood_state: Current mood state

        Returns:
            The created effect layer
        """
        # Effect intensity from controversy
        strength = mood_state.controversy_level * 5.0  # Pixels

        aberration = {
            "type": "chromatic_aberration",
            "strength": strength,
            "angle": 0.0
        }

        return self.add_layer(
            layer_type=LayerType.OVERLAY,
            content=aberration,
            opacity=1.0,
            blend_mode=BlendMode.NORMAL,
            z_index=110
        )

    def apply_blur_pulse(self, mood_state: MoodState, pulse_frequency: float = 1.0) -> Dict:
        """
        Create a pulsing blur effect based on energy

        Args:
            mood_state: Current mood state
            pulse_frequency: Pulse frequency in Hz

        Returns:
            Effect parameters
        """
        # Calculate pulse based on frame count
        pulse_phase = (self.frames_composited / self.config.fps) * pulse_frequency * 2 * math.pi
        pulse_value = (math.sin(pulse_phase) + 1) / 2  # 0 to 1

        blur_amount = pulse_value * mood_state.energy_level * 10

        return {
            "type": "blur",
            "amount": blur_amount,
            "quality": "medium"
        }

    def create_split_screen(
        self,
        left_content: Dict,
        right_content: Dict,
        split_position: float = 0.5,
        divider_width: int = 2,
        divider_color: str = "#FFFFFF"
    ) -> List[Layer]:
        """
        Create a split-screen composition

        Args:
            left_content: Content for left side
            right_content: Content for right side
            split_position: Split position (0.0 to 1.0)
            divider_width: Width of dividing line
            divider_color: Color of divider

        Returns:
            List of created layers
        """
        layers = []

        # Left side
        left_layer = Layer(
            layer_type=LayerType.VIDEO,
            content={
                **left_content,
                "crop": {
                    "x": 0,
                    "y": 0,
                    "width": int(self.config.width * split_position),
                    "height": self.config.height
                }
            },
            z_index=20
        )
        layers.append(left_layer)
        self.layers.append(left_layer)

        # Right side
        right_layer = Layer(
            layer_type=LayerType.VIDEO,
            content={
                **right_content,
                "crop": {
                    "x": int(self.config.width * split_position),
                    "y": 0,
                    "width": int(self.config.width * (1.0 - split_position)),
                    "height": self.config.height
                }
            },
            z_index=20
        )
        layers.append(right_layer)
        self.layers.append(right_layer)

        # Divider
        divider_layer = Layer(
            layer_type=LayerType.FOREGROUND,
            content={
                "type": "rectangle",
                "x": int(self.config.width * split_position) - (divider_width // 2),
                "y": 0,
                "width": divider_width,
                "height": self.config.height,
                "color": divider_color
            },
            z_index=30
        )
        layers.append(divider_layer)
        self.layers.append(divider_layer)

        self._sort_layers()

        return layers

    def create_picture_in_picture(
        self,
        main_content: Dict,
        pip_content: Dict,
        position: Tuple[int, int] = (50, 50),
        size: Tuple[int, int] = (320, 180),
        border_width: int = 2,
        border_color: str = "#FFFFFF"
    ) -> List[Layer]:
        """
        Create picture-in-picture composition

        Args:
            main_content: Main video content
            pip_content: Picture-in-picture content
            position: PiP position (x, y)
            size: PiP size (width, height)
            border_width: Border width
            border_color: Border color

        Returns:
            List of created layers
        """
        layers = []

        # Main content
        main_layer = Layer(
            layer_type=LayerType.VIDEO,
            content=main_content,
            z_index=10
        )
        layers.append(main_layer)
        self.layers.append(main_layer)

        # PiP border
        border_layer = Layer(
            layer_type=LayerType.FOREGROUND,
            content={
                "type": "rectangle",
                "x": position[0] - border_width,
                "y": position[1] - border_width,
                "width": size[0] + (border_width * 2),
                "height": size[1] + (border_width * 2),
                "color": border_color
            },
            z_index=50
        )
        layers.append(border_layer)
        self.layers.append(border_layer)

        # PiP content
        pip_layer = Layer(
            layer_type=LayerType.VIDEO,
            content={
                **pip_content,
                "position": position,
                "size": size
            },
            z_index=51
        )
        layers.append(pip_layer)
        self.layers.append(pip_layer)

        self._sort_layers()

        return layers

    def clear_layers(self, layer_type: Optional[LayerType] = None):
        """
        Clear layers, optionally filtered by type

        Args:
            layer_type: If specified, only clear layers of this type
        """
        if layer_type:
            self.layers = [layer for layer in self.layers if layer.layer_type != layer_type]
        else:
            self.layers.clear()

    def get_layer_count(self, layer_type: Optional[LayerType] = None) -> int:
        """
        Get count of layers, optionally filtered by type

        Args:
            layer_type: If specified, only count layers of this type

        Returns:
            Number of layers
        """
        if layer_type:
            return sum(1 for layer in self.layers if layer.layer_type == layer_type)
        return len(self.layers)

    def reset(self):
        """Reset compositor state"""
        self.layers.clear()
        self.transition_active = False
        self.transition_progress = 0.0
        self.previous_background = None
        self.current_background = None
        self.frames_composited = 0

    def get_statistics(self) -> Dict:
        """Get compositor statistics"""
        return {
            "frames_composited": self.frames_composited,
            "layer_count": len(self.layers),
            "transition_active": self.transition_active,
            "transition_progress": self.transition_progress,
            "background_set": self.current_background is not None
        }
