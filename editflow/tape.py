import moviepy as mp
from typing import Union, Optional, List, Tuple, Callable, Dict, Any
from .component import Component
from .sound import Sound
from . import easings
from .animations import (
    Animation, PositionAnimation, ScaleAnimation,
    RotationAnimation, OpacityAnimation, ColorAnimation, AnimationSet
)


class Tape(Component):
    """A Tape represents a single media clip with properties and animations.
    
    Tapes are the basic building blocks of EditFlow compositions.
    Each Tape wraps a MoviePy clip and adds positioning, animation,
    and other metadata.
    """
    
    def __init__(self, clip: mp.Clip, custom_start: bool = False, custom_position: bool = False, name: str = "default_tape"):
        """Initialize a Tape with a MoviePy clip.
        
        Args:
            clip: The MoviePy clip to wrap
            custom_start: Whether this tape has its start time managed externally
            name: A descriptive name for this tape
        """
        super().__init__(name=name)
        self.clip = clip
        self.custom_start = custom_start
        self.custom_position = custom_position
        
        # Positioning properties
        self.pos = (0, 0)
        self.offset = (0, 0)
        self.anchor = "topleft"
        # span is not used
        self.span = (1, 1)
        
        # Effects and animations
        self.effects = []
        self.animations = AnimationSet()
        
    def add_sound(self, sound: Sound, method: str = "compose", start: float = 0.0) -> 'Tape':
        """Add a sound to this tape.
        
        Args:
            sound: The sound to add
            method: How to add the sound ("compose", "concat")
            start: Start time when using "compose" method
            
        Returns:
            self for method chaining
        """
        return self.add_component(sound, method, start)
        
    def apply_attributes(self, sound: Sound, **attributes) -> None:
        """Apply attributes to a sound component.
        
        Args:
            sound: The sound to modify
            **attributes: The attributes to apply
        """
        # Handle sound-specific attributes here if needed
        pass
    
    def with_position_animation(self, 
                               pos: Union[Tuple[float, float], List[Tuple[float, float]]],
                               duration: float = 1.0,
                               easing_func: Optional[Callable] = easings.easeInQuad,
                               start_delay: float = 0.0,
                               anchor: Union[str, List[str]] = "topleft",
                               offset: Union[Tuple[float, float], List[Tuple[float, float]]] = (0, 0),
                               no_grid: bool = False,
                               each: float = 1.0) -> 'Tape':
        """Add a position animation to this tape.
        
        Args:
            pos: Target position(s) - either a single position or list of positions
            duration: Duration of the animation in seconds, for mono-position
            easing_func: Easing function to use
            start_delay: Delay before the animation starts
            anchor: Anchor point for positioning
            offse: Offset from the anchor point (in pixels)
            no_grid: Whether to bypass the grid system (use raw pixel coordinates)
            each: Time to spend at each position (for multi-position animations)
            
        Returns:
            self for method chaining
        """
        self.animations.position = PositionAnimation(
            pos=pos,
            duration=duration,
            easing_func=easing_func,
            start_delay=start_delay,
            anchor=anchor,
            offset=offset,
            no_grid=no_grid,
            each=each
        )
        return self
    
    def with_scale_animation(self,
                           scale: Union[float, List[float]],
                           duration: float = 1.0,
                           easing_func: Optional[Callable] = None,
                           start_delay: float = 0.0,
                           maintain_aspect: bool = True,
                           pivot: Tuple[float, float] = (0.5, 0.5)) -> 'Tape':
        """Add a scale animation to this tape.
        
        Args:
            scale: Target scale factor(s)
            duration: Duration of the animation in seconds
            easing_func: Easing function to use
            start_delay: Delay before the animation starts
            maintain_aspect: Whether to maintain aspect ratio
            pivot: Pivot point for scaling (relative coordinates 0-1)
            
        Returns:
            self for method chaining
        """
        self.animations.scale = ScaleAnimation(
            scale=scale,
            duration=duration,
            easing_func=easing_func,
            start_delay=start_delay,
            maintain_aspect=maintain_aspect,
            pivot=pivot
        )
        return self
    
    def with_rotation_animation(self,
                              angles: Union[float, List[float]],
                              duration: float = 1.0,
                              easing_func: Optional[Callable] = None,
                              start_delay: float = 0.0,
                              pivot: Tuple[float, float] = (0.5, 0.5),
                              use_shortest_path: bool = True) -> 'Tape':
        """Add a rotation animation to this tape.
        
        Args:
            angles: Target rotation(s) in degrees
            duration: Duration of the animation in seconds
            easing_func: Easing function to use
            start_delay: Delay before the animation starts
            pivot: Pivot point for rotation (relative coordinates 0-1)
            use_shortest_path: Whether to use the shortest rotation path
            
        Returns:
            self for method chaining
        """
        self.animations.rotation = RotationAnimation(
            angles=angles,
            duration=duration,
            easing_func=easing_func,
            start_delay=start_delay,
            pivot=pivot,
            use_shortest_path=use_shortest_path
        )
        return self
    
    def with_opacity_animation(self,
                             opacity: Union[float, List[float]],
                             duration: float = 1.0,
                             easing_func: Optional[Callable] = None,
                             start_delay: float = 0.0) -> 'Tape':
        """Add an opacity animation to this tape.
        
        Args:
            opacity: Target opacity value(s) (0-1)
            duration: Duration of the animation in seconds
            easing_func: Easing function to use
            start_delay: Delay before the animation starts
            
        Returns:
            self for method chaining
        """
        self.animations.opacity = OpacityAnimation(
            opacity=opacity,
            duration=duration,
            easing_func=easing_func,
            start_delay=start_delay
        )
        return self
    
    def with_color_animation(self,
                           color: Union[Tuple[int, int, int], List[Tuple[int, int, int]]],
                           duration: float = 1.0,
                           easing_func: Optional[Callable] = None,
                           start_delay: float = 0.0,
                           blend_mode: str = "multiply") -> 'Tape':
        """Add a color animation to this tape.
        
        Args:
            color: Target color(s) (RGB tuples)
            duration: Duration of the animation in seconds
            easing_func: Easing function to use
            start_delay: Delay before the animation starts
            blend_mode: Blend mode for the color transition
            
        Returns:
            self for method chaining
        """
        self.animations.color = ColorAnimation(
            color=color,
            duration=duration,
            easing_func=easing_func,
            start_delay=start_delay,
            blend_mode=blend_mode
        )
        return self
    
    def with_custom_animation(self,
                            name: str,
                            animation: Animation) -> 'Tape':
        """Add a custom animation to this tape.
        
        Args:
            name: Name of the custom animation
            animation: The animation object
            
        Returns:
            self for method chaining
        """
        self.animations.custom[name] = animation
        return self
    
    # Legacy support for the original with_animations method
    def with_animations(self, animations: Dict[str, Dict[str, Any]]) -> 'Tape':
        """Legacy method to add animations using dictionary format.
        
        This method is maintained for backward compatibility.
        New code should use the specific animation methods.
        
        Args:
            animations: Dictionary of animation configurations
            
        Returns:
            self for method chaining
        """
        for key, config in animations.items():
            if key == "position":
                if config.get("pos") is not None:
                    self.with_position_animation(
                        pos=config.get("pos"),
                        duration=config.get("duration", 1.0),
                        easing_func=config.get("easing_func"),
                        start_delay=config.get("start_delay", 0.0),
                        anchor=config.get("anchor", "topleft"),
                        offset=config.get("offset", (0, 0)),
                        no_grid=config.get("no_grid", False),
                        each=config.get("each", 1.0)
                    )
            # Add handlers for other animation types as needed
                
        return self
        
    @property
    def finish(self) -> float:
        """Calculate when this tape finishes.
        
        Returns:
            The end time of this tape
        """
        # First check if there are any child sounds that extend beyond the clip
        child_finish = super().finish
        
        # Then consider the clip's own duration
        clip_finish = self.begin + self.clip.duration
        
        # Return the later of the two
        return max(child_finish, clip_finish)
        
    @property
    def lifetime(self) -> float:
        """Calculate the duration of this tape.
        
        Returns:
            The duration of this tape
        """
        return self.clip.duration
