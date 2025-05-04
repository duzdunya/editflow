from typing import Union, Any, List, Dict, Optional
import copy as _copy


class Component:
    """Base class for all EditFlow components (Tape, Film, Screen).
    
    Provides common functionality for timing, component hierarchy, and copying.
    All component types inherit from this class to ensure consistent behavior.
    """
    
    def __init__(self, name: str = "unnamed_component"):
        """Initialize a component with default values.
        
        Args:
            name: A descriptive name for the component
        """
        self.name = name
        self.begin = 0.0
        self.children = []
    
    def add_component(self, component: 'Component', 
                      method: str = "compose",
                      start: float = 0.0) -> 'Component':
        """Add a child component using the specified method.
        
        Args:
            component: The component to add
            method: How to add the component:
                  - "compose": Start at specified time
                  - "concat": Start after the previous component ends
                  - "last": Start at the same time as the previous component
            start: Start time when using "compose" method
            
        Returns:
            self for method chaining
        """
        # Create a copy to avoid modifying the original
        component_copy = component.copy()
        
        if method == "compose":
            # Start at specified time relative to this component
            component_copy.begin = self.begin + start
            self.children.append(component_copy)
        elif method == "concat":
            if not self.children:
                # First child starts at the beginning of this component
                component_copy.begin = start
                self.children.append(component_copy)
            else:
                # Additional children start when the previous child finishes
                component_copy.begin = self.children[-1].finish + start
                self.children.append(component_copy)
        elif method == "last":
            if not self.children:
                # First child starts at the beginning of this component
                component_copy.begin = start
                self.children.append(component_copy)
            else:
                # Additional children start at the same time as previous child
                component_copy.begin = self.children[-1].begin + start
                self.children.append(component_copy)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'compose', 'concat', or 'last'.")
            
        return self
    
    def apply_attributes(self, component: 'Component', **attributes) -> None:
        """Apply custom attributes to a component.
        
        This method should be overridden by subclasses to handle
        type-specific attributes.
        
        Args:
            component: The component to modify
            **attributes: The attributes to apply
        """
        pass
        
    def copy(self) -> 'Component':
        """Create a shallow copy of this component.
        
        Returns:
            A copy of this component
        """
        return _copy.copy(self)
        
    @property
    def finish(self) -> float:
        """Calculate when this component finishes.
        
        Returns:
            The end time of this component
        """
        if not self.children:
            return self.begin
        return max([child.finish for child in self.children], default=self.begin)
        
    @property
    def lifetime(self) -> float:
        """Calculate the total duration of this component.
        
        Returns:
            The duration from begin to finish
        """
        return self.finish - self.begin
