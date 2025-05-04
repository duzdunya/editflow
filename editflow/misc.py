from typing import Union, Any, List, Dict, Tuple, Callable
import json
import numpy as np
#from scipy.optimize import bisect

def bisect(func, a, b, xtol=1e-6, maxiter=100):
    """
    Find root of a function within an interval using bisection method.
    
    Args:
        func: The function to find the root of
        a: Lower bound of interval
        b: Upper bound of interval
        xtol: Tolerance for convergence
        maxiter: Maximum number of iterations
        
    Returns:
        The approximated root of the function
    """
    fa = func(a)
    fb = func(b)
    
    # Check if either endpoint is already a root
    if abs(fa) < xtol:
        return a
    if abs(fb) < xtol:
        return b
    
    # Handle the case where the function doesn't change sign
    if fa * fb >= 0:
        # If both values are positive, return the endpoint with the smaller value
        if fa > 0 and fb > 0:
            return a if fa < fb else b
        # If both values are negative, return the endpoint with the larger value
        elif fa < 0 and fb < 0:
            return a if fa > fb else b
        # If one or both are zero
        else:
            return a if abs(fa) < abs(fb) else b
    
    # Standard bisection method when the function changes sign
    for _ in range(maxiter):
        # Calculate midpoint
        c = (a + b) / 2
        
        # Check if we've reached desired tolerance
        if b - a < xtol:
            return c
        
        fc = func(c)
        
        # Check if midpoint is a root
        if abs(fc) < xtol:
            return c
            
        # Update interval
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    # Return best approximation after maxiter iterations
    return (a + b) / 2

def invert_easing(fn: Callable[[float], float], y_target: float, tol: float = 1e-6) -> float:
    """Invert an easing function to find the input that produces a given output.
    
    Args:
        fn: The easing function to invert
        y_target: The target output value
        tol: Tolerance for the bisection method
        
    Returns:
        The input value that produces y_target when passed to fn
    """
    return bisect(lambda x: fn(x) - y_target, 0, 1, xtol=tol)


def interpolate(a: float, b: float, weight: float) -> float:
    """Interpolate between two values with a given weight.
    
    Args:
        a: Starting value
        b: Ending value
        weight: Interpolation weight (0 to 1)
        
    Returns:
        Interpolated value
    """
    if weight == 0:
        weight += 0.0001  # Avoid division by zero issues
    return a + (b - a) * weight


def get_info(screen) -> None:
    """Print detailed timing information about a screen and its components.
    
    Args:
        screen: A Screen object
    """
    n = 26
    print((n+3)*"*")
    print("* " + f'Screen\'s begin 0.0')
    print("* " + f'Screen\'s finish {screen.finish}')
    print("* " + f'Screen\'s lifetime {screen.lifetime}')
    
    for film in screen.children:
        print((n+3)*"*")
        print("* " + f'Film\'s begin {film.begin}')
        print("* " + f'Film\'s finish {film.finish}')
        print("* " + f'Film\'s lifetime {film.lifetime}')
        
        for tape in film.children:
            print((n+3)*"*")
            print("* " + " "*4 + f'NAME {tape.name}')
            print("* " + " "*4 + f'Tape\'s begin {tape.begin}')
            print("* " + " "*4 + f'Tape\'s finish {tape.finish}')
            print("* " + " "*4 + f'Tape\'s lifetime {tape.lifetime}')
            print("-")
            print("* " + " "*8 + f'Tape.clip\'s start {tape.clip.start}')
            print("* " + " "*8 + f'Tape.clip\'s end {tape.clip.end}')
            print("* " + " "*8 + f'Tape.clip\'s duration {tape.clip.duration}')

    print((n+3)*"*")
    print("\n")
