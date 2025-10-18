"""
Slider widget for numeric value selection
"""

from typing import Optional, Callable
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State


class Slider(Widget):
    """
    A slider for selecting numeric values.
    
    Example:
        >>> volume = State(50)
        >>> slider = Slider(
        ...     value=volume,
        ...     min_value=0,
        ...     max_value=100,
        ...     on_change=lambda val: print(f"Volume: {val}")
        ... )
    """
    
    def __init__(
        self,
        value: State | float = 0,
        min_value: float = 0,
        max_value: float = 100,
        step: float = 1,
        track_color: str = "#C6C6C8",
        active_color: str = "#007AFF",
        thumb_color: str = "#FFFFFF",
        disabled: bool = False,
        on_change: Optional[Callable[[float], None]] = None,
        **kwargs
    ):
        """
        Initialize a Slider widget.
        
        Args:
            value: Current value (can be State object)
            min_value: Minimum value
            max_value: Maximum value
            step: Step increment
            track_color: Track (background) color
            active_color: Active portion color
            thumb_color: Thumb (handle) color
            disabled: Whether slider is disabled
            on_change: Callback when value changes
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self._value_source = value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.track_color = track_color
        self.active_color = active_color
        self.thumb_color = thumb_color
        self.disabled = disabled
        self.on_change = on_change
        
        self._is_dragging = False
        
        if isinstance(value, State):
            self.watch(value)
    
    @property
    def value(self) -> float:
        """Get current slider value"""
        if isinstance(self._value_source, State):
            return float(self._value_source.value)
        return float(self._value_source)
    
    def set_value(self, new_value: float) -> None:
        """Set slider value"""
        # Clamp to range
        clamped = max(self.min_value, min(self.max_value, new_value))
        
        # Apply step
        if self.step > 0:
            clamped = round(clamped / self.step) * self.step
        
        if isinstance(self._value_source, State):
            self._value_source.value = clamped
        else:
            self._value_source = clamped
        
        if self.on_change:
            self.on_change(clamped)
        
        self._trigger_rebuild()
    
    def handle_drag(self, x: float, width: float) -> None:
        """Handle drag event to update value"""
        if self.disabled:
            return
        
        # Calculate percentage
        percentage = max(0, min(1, x / width))
        
        # Map to value range
        new_value = self.min_value + percentage * (self.max_value - self.min_value)
        self.set_value(new_value)
    
    def build(self) -> dict:
        """Build the slider's visual representation"""
        # Calculate percentage for rendering
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        return {
            "type": "slider",
            "value": self.value,
            "percentage": percentage,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "track_color": self.track_color,
            "active_color": self.active_color,
            "thumb_color": self.thumb_color,
            "disabled": self.disabled,
            "width": self.width or 200,
            "height": self.height or 4,
            "margin": self.margin,
            "position": (self.x, self.y),
            "on_drag": self.handle_drag
        }
