"""
Vertical Box layout container
"""

from typing import List, Optional
from pocketpy.widgets.base import Widget


class VBox(Widget):
    """
    A vertical layout container that arranges children in a column.
    
    Example:
        >>> layout = VBox(
        ...     children=[
        ...         Label(text="Title"),
        ...         Button(text="Click Me"),
        ...         Label(text="Footer")
        ...     ],
        ...     spacing=10
        ... )
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        spacing: float = 0,
        alignment: str = "start",
        **kwargs
    ):
        """
        Initialize a VBox layout container.
        
        Args:
            children: List of child widgets to arrange vertically
            spacing: Space between children (in pixels)
            alignment: Horizontal alignment ('start', 'center', 'end', 'stretch')
            **kwargs: Additional styling properties
        """
        super().__init__(children=children, **kwargs)
        self.spacing = spacing
        self.alignment = alignment
    
    def build(self) -> dict:
        """
        Build the VBox layout.
        
        Returns:
            Dictionary describing the layout
        """
        # Calculate positions for children
        current_y = self.y
        if self.padding:
            current_y += self.padding[0] if isinstance(self.padding, tuple) else self.padding
        
        for child in self.children:
            # Set child position
            child.x = self.x
            if self.padding:
                child.x += self.padding[1] if len(self.padding) > 1 else self.padding[0]
            
            child.y = current_y
            
            # Calculate next Y position
            child_height = child.height or 0
            current_y += child_height + self.spacing
        
        return {
            "type": "vbox",
            "children": [child.build() for child in self.children],
            "spacing": self.spacing,
            "alignment": self.alignment,
            "width": self.width,
            "height": self.height,
            "background_color": self.background_color,
            "padding": self.padding,
            "margin": self.margin,
            "position": (self.x, self.y)
        }
