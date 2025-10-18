"""
TextInput widget for text entry
"""

from typing import Optional, Callable
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State


class TextInput(Widget):
    """
    A text input field for user text entry.
    
    Example:
        >>> text_state = State("")
        >>> input_field = TextInput(
        ...     value=text_state,
        ...     placeholder="Enter your name",
        ...     on_change=lambda text: print(f"Changed: {text}")
        ... )
    """
    
    def __init__(
        self,
        value: State | str = "",
        placeholder: str = "Enter text...",
        font_size: int = 16,
        font_family: str = "sans-serif",
        color: str = "#000000",
        background_color: str = "#FFFFFF",
        border_color: str = "#C6C6C8",
        focus_border_color: str = "#007AFF",
        placeholder_color: str = "#8E8E93",
        secure: bool = False,
        multiline: bool = False,
        max_length: Optional[int] = None,
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
        on_focus: Optional[Callable[[], None]] = None,
        on_blur: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """
        Initialize a TextInput widget.
        
        Args:
            value: Current text value (can be State object)
            placeholder: Placeholder text when empty
            font_size: Font size
            font_family: Font family
            color: Text color
            background_color: Background color
            border_color: Border color
            focus_border_color: Border color when focused
            placeholder_color: Placeholder text color
            secure: Whether to hide text (password field)
            multiline: Whether to allow multiple lines
            max_length: Maximum text length
            on_change: Callback when text changes
            on_submit: Callback when enter is pressed
            on_focus: Callback when field gains focus
            on_blur: Callback when field loses focus
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self._value_source = value
        self.placeholder = placeholder
        self.font_size = font_size
        self.font_family = font_family
        self.color = color
        self.background_color = background_color
        self.border_color = border_color
        self.focus_border_color = focus_border_color
        self.placeholder_color = placeholder_color
        self.secure = secure
        self.multiline = multiline
        self.max_length = max_length
        self.on_change = on_change
        self.on_submit = on_submit
        self.on_focus = on_focus
        self.on_blur = on_blur
        
        self._is_focused = False
        self._cursor_position = 0
        
        if isinstance(value, State):
            self.watch(value)
    
    @property
    def value(self) -> str:
        """Get current text value"""
        if isinstance(self._value_source, State):
            return str(self._value_source.value)
        return str(self._value_source)
    
    @value.setter
    def value(self, new_value: str):
        """Set text value"""
        if isinstance(self._value_source, State):
            self._value_source.value = new_value
        else:
            self._value_source = new_value
        
        if self.on_change:
            self.on_change(new_value)
        
        self._trigger_rebuild()
    
    def handle_key_press(self, key: str) -> None:
        """Handle keyboard input"""
        current = self.value
        
        if key == "backspace":
            if len(current) > 0:
                self.value = current[:-1]
        elif key == "enter":
            if not self.multiline and self.on_submit:
                self.on_submit(current)
            elif self.multiline:
                self.value = current + "\n"
        elif len(key) == 1:
            if self.max_length is None or len(current) < self.max_length:
                self.value = current + key
    
    def handle_focus(self) -> None:
        """Handle focus event"""
        self._is_focused = True
        if self.on_focus:
            self.on_focus()
        self._trigger_rebuild()
    
    def handle_blur(self) -> None:
        """Handle blur event"""
        self._is_focused = False
        if self.on_blur:
            self.on_blur()
        self._trigger_rebuild()
    
    def build(self) -> dict:
        """Build the text input's visual representation"""
        current_border = self.focus_border_color if self._is_focused else self.border_color
        
        display_text = self.value
        if self.secure and display_text:
            display_text = "•" * len(display_text)
        
        return {
            "type": "textinput",
            "text": display_text,
            "placeholder": self.placeholder if not display_text else "",
            "font_size": self.font_size,
            "font_family": self.font_family,
            "color": self.color,
            "placeholder_color": self.placeholder_color,
            "background_color": self.background_color,
            "border_color": current_border,
            "is_focused": self._is_focused,
            "width": self.width or 200,
            "height": self.height or 40,
            "padding": self.padding or (8, 12),
            "margin": self.margin,
            "position": (self.x, self.y),
            "on_key_press": self.handle_key_press,
            "on_focus": self.handle_focus,
            "on_blur": self.handle_blur
        }
