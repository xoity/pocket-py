"""
Label widget for displaying text
"""

from typing import Optional
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State


class Label(Widget):
    """
    A widget for displaying text.
    
    Example:
        >>> label = Label(text="Hello, World!", font_size=16)
        
        >>> # With reactive state
        >>> username = State("Guest")
        >>> label = Label(text=username)
        >>> label.watch(username)
    """
    
    def __init__(
        self,
        text: str | State = "",
        font_size: int = 14,
        font_family: str = "sans-serif",
        color: str = "#000000",
        text_align: str = "left",
        **kwargs
    ):
        """
        Initialize a Label widget.
        
        Args:
            text: The text to display (can be a string or State object)
            font_size: Size of the font
            font_family: Font family name
            color: Text color (hex string)
            text_align: Text alignment ('left', 'center', 'right')
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        # Store the text (might be a State object)
        self._text_source = text
        self.font_size = font_size
        self.font_family = font_family
        self.color = color
        self.text_align = text_align
        
        # If text is a State object, watch it
        if isinstance(text, State):
            self.watch(text)
    
    @property
    def text(self) -> str:
        """
        Get the current text value.
        
        Returns:
            The text string
        """
        if isinstance(self._text_source, State):
            return str(self._text_source.value)
        return str(self._text_source)
    
    def build(self) -> dict:
        """
        Build the label's visual representation.
        
        Returns:
            Dictionary describing the label
        """
        return {
            "type": "label",
            "text": self.text,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "color": self.color,
            "text_align": self.text_align,
            "width": self.width,
            "height": self.height,
            "background_color": self.background_color,
            "padding": self.padding,
            "margin": self.margin,
            "position": (self.x, self.y)
        }
