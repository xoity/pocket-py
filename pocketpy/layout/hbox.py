"""
Horizontal Box layout container
"""

from typing import List, Optional
from pocketpy.widgets.base import Widget


class HBox(Widget):
    """
    A horizontal layout container that arranges children in a row.
    
    Example:
        >>> layout = HBox(
        ...     children=[
        ...         Button(text="Back"),
        ...         Label(text="Title"),
        ...         Button(text="Next")
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
        Initialize an HBox layout container.
        
        Args:
            children: List of child widgets to arrange horizontally
            spacing: Space between children (in pixels)
            alignment: Vertical alignment ('start', 'center', 'end', 'stretch')
            **kwargs: Additional styling properties
        """
        super().__init__(children=children, **kwargs)
        self.spacing = spacing
        self.alignment = alignment
    
    def build(self) -> dict:
        """
        Build the HBox layout.
        
        Returns:
            Dictionary describing the layout
        """
        # Calculate positions for children
        current_x = self.x
        if self.padding:
            current_x += self.padding[1] if len(self.padding) > 1 else self.padding[0]
        
        for child in self.children:
            # Set child position
            child.x = current_x
            child.y = self.y
            if self.padding:
                child.y += self.padding[0] if isinstance(self.padding, tuple) else self.padding
            
            # Calculate next X position
            child_width = child.width or 0
            current_x += child_width + self.spacing
        
        return {
            "type": "hbox",
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
