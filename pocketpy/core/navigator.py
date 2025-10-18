"""
Navigation and routing system for PocketPy framework
"""

from typing import Optional, Dict, Callable, Any, List
from pocketpy.core.app import View
from pocketpy.core.animation import AnimationController, Easing


class Route:
    """
    A route in the navigation stack.
    
    Example:
        >>> route = Route(name="home", view_class=HomeView, params={"user_id": 123})
    """
    
    def __init__(
        self,
        name: str,
        view_class: type[View],
        params: Optional[Dict[str, Any]] = None,
        transition: str = "slide"
    ):
        """
        Initialize a route.
        
        Args:
            name: Route name/identifier
            view_class: View class to instantiate
            params: Parameters to pass to view
            transition: Transition animation type
        """
        self.name = name
        self.view_class = view_class
        self.params = params or {}
        self.transition = transition
        self._view_instance: Optional[View] = None
    
    def get_view(self) -> View:
        """Get or create view instance"""
        if self._view_instance is None:
            self._view_instance = self.view_class()
            
            # Set params as attributes
            for key, value in self.params.items():
                setattr(self._view_instance, key, value)
        
        return self._view_instance


class Navigator:
    """
    Navigation controller for managing view stack and transitions.
    
    Example:
        >>> nav = Navigator()
        >>> nav.register_route("home", HomeView)
        >>> nav.register_route("details", DetailsView)
        >>> 
        >>> # Navigate
        >>> nav.push("details", params={"item_id": 42})
        >>> 
        >>> # Go back
        >>> nav.pop()
    """
    
    def __init__(self, animation_controller: Optional[AnimationController] = None):
        """
        Initialize navigator.
        
        Args:
            animation_controller: Animation controller for transitions
        """
        self.routes: Dict[str, type[View]] = {}
        self.stack: List[Route] = []
        self.animation_controller = animation_controller or AnimationController()
        
        # Callbacks
        self.on_navigate: Optional[Callable[[Route], None]] = None
        self.on_back: Optional[Callable[[], None]] = None
    
    def register_route(
        self,
        name: str,
        view_class: type[View],
        transition: str = "slide"
    ) -> None:
        """
        Register a route.
        
        Args:
            name: Route name
            view_class: View class
            transition: Default transition type
        """
        self.routes[name] = view_class
    
    def push(
        self,
        route_name: str,
        params: Optional[Dict[str, Any]] = None,
        transition: Optional[str] = None
    ) -> bool:
        """
        Push a new route onto the stack.
        
        Args:
            route_name: Name of route to navigate to
            params: Parameters to pass to view
            transition: Transition animation (overrides default)
            
        Returns:
            True if navigation successful
        """
        if route_name not in self.routes:
            print(f"Warning: Route '{route_name}' not found")
            return False
        
        view_class = self.routes[route_name]
        route = Route(
            name=route_name,
            view_class=view_class,
            params=params,
            transition=transition or "slide"
        )
        
        self.stack.append(route)
        
        if self.on_navigate:
            self.on_navigate(route)
        
        return True
    
    def pop(self) -> bool:
        """
        Pop the current route from the stack.
        
        Returns:
            True if pop successful
        """
        if len(self.stack) <= 1:
            return False
        
        self.stack.pop()
        
        if self.on_back:
            self.on_back()
        
        return True
    
    def pop_to_root(self) -> None:
        """Pop all routes except the root"""
        if len(self.stack) > 1:
            self.stack = [self.stack[0]]
            
            if self.on_back:
                self.on_back()
    
    def replace(
        self,
        route_name: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Replace current route with a new one.
        
        Args:
            route_name: Name of route to navigate to
            params: Parameters to pass to view
            
        Returns:
            True if successful
        """
        if not self.stack:
            return self.push(route_name, params)
        
        if route_name not in self.routes:
            return False
        
        view_class = self.routes[route_name]
        route = Route(
            name=route_name,
            view_class=view_class,
            params=params
        )
        
        self.stack[-1] = route
        
        if self.on_navigate:
            self.on_navigate(route)
        
        return True
    
    def get_current_route(self) -> Optional[Route]:
        """Get the current route"""
        return self.stack[-1] if self.stack else None
    
    def get_current_view(self) -> Optional[View]:
        """Get the current view"""
        route = self.get_current_route()
        return route.get_view() if route else None
    
    def can_pop(self) -> bool:
        """Check if we can go back"""
        return len(self.stack) > 1
    
    def get_stack_depth(self) -> int:
        """Get current navigation stack depth"""
        return len(self.stack)


class NavigationBar(View):
    """
    A navigation bar widget with title and back button.
    
    Example:
        >>> nav_bar = NavigationBar(
        ...     title="Settings",
        ...     show_back=True,
        ...     on_back=navigator.pop
        ... )
    """
    
    def __init__(
        self,
        title: str = "",
        show_back: bool = False,
        on_back: Optional[Callable[[], None]] = None,
        background_color: str = "#F8F8F8",
        text_color: str = "#000000"
    ):
        """
        Initialize navigation bar.
        
        Args:
            title: Title text
            show_back: Whether to show back button
            on_back: Back button callback
            background_color: Bar background color
            text_color: Text color
        """
        super().__init__()
        
        self.title = title
        self.show_back = show_back
        self.on_back = on_back
        self.background_color = background_color
        self.text_color = text_color
    
    def body(self) -> dict:
        """Build navigation bar"""
        return {
            "type": "navigationbar",
            "title": self.title,
            "show_back": self.show_back,
            "on_back": self.on_back,
            "background_color": self.background_color,
            "text_color": self.text_color,
            "height": 44
        }
