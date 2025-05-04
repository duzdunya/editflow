from typing import Union, Optional, List, Tuple, Dict, Any
from .component import Component
from .tape import Tape


class Film(Component):
    """A Film represents a collection of Tapes in the EditFlow system.
    
    Films organize multiple Tapes into coherent segments that can be
    arranged and composed in a Screen. Films handle the timing and
    positioning of their contained Tapes.
    """
    
    def __init__(self, name: str = "default_film"):
        """Initialize an empty Film.
        
        Args:
            name: A descriptive name for this film
        """
        super().__init__(name=name)
    
    def add_tape(self,
                 tape: Union[Tape, List[Tape]],
                 method: str = "compose",
                 start: float = 0.0,
                 effects: List = None,
                 pos: Tuple[int, int] = None,
                 span: Tuple[int, int] = None,
                 anchor: str = None,
                 offset: Tuple[int, int] = None,
                 z_index: Optional[int] = None) -> 'Film':
        """Add a Tape or list of Tapes to this Film.
        
        Args:
            tape: The Tape or list of Tapes to add
            method: How to add the tape(s) ("compose", "concat", "last")
            start: Start time when using "compose" method
            effects: List of effects to apply to the tape(s)
            pos: Grid position (row, column)
            span: Grid span (rows, columns)
            anchor: Positioning anchor point
            offset: Pixel offset from the grid position
            z_index: Layer order for rendering
            
        Returns:
            self for method chaining
        """
        # Handle lists of tapes
        if isinstance(tape, list):
            for t in tape:
                self.add_tape(t, method, start, effects, pos, span, anchor, offset, z_index)
            return self
            
        # Validate tape type
        if not isinstance(tape, Tape):
            raise TypeError("You must provide a Tape or list of Tapes to add_tape")
            
        # Add the tape as a component
        self.add_component(tape, method, start)
        
        # Get the most recently added tape
        added_tape = self.children[-1]
        
        # Apply attributes specific to Tape objects
        self.apply_attributes(added_tape, 
                             effects=effects, 
                             pos=pos, 
                             span=span, 
                             anchor=anchor, 
                             offset=offset, 
                             z_index=z_index)
        
        return self
    
    def apply_attributes(self, tape: Tape, **attributes):
        """Apply attributes specific to Tape objects.
        
        Args:
            tape: The tape to modify
            **attributes: The attributes to apply
        """
        # Apply each attribute if it's provided (not None)
        if attributes.get('effects') is not None:
            tape.effects += attributes['effects']
            
        if attributes.get('pos') is not None:
            tape.pos = attributes['pos']
            
        if attributes.get('span') is not None:
            tape.span = attributes['span']
            
        if attributes.get('anchor') is not None:
            tape.anchor = attributes['anchor']
            
        if attributes.get('offset') is not None:
            tape.offset = attributes['offset']
            
        # Apply z-index by setting layer_index on the clip
        if attributes.get('z_index') is not None:
            tape.clip = tape.clip.with_layer_index(attributes['z_index'])
