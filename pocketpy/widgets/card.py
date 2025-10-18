"""
Card widget for grouped content with elevation
"""

from typing import Optional, List
from pocketpy.widgets.base import Widget


class Card(Widget):
    """
    A card container with elevation and rounded corners.
    
    Example:
        >>> card = Card(
        ...     children=[Label("Title"), Label("Content")],
        ...     elevation="md",
        ...     padding=16
        ... )
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        background_color: str = "#FFFFFF",
        border_color: Optional[str] = None,
        border_width: int = 0,
        border_radius: int = 12,
        elevation: str = "md",  # "none", "sm", "md", "lg", "xl"
        padding: int | tuple = 16,
        **kwargs
    ):
        """
        Initialize a Card widget.
        
        Args:
            children: Child widgets
            background_color: Card background color
            border_color: Border color (optional)
            border_width: Border width in pixels
            border_radius: Corner radius
            elevation: Shadow elevation level
            padding: Internal padding
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.children = children or []
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.elevation = elevation
        self.card_padding = padding
        
        # Watch all children
        for child in self.children:
            if hasattr(child, '_parent'):
                child._parent = self
    
    def build(self) -> dict:
        """Build the card's visual representation"""
        # Build all children
        built_children = [child.build() for child in self.children]
        
        return {
            "type": "card",
            "children": built_children,
            "background_color": self.background_color,
            "border_color": self.border_color,
            "border_width": self.border_width,
            "border_radius": self.border_radius,
            "elevation": self.elevation,
            "padding": self.card_padding,
            "width": self.width,
            "height": self.height,
            "margin": self.margin,
            "position": (self.x, self.y)
        }
