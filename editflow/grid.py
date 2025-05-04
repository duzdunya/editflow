from typing import Union, Tuple, Literal
import moviepy as mp


class GridSystem:
    """A grid system for positioning clips in a screen.
    
    The grid divides the screen into a 12x12 grid, allowing for
    consistent positioning of elements.
    """
    
    def __init__(self, screen_size: Tuple[int, int] = (1920, 1080)):
        """Initialize a grid system with the given screen size.
        
        Args:
            screen_size: Screen dimensions (width, height) in pixels
        """
        self.screen_size = screen_size
        self.column_gap = screen_size[0] / 12
        self.row_gap = screen_size[1] / 12

    def get_coords(self, 
                  clip: mp.VideoClip, 
                  pos: Tuple[int, int] = (0, 0), 
                  span: Tuple[int, int] = (1, 1), 
                  anchor: Literal["center", "left", "right", "top", "bottom", 
                                "topleft", "topright", "bottomleft", "bottomright"] = "topleft", 
                  offset: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
        """Calculate the pixel coordinates for a clip based on grid position.
        
        Args:
            clip: The clip to position
            pos: Grid position (row, column)
            span: Grid span (rows, columns)
            anchor: Positioning anchor point
            offset: Pixel offset from the calculated position
            
        Returns:
            Pixel coordinates (x, y) for the clip
        """
        column_gap = self.column_gap
        row_gap = self.row_gap

        offset_anchor = anchor.lower().strip(" ")
        row = pos[0]
        column = pos[1]

        # Get the base position in the grid
        default_x = column * column_gap
        default_y = row * row_gap

        # Apply offsets
        offset_x = offset[0]
        offset_y = offset[1]

        # Calculate the final position based on the anchor
        if offset_anchor == "center":
            return (default_x + column_gap/2) - clip.w/2, (default_y + row_gap/2) - clip.h/2
            
        elif offset_anchor == "left":
            return default_x - offset_x*(clip.w/2), (default_y + row_gap/2) - clip.h/2
            
        elif offset_anchor == "top":
            return (default_x + column_gap/2) - clip.w/2, default_y - offset_y*(clip.h/2)
            
        elif offset_anchor == "right":
            return (default_x + column_gap) - clip.w + offset_x*(clip.w/2), (default_y + row_gap/2) - clip.h/2
            
        elif offset_anchor == "bottom":
            return (default_x + column_gap/2) - clip.w/2, default_y + row_gap - clip.h + offset_y*(clip.h/2)
            
        elif offset_anchor == "topleft":
            return default_x - offset_x*(clip.w/2), default_y - offset_y*(clip.h/2)
            
        elif offset_anchor == "topright":
            return (default_x + column_gap) - clip.w + offset_x*(clip.w/2), default_y - offset_y*(clip.h/2)
            
        elif offset_anchor == "bottomleft":
            return default_x - offset_x*(clip.w/2), default_y + row_gap - clip.h + offset_y*(clip.h/2)
            
        elif offset_anchor == "bottomright":
            return (default_x + column_gap) - clip.w + offset_x*(clip.w/2), default_y + row_gap - clip.h + offset_y*(clip.h/2)
            
        else:
            raise ValueError("Unknown anchor. Must be 'center', 'left', 'top', 'right', 'bottom', 'topleft', 'topright', 'bottomleft', 'bottomright'")
