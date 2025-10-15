"""
Base Widget class for PocketPy framework
All UI components inherit from this class
"""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class Widget(ABC):
    """
    Base class for all PocketPy widgets.
    
    Widgets are the building blocks of your UI. Each widget represents
    a visual component that can be rendered on screen.
    
    Example:
        >>> class MyButton(Widget):
        ...     def render(self):
        ...         return {"type": "button", "text": self.props.get("text", "Click")}
    """
    
    def __init__(self, **props: Any):
        """
        Initialize a new Widget with the given properties.
        
        Args:
            **props: Widget properties (similar to React props)
        """
        self.props: Dict[str, Any] = props
        self.children: List[Widget] = props.get("children", [])
        self.parent: Optional[Widget] = None
        self._mounted = False
    
    @abstractmethod
    def render(self) -> Dict[str, Any]:
        """
        Render the widget to a dictionary representation.
        
        This method must be implemented by all widget subclasses.
        It should return a dictionary describing how the widget
        should be displayed.
        
        Returns:
            A dictionary representation of the widget
        """
        pass
    
    def mount(self) -> None:
        """
        Called when the widget is mounted to the UI tree.
        Override this method to perform initialization logic.
        """
        self._mounted = True
    
    def unmount(self) -> None:
        """
        Called when the widget is removed from the UI tree.
        Override this method to perform cleanup logic.
        """
        self._mounted = False
    
    def update(self, **new_props: Any) -> None:
        """
        Update the widget's properties.
        
        Args:
            **new_props: New properties to merge with existing ones
        """
        self.props.update(new_props)
        if self._mounted:
            self._trigger_rerender()
    
    def add_child(self, child: "Widget") -> None:
        """
        Add a child widget.
        
        Args:
            child: The child widget to add
        """
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: "Widget") -> None:
        """
        Remove a child widget.
        
        Args:
            child: The child widget to remove
        """
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def _trigger_rerender(self) -> None:
        """
        Trigger a re-render of this widget.
        This will be called when properties change.
        """
        # TODO: Implement rerender logic
        pass
    
    def __repr__(self) -> str:
        """
        String representation of the widget.
        """
        return f"{self.__class__.__name__}(props={self.props})"
