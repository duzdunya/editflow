# Core components
from .component import Component
from .tape import Tape
from .film import Film
from .screen import Screen
from .sound import Sound
from .grid import GridSystem

# Animation system
from .animations import (
    Animation,
    PositionAnimation,
    ScaleAnimation,
    RotationAnimation,
    OpacityAnimation,
    ColorAnimation,
    AnimationSet,
    create_position_animation,
    create_scale_animation,
    create_rotation_animation,
    create_opacity_animation,
    create_color_animation
)

# Effects and utilities
from . import effects
from . import easings
from . import misc
from . import image_manipulation
from .constants import Colors

__version__ = "0.2.0" 
