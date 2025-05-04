from typing import Union, List, Tuple, Optional, Dict, Any, Callable
import moviepy as mp
from .component import Component
from .constants import Colors
from .grid import GridSystem
from .effects import moveAnim, moveToMany
from .film import Film
from .sound import Sound


class Screen(Component):
    """A Screen represents the final composition in the EditFlow system.
    
    Screens organize multiple Films into a complete video, handling
    positioning, timing, background, and export settings.
    """
    
    def __init__(self,
                 size: Tuple[int, int] = (1920, 1080),
                 fps: int = 24,
                 bgcolor = Colors.BLACK,
                 name: str = "default_screen"):
        """Initialize a Screen with the given settings.
        
        Args:
            size: Dimensions (width, height) in pixels
            fps: Frames per second for rendering
            bgcolor: Background color
            name: A descriptive name for this screen
        """
        super().__init__(name=name)
        self.size = size
        self.fps = fps
        self.bgcolor = bgcolor
        
        # Create a background color clip
        self.BACKGROUND = mp.ColorClip(size=self.size, color=bgcolor, duration=1).with_start(0)
        
        # Initialize grid system
        self.grid = GridSystem(screen_size=self.size)
        
        # Initialize audio
        self.bg_music = None
        
        # Final composition (set after compose())
        self._end = None
    
    def add_film(self,
                 film: Film,
                 method: str = "compose",
                 start: float = 0.0) -> 'Screen':
        """Add a Film to this Screen.
        
        Args:
            film: The Film to add
            method: How to add the film ("compose", "concat")
            start: Start time when using "compose" method
            
        Returns:
            self for method chaining
        """
        if len(film.children) == 0:
            raise ValueError("Film must have at least one tape")
            
        # Add film as a component
        self.add_component(film, method, start)
        
        return self
        
    def add_bg_music(self, 
                    sound: Sound,
                    fadein: float = 0, 
                    fadeout: float = 0, 
                    start_offset: float = 0.0) -> 'Screen':
        """Add background music to this Screen.
        
        Args:
            sound: The Sound to use as background music
            fadein: Duration in seconds for fade in effect
            fadeout: Duration in seconds for fade out effect
            start_offset: Time in seconds to offset from the beginning of the source
            
        Returns:
            self for method chaining
        """
        copysound = sound.copy()
        copysound.with_fade(fadein, fadeout)
        copysound.with_start_offset(start_offset)
        self.bg_music = copysound
        
        return self
    

    def compose(self) -> 'Screen':
        """Prepare all components for rendering.
        
        This method processes all films, tapes, and sounds, handling
        positioning, animations, and timing to create the final composition.
        
        Returns:
            self for method chaining
        """
        if len(self.children) == 0:
            raise ValueError("Screen must have at least one film")
            
        # Calculate total duration based on all films
        self.total_duration = self.finish
        
        # Prepare the background to match the total duration
        composelist = [self.BACKGROUND.with_duration(self.total_duration)]
        audiocomposelist = []
        
        # Process all films and their tapes
        for film in self.children:
            # Process each tape in the film
            for tape in film.children:
                # Create a reference to the original clip for modifications
                clip = tape.clip
                
                # Handle position animations
                if tape.animations.position is not None:
                    position_anim = tape.animations.position
                    
                    # Handle single position animation
                    if isinstance(position_anim.pos, tuple):
                        # Important: Create local variables for capturing in lambda
                        # to avoid late binding issues
                        from_coord = self.grid.get_coords(clip, 
                                                         pos=tape.pos, 
                                                         anchor=tape.anchor, 
                                                         offset=tape.offset)
                        to_coord = self.grid.get_coords(clip, 
                                                       pos=position_anim.pos, 
                                                       anchor=position_anim.anchor, 
                                                       offset=position_anim.offset)
                        
                        # Create a closure with fixed parameters
                        def create_pos_function(from_pos, to_pos, dur, delay, ease_fn):
                            # This creates a new function with fixed parameter values
                            return lambda t: moveAnim(
                                t, 
                                from_position=from_pos,
                                to_position=to_pos, 
                                duration=dur, 
                                start_delay=delay, 
                                easing_func=ease_fn
                            )
                        
                        # Use the factory function to create a position function
                        pos_function = create_pos_function(
                            from_coord, 
                            to_coord, 
                            position_anim.duration, 
                            position_anim.start_delay, 
                            position_anim.easing_func
                        )
                        
                        # Apply the position function to the clip
                        clip = clip.with_position(pos_function)
                        
                    # Handle multiple position animations
                    elif isinstance(position_anim.pos, list):
                        if position_anim.no_grid:
                            positions = position_anim.pos
                        else:
                            # Generate grid positions for each entry
                            positions = []
                            for idx, p in enumerate(position_anim.pos):
                                a = position_anim.anchor[idx] if isinstance(position_anim.anchor, list) else position_anim.anchor
                                o = position_anim.offset[idx] if isinstance(position_anim.offset, list) else position_anim.offset
                                positions.append(self.grid.get_coords(clip, pos=p, anchor=a, offset=o))
                        
                        # Create a closure with fixed parameters
                        def create_many_pos_function(pos_list, e, dur, delay, ease_fn):
                            return lambda t: moveToMany(
                                t, 
                                positions=pos_list, 
                                each=e, 
                                ease_duration=dur, 
                                start_delay=delay, 
                                easing_func=ease_fn
                            )
                        
                        # Use the factory function to create a position function
                        pos_function = create_many_pos_function(
                            positions, 
                            position_anim.each, 
                            position_anim.duration, 
                            position_anim.start_delay, 
                            position_anim.easing_func
                        )
                        
                        # Apply the position function to the clip
                        clip = clip.with_position(pos_function)
                
                # Handle scale animations (if implemented)
                if tape.animations.scale is not None:
                    # Implement scale animations here
                    pass
                    
                # Handle rotation animations (if implemented)
                if tape.animations.rotation is not None:
                    # Implement rotation animations here
                    pass
                    
                # Handle opacity animations (if implemented)
                if tape.animations.opacity is not None:
                    # Implement opacity animations here
                    pass
                    
                # Handle color animations (if implemented)
                if tape.animations.color is not None:
                    # Implement color animations here
                    pass
                    
                # Handle custom animations
                for name, animation in tape.animations.custom.items():
                    # Process custom animations based on their type
                    pass
                
                # Handle static positioning if no position animation
                if tape.animations.position is None and not tape.custom_position:
                    coord = self.grid.get_coords(clip, 
                                               pos=tape.pos, 
                                               anchor=tape.anchor, 
                                               offset=tape.offset)
                    clip = clip.with_position(coord)
                
                # Apply effects
                if tape.effects:
                    clip = clip.with_effects(tape.effects)
                
                # Set the start time if not using custom start
                if not tape.custom_start:
                    clip = clip.with_start(tape.begin)
                
                # Add the processed clip to the composition list
                composelist.append(clip)
                
                # Process sounds attached to the tape
                for sound in tape.children:
                    sound_clip = sound.clip.with_start(tape.begin+sound.begin)
                    if sound.adjust_to_clip:
                        sound_clip = sound_clip.with_duration(tape.lifetime)
                    audiocomposelist.append(sound_clip)

                if tape.clip.audio is not None:
                    videoaudio = tape.clip.audio
                    videoaudio = videoaudio.with_start(tape.begin)
                    audiocomposelist.append(videoaudio)
        
        # Create the final composite video
        self._end = mp.CompositeVideoClip(composelist, use_bgclip=True)
        
        # Add background music if specified
        if self.bg_music is not None:
            bg_clip = self.bg_music.clip.subclipped(
                self.bg_music.start_offset, 
                self.total_duration + self.bg_music.start_offset
            ).with_start(0.0)
            
            # Apply fade effects if specified
            if self.bg_music.fadein or self.bg_music.fadeout:
                effects = []
                if self.bg_music.fadein:
                    effects.append(mp.afx.AudioFadeIn(self.bg_music.fadein))
                if self.bg_music.fadeout:
                    effects.append(mp.afx.AudioFadeOut(self.bg_music.fadeout))
                bg_clip = bg_clip.with_effects(effects)
            
            audiocomposelist.append(bg_clip)
        
        # Create and attach the composite audio if any audio components exist
        if audiocomposelist:
            self._audio_end = mp.CompositeAudioClip(audiocomposelist)
            self._end = self._end.with_audio(self._audio_end)
        
        return self

    def render(self,
                      filename: str, 
                      codec: str = "mpeg4", 
                      bitrate: str = "4000k", 
                      threads: int = 4, 
                      logger = None, 
                      **kwargs) -> None:
        """Render the screen to a video file.
        
        Args:
            filename: Output filename
            codec: Video codec to use
            bitrate: Video bitrate
            threads: Number of processing threads
            logger: Optional logger for progress information
            **kwargs: Additional arguments for MoviePy's write_videofile
        """
        if self._ensure_ready():
            self._end.write_videofile(
                filename, 
                fps=self.fps, 
                codec=codec, 
                bitrate=bitrate, 
                threads=threads, 
                logger=logger, 
                **kwargs
            )
    
    def get_end_video(self) -> mp.VideoClip:
        """Get the final composited video clip.
        
        Returns:
            The rendered MoviePy video clip
        """
        if self._ensure_ready():
            return self._end
    
    def show(self, *args) -> None:
        """Show a preview of the video in a window.
        
        Args:
            *args: Arguments to pass to MoviePy's show method
        """
        if self._ensure_ready():
            self._end.show(*args)
    
    def preview(self, *args) -> None:
        """Show a preview of the video in the default media player.
        
        Args:
            *args: Arguments to pass to MoviePy's preview method
        """
        if self._ensure_ready():
            self._end.preview(*args)
    
    def _ensure_ready(self) -> bool:
        """Check if the screen is ready for output.
        
        Returns:
            True if ready, otherwise raises an exception
        """
        if not hasattr(self, '_end') or self._end is None:
            raise RuntimeError("Screen must be prepared with compose() first.")
        return True
