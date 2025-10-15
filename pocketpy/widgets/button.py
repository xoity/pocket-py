"""
Button widget for user interaction
"""

from typing import Optional, Callable
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State


class Button(Widget):
    """
    A clickable button widget.
    
    Example:
        >>> def handle_click():
        ...     print("Button clicked!")
        >>> button = Button(text="Click Me", on_press=handle_click)
        
        >>> # With reactive state
        >>> counter = State(0)
        >>> button = Button(
        ...     text=counter,
        ...     on_press=lambda: setattr(counter, 'value', counter.value + 1)
        ... )
    """
    
    def __init__(
        self,
        text: str | State = "Button",
        on_press: Optional[Callable[[], None]] = None,
        font_size: int = 14,
        font_family: str = "sans-serif",
        color: str = "#FFFFFF",
        background_color: str = "#007AFF",
        hover_color: str = "#0051D5",
        disabled: bool = False,
        **kwargs
    ):
        """
        Initialize a Button widget.
        
        Args:
            text: The button text (can be a string or State object)
            on_press: Callback function when button is pressed
            font_size: Size of the font
            font_family: Font family name
            color: Text color (hex string)
            background_color: Button background color
            hover_color: Background color when hovered
            disabled: Whether the button is disabled
            **kwargs: Additional styling properties
        """
        # Set default background color if not provided
        if "background_color" not in kwargs:
            kwargs["background_color"] = background_color
            
        super().__init__(**kwargs)
        
        # Store the text (might be a State object)
        self._text_source = text
        self.on_press = on_press
        self.font_size = font_size
        self.font_family = font_family
        self.color = color
        self.hover_color = hover_color
        self.disabled = disabled
        
        # Internal state
        self._is_hovered = False
        self._is_pressed = False
        
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
    
    def handle_press(self) -> None:
        """
        Handle button press event.
        """
        if not self.disabled and self.on_press:
            self.on_press()
    
    def handle_hover_enter(self) -> None:
        """
        Handle mouse hover enter event.
        """
        if not self.disabled:
            self._is_hovered = True
            self._trigger_rebuild()
    
    def handle_hover_exit(self) -> None:
        """
        Handle mouse hover exit event.
        """
        self._is_hovered = False
        self._trigger_rebuild()
    
    def build(self) -> dict:
        """
        Build the button's visual representation.
        
        Returns:
            Dictionary describing the button
        """
        # Determine current background color
        current_bg = self.background_color
        if self._is_hovered and not self.disabled:
            current_bg = self.hover_color
        
        return {
            "type": "button",
            "text": self.text,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "color": self.color,
            "background_color": current_bg,
            "disabled": self.disabled,
            "width": self.width,
            "height": self.height,
            "padding": self.padding or (10, 20),
            "margin": self.margin,
            "position": (self.x, self.y),
            "on_press": self.handle_press,
            "on_hover_enter": self.handle_hover_enter,
            "on_hover_exit": self.handle_hover_exit
        }
