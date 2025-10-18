"""
Main App class for PocketPy framework
"""

from typing import Optional, Any, Type
from abc import ABC


class View(ABC):
    """
    Base class for declarative views in MVVM pattern.
    
    Example:
        >>> class MyView(View):
        ...     def __init__(self):
        ...         self.counter = State(0)
        ...     
        ...     def body(self):
        ...         return VBox(children=[
        ...             Label(text=self.counter),
        ...             Button(
        ...                 text="Increment",
        ...                 on_press=lambda: setattr(self.counter, 'value', self.counter.value + 1)
        ...             )
        ...         ])
    """
    
    def body(self):
        """
        Define the UI structure for this view.
        
        Must return a Widget that represents the view's layout.
        """
        raise NotImplementedError("Subclasses must implement body()")


class App:
    """
    Main application class for PocketPy mobile framework.
    
    This class serves as the entry point for your mobile application.
    It manages the application lifecycle and orchestrates the UI rendering.
    
    Example:
        >>> app = App(title="My App")
        >>> app.set_view(MyView)
        >>> app.run()
    """
    
    def __init__(
        self,
        title: str = "PocketPy App",
        use_pygame: bool = False,
        theme: Optional[Any] = None,
        width: int = 800,
        height: int = 600,
        **kwargs: Any
    ):
        """
        Initialize a new PocketPy application.
        
        Args:
            title: The title of the application
            use_pygame: Whether to use Pygame rendering backend
            theme: Theme configuration (defaults to light theme)
            width: Window width in pixels
            height: Window height in pixels
            **kwargs: Additional configuration options
        """
        self.title = title
        self.config = kwargs
        self.width = width
        self.height = height
        self._view: Optional[View] = None
        self._root_widget: Optional[Any] = None
        self._is_running = False
        self._window = None
        self._use_pygame = use_pygame
        self._backend = None
        
        # Theme support
        if theme is None:
            from pocketpy.core.theme import Theme
            self.theme = Theme.light()
        else:
            self.theme = theme
    
    def set_view(self, view_class: Type[View]) -> None:
        """
        Set the root view for the application.
        
        Args:
            view_class: A View class (not an instance) to use as the root
        """
        self._view = view_class()
        self._root_widget = self._view.body()
        
        # Mount the widget tree
        if self._root_widget:
            self._root_widget.mount()
    
    def set_root(self, widget: Any) -> None:
        """
        Set the root widget for the application directly.
        
        Args:
            widget: The root widget to display
        """
        self._root_widget = widget
        if self._root_widget:
            self._root_widget.mount()
    
    def run(self) -> None:
        """
        Start the application main loop.
        """
        if self._is_running:
            raise RuntimeError("Application is already running")
        
        if not self._root_widget:
            raise RuntimeError("No view or root widget set. Call set_view() or set_root() first.")
        
        self._is_running = True
        
        # Use Pygame backend if requested
        if self._use_pygame:
            try:
                from pocketpy.backends.pygame_backend import PygameBackend
                self._backend = PygameBackend(
                    width=self.config.get('width', 800),
                    height=self.config.get('height', 600),
                    title=self.title
                )
                self._backend.run(self)
                return
            except ImportError:
                print("Warning: Pygame not installed. Install with: pip install pygame")
                print("Falling back to console mode...")
        
        # Console mode (original behavior)
        print(f"Starting {self.title}...")
        print(f"Root widget: {self._root_widget}")
        
        # Build the initial UI tree
        ui_tree = self._root_widget.build()
        print(f"UI Tree: {ui_tree}")
        
        # TODO: Initialize rendering backend (Pygame, Kivy, or custom)
        # TODO: Implement main application loop
        # This will handle events, rendering, and state updates
        
        self._main_loop()
    
    def _main_loop(self) -> None:
        """
        The main application event loop.
        """
        # TODO: Implement proper event loop
        # For now, just a placeholder
        print("Main loop started. Press Ctrl+C to exit.")
        try:
            import time
            while self._is_running:
                time.sleep(0.016)  # ~60 FPS
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self) -> None:
        """
        Stop the application.
        """
        self._is_running = False
        
        # Unmount the widget tree
        if self._root_widget:
            self._root_widget.unmount()
        
        print(f"Stopping {self.title}...")
