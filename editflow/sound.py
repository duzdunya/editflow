import moviepy as mp
from typing import Optional
from .component import Component


class Sound(Component):
    """A Sound represents an audio clip in the EditFlow system.
    
    Sounds can be added to Tapes and have their own timing properties.
    Each Sound wraps a MoviePy AudioClip and adds additional metadata.
    """
    
    def __init__(self, clip: mp.AudioClip, name: str = "default_sound", adjust_to_clip: bool = False):
        """Initialize a Sound with a MoviePy audio clip.
        
        Args:
            clip: The MoviePy audio clip to wrap
            name: A descriptive name for this sound
        """
        super().__init__(name=name)
        self.clip = clip
        self.adjust_to_clip = adjust_to_clip

        self.start_offset = None
        self.fadein = None
        self.fadeout = None
    
    def with_fade(self, fadein: Optional[float] = None, fadeout: Optional[float] = None) -> 'Sound':
        """Set fade in and fade out durations for this sound.
        
        Args:
            fadein: Duration in seconds for fade in effect, or None for no fade
            fadeout: Duration in seconds for fade out effect, or None for no fade
            
        Returns:
            self for method chaining
        """
        self.fadein = fadein
        self.fadeout = fadeout
        return self
        
    def with_start_offset(self, offset: float) -> 'Sound':
        """Set a start offset for this sound.
        
        The start offset determines where to begin playing from the source clip.
        
        Args:
            offset: Time in seconds to offset from the beginning of the source
            
        Returns:
            self for method chaining
        """
        self.start_offset = offset
        return self
    
    @property
    def finish(self) -> float:
        """Calculate when this sound finishes.
        
        Returns:
            The end time of this sound
        """
        return self.begin + self.clip.duration
    
    @property
    def lifetime(self) -> float:
        """Calculate the duration of this sound.
        
        Returns:
            The duration of this sound
        """
        return self.clip.duration
