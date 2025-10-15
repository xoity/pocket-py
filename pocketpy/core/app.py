"""
Main App class for PocketPy framework
"""

from typing import Optional, Any


class App:
    """
    Main application class for PocketPy mobile framework.
    
    This class serves as the entry point for your mobile application.
    It manages the application lifecycle and orchestrates the UI rendering.
    
    Example:
        >>> app = App(title="My App")
        >>> app.run()
    """
    
    def __init__(self, title: str = "PocketPy App", **kwargs: Any):
        """
        Initialize a new PocketPy application.
        
        Args:
            title: The title of the application
            **kwargs: Additional configuration options
        """
        self.title = title
        self.config = kwargs
        self._root_widget: Optional[Any] = None
        self._is_running = False
    
    def set_root(self, widget: Any) -> None:
        """
        Set the root widget for the application.
        
        Args:
            widget: The root widget to display
        """
        self._root_widget = widget
    
    def run(self) -> None:
        """
        Start the application main loop.
        """
        if self._is_running:
            raise RuntimeError("Application is already running")
        
        self._is_running = True
        print(f"Starting {self.title}...")
        
        # TODO: Implement main application loop
        # This will handle events, rendering, and state updates
        
    def stop(self) -> None:
        """
        Stop the application.
        """
        self._is_running = False
        print(f"Stopping {self.title}...")
