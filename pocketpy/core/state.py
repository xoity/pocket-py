"""
Observable State class for PocketPy framework
Implements reactive state management
"""

from typing import Any, Callable, List


class State:
    """
    Observable state container for reactive UI updates.
    
    This class allows you to create reactive state that automatically
    notifies listeners when the value changes.
    
    Example:
        >>> state = State(initial_value=0)
        >>> state.subscribe(lambda: print(f"State changed to: {state.value}"))
        >>> state.value = 5  # Triggers listener notification
    """
    
    def __init__(self, initial_value: Any):
        """
        Initialize a new State object with an initial value.
        
        Args:
            initial_value: The initial value for this state
        """
        self._value: Any = initial_value
        self._listeners: List[Callable[[], None]] = []
    
    def subscribe(self, listener: Callable[[], None]) -> None:
        """
        Subscribe a listener function to state changes.
        
        Args:
            listener: A callback function that will be called when state changes
        """
        if listener not in self._listeners:
            self._listeners.append(listener)
    
    @property
    def value(self) -> Any:
        """
        Get the current state value.
        
        Returns:
            The current value
        """
        return self._value
    
    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set a new state value and notify all listeners.
        
        Args:
            new_value: The new value to set
        """
        self._value = new_value
        # Notify all listeners
        for listener in self._listeners:
            listener()
