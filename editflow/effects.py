import math
from typing import Callable, Tuple, List, Union
import numpy as np
from . import easings
from .misc import interpolate


e = math.e


def cool_resize(t: float) -> float:
    """Create a pulsing resize effect.
    
    Args:
        t: Time in seconds
        
    Returns:
        Scale factor for the frame at time t
    """
    if t < 1.5:
        return 1 + 2 * math.pow(e, -7 * t)
    else:
        return 1


def brightness_effect(t: float) -> float:
    """Create a brightness adjustment effect.
    
    Args:
        t: Time in seconds
        
    Returns:
        Brightness factor for the frame at time t
    """
    if t < 3:
        return 1
    if 3 <= t < 4:
        return math.pow(t, -0.5) + ((math.pow(3, 0.5) - t/3) / math.pow(3, 0.5))
    else:
        return math.pow(4, -0.5) + ((math.pow(3, 0.5) - 4/3) / math.pow(3, 0.5))


def sin_heart_effect(t: float) -> float:
    """Create a pulsing heart-like effect.
    
    Args:
        t: Time in seconds
        
    Returns:
        Scale factor for the frame at time t
    """
    return 1 + (0.2 * math.sin(4 * t) + 0.2)


def oneToZeroAnim(t: float, 
                 duration: float, 
                 start_delay: float, 
                 easing_func: Callable[[float], float]) -> float:
    """Animate from one value to zero.
    
    Args:
        t: Current time
        duration: Animation duration
        start_delay: Delay before starting animation
        easing_func: Easing function to use
        
    Returns:
        Interpolated value between 0 and 1
    """
    if t < start_delay:
        return 0.0
    elif t >= start_delay:
        if (t - start_delay) > duration:
            return 1.0
        else:
            # Normalize time to 0-1 range
            normalized_t = (t - start_delay) / duration
            # Apply easing function
            relWeight = math.floor(easing_func(normalized_t) * 1000) / 1000
            return interpolate(0.0, 1.0, relWeight)


def moveAnim(t: float, 
            from_position: Tuple[float, float], 
            to_position: Tuple[float, float], 
            duration: float, 
            start_delay: float, 
            easing_func: Callable[[float], float]) -> Tuple[int, int]:
    """Animate movement between two positions.
    
    Args:
        t: Current time
        from_position: Starting position (x, y)
        to_position: Ending position (x, y)
        duration: Animation duration
        start_delay: Delay before starting animation
        easing_func: Easing function to use
        
    Returns:
        Current position (x, y) at time t
    """
    if t < start_delay:
        # Before start delay return starting position
        return from_position
    elif t >= start_delay:
        if (t - start_delay) > duration:
            # After animation completes, return ending position
            return to_position
        else:
            # Calculate progress using easing function
            normalized_t = (t - start_delay) / duration
            relWeight = math.floor(easing_func(normalized_t) * 1000) / 1000
            
            # Debug info
            interpolated_pos = (
                int(interpolate(from_position[0], to_position[0], relWeight)),
                int(interpolate(from_position[1], to_position[1], relWeight))
            )
            print(
                "from: ", from_position,
                " to: ", to_position,
                " interpolated: ", interpolated_pos
            )
            
            return interpolated_pos


def moveToMany(t: float, 
              positions: List[Tuple[float, float]], 
              each: float, 
              ease_duration: float, 
              start_delay: float, 
              easing_func: Callable[[float], float]) -> Tuple[int, int]:
    """Animate through multiple positions sequentially.
    
    Args:
        t: Current time
        positions: List of positions to move through
        each: Time to spend at each position
        ease_duration: Duration of animation between positions
        start_delay: Delay before starting animation
        easing_func: Easing function to use
        
    Returns:
        Current position (x, y) at time t
    """
    duration = len(positions) * each
    
    if t < start_delay:
        # Before start delay return first position
        return positions[0]
    elif t >= start_delay:
        # Adjust time by start delay
        t = t - start_delay
        
        # If beyond total duration, stay at last position
        if t >= duration:
            return positions[-1]
        
        # Find current segment
        current_index = int(t / each)
        
        # Handle edge case for last position
        if current_index >= len(positions) - 1:
            return positions[-1]
        
        # Calculate timing within the current segment
        segment_start_time = current_index * each
        segment_time = t - segment_start_time
        
        # If within easing duration, interpolate between positions
        if segment_time <= ease_duration:
            progress = segment_time / ease_duration
            relweight = math.floor(easing_func(progress) * 1000) / 1000
            
            return (
                int(interpolate(positions[current_index][0], positions[current_index + 1][0], relweight)),
                int(interpolate(positions[current_index][1], positions[current_index + 1][1], relweight))
            )
        # Otherwise, stay at the current position
        else:
            return positions[current_index + 1]
