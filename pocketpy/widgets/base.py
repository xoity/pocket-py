"""
Base Widget class for PocketPy framework
All UI components inherit from this class
"""

from typing import Any, List, Optional, Callable
from abc import ABC, abstractmethod
from pocketpy.core.state import State


class Widget(ABC):
    """
    Base class for all PocketPy widgets.
    
    Widgets are the building blocks of your UI. Each widget represents
    a visual component that can be rendered on screen and can automatically
    respond to State changes.
    
    Example:
        >>> class MyButton(Widget):
        ...     def build(self):
        ...         return {"type": "button", "text": "Click Me"}
    """
    
    def __init__(
        self,
        children: Optional[List["Widget"]] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        background_color: Optional[str] = None,
        padding: Optional[tuple] = None,
        margin: Optional[tuple] = None,
        **kwargs: Any
    ):
        """
        Initialize a new Widget with styling and properties.
        
        Args:
            children: List of child widgets
            width: Width of the widget
            height: Height of the widget
            background_color: Background color (hex string)
            padding: Padding as (vertical, horizontal) or (top, right, bottom, left)
            margin: Margin as (vertical, horizontal) or (top, right, bottom, left)
            **kwargs: Additional widget-specific properties
        """
        self.children: List[Widget] = children or []
        self.parent: Optional[Widget] = None
        
        # Styling properties
        self.width = width
        self.height = height
        self.background_color = background_color
        self.padding = padding or (0, 0)
        self.margin = margin or (0, 0)
        
        # Additional properties
        self.props = kwargs
        
        # Internal state
        self._mounted = False
        self._subscriptions: List[Callable[[], None]] = []
        
        # Position (calculated during layout)
        self.x = 0
        self.y = 0
    
    @abstractmethod
    def build(self) -> Any:
        """
        Build the widget's visual representation.
        
        This method must be implemented by all widget subclasses.
        It should return the widget's rendered output.
        
        Returns:
            The widget's visual representation
        """
        pass
    
    def mount(self) -> None:
        """
        Called when the widget is mounted to the UI tree.
        Override this method to perform initialization logic.
        """
        self._mounted = True
        
        # Mount all children
        for child in self.children:
            child.parent = self
            child.mount()
    
    def unmount(self) -> None:
        """
        Called when the widget is removed from the UI tree.
        Override this method to perform cleanup logic.
        """
        self._mounted = False
        
        # Unsubscribe from all state objects
        self._cleanup_subscriptions()
        
        # Unmount all children
        for child in self.children:
            child.unmount()
    
    def watch(self, state: State, callback: Optional[Callable[[], None]] = None) -> None:
        """
        Subscribe to a State object and trigger a rebuild when it changes.
        
        Args:
            state: The State object to watch
            callback: Optional callback to execute on state change (before rebuild)
        """
        def on_change():
            if callback:
                callback()
            if self._mounted:
                self._trigger_rebuild()
        
        state.subscribe(on_change)
        self._subscriptions.append(lambda: state._listeners.remove(on_change))
    
    def _cleanup_subscriptions(self) -> None:
        """
        Clean up all state subscriptions.
        """
        for unsubscribe in self._subscriptions:
            try:
                unsubscribe()
            except (ValueError, AttributeError):
                pass  # Already unsubscribed
        self._subscriptions.clear()
    
    def _trigger_rebuild(self) -> None:
        """
        Trigger a rebuild of this widget.
        This will be called when watched State objects change.
        """
        # TODO: Implement rebuild/rerender logic
        # For now, just call build to ensure the method works
        self.build()
    
    def add_child(self, child: "Widget") -> None:
        """
        Add a child widget.
        
        Args:
            child: The child widget to add
        """
        child.parent = self
        self.children.append(child)
        if self._mounted:
            child.mount()
    
    def remove_child(self, child: "Widget") -> None:
        """
        Remove a child widget.
        
        Args:
            child: The child widget to remove
        """
        if child in self.children:
            child.unmount()
            child.parent = None
            self.children.remove(child)
    
    def __repr__(self) -> str:
        """
        String representation of the widget.
        """
        return f"{self.__class__.__name__}(children={len(self.children)})"
