from dataclasses import dataclass, field
from typing import Union, List, Tuple, Optional, Callable, Dict, Any
import copy


@dataclass
class Animation:
    """Base class for all animations."""
    
    # Duration of the animation in seconds
    duration: float = 1.0
    
    # Delay before the animation starts
    start_delay: float = 0.0
    
    # Easing function to use (defaults to linear in subclasses)
    easing_func: Optional[Callable[[float], float]] = None
    
    def copy(self) -> 'Animation':
        """Create a copy of this animation."""
        return copy.deepcopy(self)


@dataclass
class PositionAnimation(Animation):
    """Animation for moving elements between positions."""
    
    # Target position(s) - either a single position or list of positions
    pos: Union[Tuple[float, float], List[Tuple[float, float]]] = None
    
    # Anchor point for positioning
    anchor: Union[str, List[str]] = "topleft"
    
    # Offset from the anchor point (in pixels)
    offset: Union[Tuple[float, float], List[Tuple[float, float]]] = (0, 0)
    
    # Whether to bypass the grid system (use raw pixel coordinates)
    no_grid: bool = False
    
    # Time to spend at each position (for multi-position animations)
    each: float = 1.0


@dataclass
class ScaleAnimation(Animation):
    """Animation for scaling elements."""
    
    # Target scale factor(s) - either a single scale or list of scales
    scale: Union[float, List[float]] = 1.0
    
    # Whether to maintain aspect ratio
    maintain_aspect: bool = True
    
    # Pivot point for scaling (relative coordinates 0-1)
    pivot: Tuple[float, float] = (0.5, 0.5)


@dataclass
class RotationAnimation(Animation):
    """Animation for rotating elements."""
    
    # Target rotation(s) in degrees - either a single angle or list of angles
    angles: Union[float, List[float]] = 0.0
    
    # Pivot point for rotation (relative coordinates 0-1)
    pivot: Tuple[float, float] = (0.5, 0.5)
    
    # Whether to use the shortest rotation path
    use_shortest_path: bool = True


@dataclass
class OpacityAnimation(Animation):
    """Animation for changing opacity/transparency."""
    
    # Target opacity value(s) - either a single value or list of values (0-1)
    opacity: Union[float, List[float]] = 1.0


@dataclass
class ColorAnimation(Animation):
    """Animation for color transitions."""
    
    # Target color(s) - either a single color or list of colors (RGB tuples)
    color: Union[Tuple[int, int, int], List[Tuple[int, int, int]]] = (255, 255, 255)
    
    # Blend mode for the color transition
    blend_mode: str = "multiply"


@dataclass
class AnimationSet:
    """Collection of animations to apply to a component."""
    
    position: Optional[PositionAnimation] = None
    scale: Optional[ScaleAnimation] = None
    rotation: Optional[RotationAnimation] = None
    opacity: Optional[OpacityAnimation] = None
    color: Optional[ColorAnimation] = None
    
    # Additional custom animations
    custom: Dict[str, Animation] = field(default_factory=dict)
    
    def copy(self) -> 'AnimationSet':
        """Create a copy of this animation set."""
        return copy.deepcopy(self)


# Helper functions to create animations
def create_position_animation(pos, duration=1.0, easing_func=None, **kwargs) -> PositionAnimation:
    """Create a position animation with the given parameters."""
    return PositionAnimation(pos=pos, duration=duration, easing_func=easing_func, **kwargs)


def create_scale_animation(scale, duration=1.0, easing_func=None, **kwargs) -> ScaleAnimation:
    """Create a scale animation with the given parameters."""
    return ScaleAnimation(scale=scale, duration=duration, easing_func=easing_func, **kwargs)


def create_rotation_animation(angles, duration=1.0, easing_func=None, **kwargs) -> RotationAnimation:
    """Create a rotation animation with the given parameters."""
    return RotationAnimation(angles=angles, duration=duration, easing_func=easing_func, **kwargs)


def create_opacity_animation(opacity, duration=1.0, easing_func=None, **kwargs) -> OpacityAnimation:
    """Create an opacity animation with the given parameters."""
    return OpacityAnimation(opacity=opacity, duration=duration, easing_func=easing_func, **kwargs)


def create_color_animation(color, duration=1.0, easing_func=None, **kwargs) -> ColorAnimation:
    """Create a color animation with the given parameters."""
    return ColorAnimation(color=color, duration=duration, easing_func=easing_func, **kwargs)
