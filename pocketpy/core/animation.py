"""
Animation system for PocketPy framework
"""

import math
import time
from typing import Callable, Optional, Any
from dataclasses import dataclass


class Easing:
    """Easing functions for smooth animations"""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing (no acceleration)"""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease in (accelerating from zero velocity)"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease out (decelerating to zero velocity)"""
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease in and out"""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease in"""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease out"""
        t -= 1
        return t * t * t + 1
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease in and out"""
        if t < 0.5:
            return 4 * t * t * t
        t = 2 * t - 2
        return 1 + t * t * t / 2
    
    @staticmethod
    def ease_in_quart(t: float) -> float:
        """Quartic ease in"""
        return t * t * t * t
    
    @staticmethod
    def ease_out_quart(t: float) -> float:
        """Quartic ease out"""
        t -= 1
        return 1 - t * t * t * t
    
    @staticmethod
    def ease_in_out_quart(t: float) -> float:
        """Quartic ease in and out"""
        if t < 0.5:
            return 8 * t * t * t * t
        t -= 1
        return 1 - 8 * t * t * t * t
    
    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease in"""
        return 0 if t == 0 else math.pow(2, 10 * (t - 1))
    
    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease out"""
        return 1 if t == 1 else 1 - math.pow(2, -10 * t)
    
    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        """Exponential ease in and out"""
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return math.pow(2, 20 * t - 10) / 2
        return (2 - math.pow(2, -20 * t + 10)) / 2
    
    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Bounce ease out"""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def ease_out_elastic(t: float) -> float:
        """Elastic ease out"""
        if t == 0 or t == 1:
            return t
        return math.pow(2, -10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1
    
    @staticmethod
    def spring(t: float, damping: float = 0.5) -> float:
        """Spring physics simulation"""
        return 1 - math.exp(-damping * t) * math.cos(10 * t)


@dataclass
class AnimationState:
    """State of an ongoing animation"""
    start_time: float
    duration: float
    start_value: float
    end_value: float
    easing: Callable[[float], float]
    on_update: Callable[[float], None]
    on_complete: Optional[Callable[[], None]] = None
    
    def get_current_value(self) -> float:
        """Calculate current value based on elapsed time"""
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        
        # Apply easing
        eased_progress = self.easing(progress)
        
        # Interpolate value
        current_value = self.start_value + (self.end_value - self.start_value) * eased_progress
        
        return current_value
    
    def is_complete(self) -> bool:
        """Check if animation is complete"""
        elapsed = time.time() - self.start_time
        return elapsed >= self.duration


class AnimationController:
    """
    Controls and manages animations.
    
    Example:
        >>> controller = AnimationController()
        >>> 
        >>> def update_opacity(value):
        ...     widget.opacity = value
        >>> 
        >>> controller.animate(
        ...     from_value=0.0,
        ...     to_value=1.0,
        ...     duration=0.3,
        ...     easing=Easing.ease_out_cubic,
        ...     on_update=update_opacity
        ... )
    """
    
    def __init__(self):
        """Initialize animation controller"""
        self.active_animations: list[AnimationState] = []
    
    def animate(
        self,
        from_value: float,
        to_value: float,
        duration: float,
        easing: Callable[[float], float] = Easing.ease_in_out_cubic,
        on_update: Optional[Callable[[float], None]] = None,
        on_complete: Optional[Callable[[], None]] = None
    ) -> AnimationState:
        """
        Start a new animation.
        
        Args:
            from_value: Starting value
            to_value: Ending value
            duration: Duration in seconds
            easing: Easing function
            on_update: Callback with current value
            on_complete: Callback when animation completes
            
        Returns:
            AnimationState object
        """
        anim = AnimationState(
            start_time=time.time(),
            duration=duration,
            start_value=from_value,
            end_value=to_value,
            easing=easing,
            on_update=on_update or (lambda x: None),
            on_complete=on_complete
        )
        
        self.active_animations.append(anim)
        return anim
    
    def update(self) -> None:
        """Update all active animations"""
        completed = []
        
        for anim in self.active_animations:
            if anim.is_complete():
                # Final update with end value
                anim.on_update(anim.end_value)
                
                # Call completion callback
                if anim.on_complete:
                    anim.on_complete()
                
                completed.append(anim)
            else:
                # Update with current value
                current_value = anim.get_current_value()
                anim.on_update(current_value)
        
        # Remove completed animations
        for anim in completed:
            self.active_animations.remove(anim)
    
    def cancel_all(self) -> None:
        """Cancel all active animations"""
        self.active_animations.clear()
    
    def has_active_animations(self) -> bool:
        """Check if there are active animations"""
        return len(self.active_animations) > 0


class Transition:
    """
    Predefined transition animations.
    
    Example:
        >>> # Fade in
        >>> Transition.fade_in(widget, duration=0.3)
        >>> 
        >>> # Slide in from right
        >>> Transition.slide_in(widget, direction="right", duration=0.4)
    """
    
    @staticmethod
    def fade_in(widget: Any, duration: float = 0.3, controller: Optional[AnimationController] = None):
        """Fade in animation"""
        if controller is None:
            controller = AnimationController()
        
        def update(value):
            widget.opacity = value
        
        controller.animate(0.0, 1.0, duration, Easing.ease_out_cubic, update)
        return controller
    
    @staticmethod
    def fade_out(widget: Any, duration: float = 0.3, controller: Optional[AnimationController] = None):
        """Fade out animation"""
        if controller is None:
            controller = AnimationController()
        
        def update(value):
            widget.opacity = value
        
        controller.animate(1.0, 0.0, duration, Easing.ease_in_cubic, update)
        return controller
    
    @staticmethod
    def scale_in(widget: Any, duration: float = 0.3, controller: Optional[AnimationController] = None):
        """Scale in animation"""
        if controller is None:
            controller = AnimationController()
        
        def update(value):
            widget.scale = value
        
        controller.animate(0.0, 1.0, duration, Easing.ease_out_back, update)
        return controller
    
    @staticmethod
    def slide_in(widget: Any, direction: str = "right", distance: int = 300, duration: float = 0.4, 
                 controller: Optional[AnimationController] = None):
        """Slide in animation"""
        if controller is None:
            controller = AnimationController()
        
        original_x = widget.x
        start_x = original_x + distance if direction == "left" else original_x - distance
        
        def update(value):
            widget.x = int(value)
        
        controller.animate(start_x, original_x, duration, Easing.ease_out_cubic, update)
        return controller


# Ease out back for spring-like effect
def ease_out_back(t: float, overshoot: float = 1.70158) -> float:
    """Ease out with back (overshoot)"""
    t -= 1
    return t * t * ((overshoot + 1) * t + overshoot) + 1

Easing.ease_out_back = staticmethod(ease_out_back)
