"""
Observable State class for PocketPy framework
Implements reactive state management
"""

from typing import Any, Callable, Dict, List, Optional


class State:
    """
    Observable state container for reactive UI updates.
    
    This class allows you to create reactive state that automatically
    notifies observers when values change, enabling automatic UI updates.
    
    Example:
        >>> state = State(count=0, name="John")
        >>> state.subscribe(lambda s: print(f"State changed: {s}"))
        >>> state.count = 5  # Triggers observer notification
    """
    
    def __init__(self, **kwargs: Any):
        """
        Initialize a new State object with initial values.
        
        Args:
            **kwargs: Initial state values as keyword arguments
        """
        self._data: Dict[str, Any] = {}
        self._observers: List[Callable[[Dict[str, Any]], None]] = []
        
        # Set initial values
        for key, value in kwargs.items():
            self._data[key] = value
    
    def __getattr__(self, name: str) -> Any:
        """
        Get a state value by attribute access.
        
        Args:
            name: The name of the state value
            
        Returns:
            The state value
            
        Raises:
            AttributeError: If the state value doesn't exist
        """
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        
        if name in self._data:
            return self._data[name]
        
        raise AttributeError(f"State has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set a state value by attribute access and notify observers.
        
        Args:
            name: The name of the state value
            value: The new value
        """
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        
        old_value = self._data.get(name)
        self._data[name] = value
        
        # Notify observers if value changed
        if old_value != value:
            self._notify_observers()
    
    def subscribe(self, observer: Callable[[Dict[str, Any]], None]) -> None:
        """
        Subscribe an observer function to state changes.
        
        Args:
            observer: A callback function that receives the state data
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable[[Dict[str, Any]], None]) -> None:
        """
        Unsubscribe an observer function from state changes.
        
        Args:
            observer: The observer function to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        """
        Notify all observers about state changes.
        """
        for observer in self._observers:
            observer(self._data.copy())
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a state value with an optional default.
        
        Args:
            key: The state key
            default: Default value if key doesn't exist
            
        Returns:
            The state value or default
        """
        return self._data.get(key, default)
    
    def update(self, **kwargs: Any) -> None:
        """
        Update multiple state values at once.
        
        Args:
            **kwargs: State values to update
        """
        changed = False
        for key, value in kwargs.items():
            if self._data.get(key) != value:
                self._data[key] = value
                changed = True
        
        if changed:
            self._notify_observers()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the state to a dictionary.
        
        Returns:
            A copy of the state data
        """
        return self._data.copy()
