"""
Switch widget for boolean toggle
"""

from typing import Optional, Callable
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State


class Switch(Widget):
    """
    A toggle switch for boolean values.
    
    Example:
        >>> enabled = State(False)
        >>> switch = Switch(
        ...     value=enabled,
        ...     on_change=lambda val: print(f"Switch: {val}")
        ... )
    """
    
    def __init__(
        self,
        value: State | bool = False,
        on_color: str = "#34C759",
        off_color: str = "#C6C6C8",
        thumb_color: str = "#FFFFFF",
        disabled: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
        **kwargs
    ):
        """
        Initialize a Switch widget.
        
        Args:
            value: Current state (can be State object)
            on_color: Color when switch is on
            off_color: Color when switch is off
            thumb_color: Color of the sliding thumb
            disabled: Whether switch is disabled
            on_change: Callback when value changes
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self._value_source = value
        self.on_color = on_color
        self.off_color = off_color
        self.thumb_color = thumb_color
        self.disabled = disabled
        self.on_change = on_change
        
        if isinstance(value, State):
            self.watch(value)
    
    @property
    def value(self) -> bool:
        """Get current switch state"""
        if isinstance(self._value_source, State):
            return bool(self._value_source.value)
        return bool(self._value_source)
    
    def toggle(self) -> None:
        """Toggle the switch"""
        if self.disabled:
            return
        
        new_value = not self.value
        
        if isinstance(self._value_source, State):
            self._value_source.value = new_value
        else:
            self._value_source = new_value
        
        if self.on_change:
            self.on_change(new_value)
        
        self._trigger_rebuild()
    
    def build(self) -> dict:
        """Build the switch's visual representation"""
        return {
            "type": "switch",
            "value": self.value,
            "on_color": self.on_color,
            "off_color": self.off_color,
            "thumb_color": self.thumb_color,
            "disabled": self.disabled,
            "width": self.width or 51,
            "height": self.height or 31,
            "margin": self.margin,
            "position": (self.x, self.y),
            "on_press": self.toggle
        }
