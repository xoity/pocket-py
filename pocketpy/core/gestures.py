"""
Gesture recognition system for PocketPy framework
"""

import time
from typing import Optional, Callable, Tuple
from dataclasses import dataclass
from enum import Enum


class GestureType(Enum):
    """Types of gestures"""
    TAP = "tap"
    DOUBLE_TAP = "double_tap"
    LONG_PRESS = "long_press"
    SWIPE = "swipe"
    DRAG = "drag"
    PINCH = "pinch"


class SwipeDirection(Enum):
    """Swipe directions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class GestureEvent:
    """Gesture event data"""
    gesture_type: GestureType
    position: Tuple[int, int]
    velocity: Optional[Tuple[float, float]] = None
    direction: Optional[SwipeDirection] = None
    distance: Optional[float] = None
    scale: Optional[float] = None
    duration: Optional[float] = None


class GestureRecognizer:
    """
    Recognizes touch and mouse gestures.
    
    Example:
        >>> recognizer = GestureRecognizer()
        >>> recognizer.on_tap = lambda event: print("Tapped!")
        >>> recognizer.on_swipe = lambda event: print(f"Swiped {event.direction}")
        >>> 
        >>> # In event loop:
        >>> recognizer.handle_mouse_down(x, y)
        >>> recognizer.handle_mouse_move(x, y)
        >>> recognizer.handle_mouse_up(x, y)
    """
    
    def __init__(
        self,
        tap_threshold: int = 10,
        long_press_duration: float = 0.5,
        double_tap_interval: float = 0.3,
        swipe_threshold: int = 50,
        swipe_velocity_threshold: float = 100.0
    ):
        """
        Initialize gesture recognizer.
        
        Args:
            tap_threshold: Max movement distance for tap (pixels)
            long_press_duration: Duration for long press (seconds)
            double_tap_interval: Max interval for double tap (seconds)
            swipe_threshold: Min distance for swipe (pixels)
            swipe_velocity_threshold: Min velocity for swipe (pixels/second)
        """
        self.tap_threshold = tap_threshold
        self.long_press_duration = long_press_duration
        self.double_tap_interval = double_tap_interval
        self.swipe_threshold = swipe_threshold
        self.swipe_velocity_threshold = swipe_velocity_threshold
        
        # Callbacks
        self.on_tap: Optional[Callable[[GestureEvent], None]] = None
        self.on_double_tap: Optional[Callable[[GestureEvent], None]] = None
        self.on_long_press: Optional[Callable[[GestureEvent], None]] = None
        self.on_swipe: Optional[Callable[[GestureEvent], None]] = None
        self.on_drag: Optional[Callable[[GestureEvent], None]] = None
        self.on_drag_start: Optional[Callable[[GestureEvent], None]] = None
        self.on_drag_end: Optional[Callable[[GestureEvent], None]] = None
        
        # State tracking
        self._is_pressed = False
        self._press_start_pos: Optional[Tuple[int, int]] = None
        self._press_start_time: Optional[float] = None
        self._current_pos: Optional[Tuple[int, int]] = None
        self._last_tap_time: Optional[float] = None
        self._last_tap_pos: Optional[Tuple[int, int]] = None
        self._is_dragging = False
        self._long_press_triggered = False
    
    def handle_mouse_down(self, x: int, y: int) -> None:
        """Handle mouse button down event"""
        self._is_pressed = True
        self._press_start_pos = (x, y)
        self._current_pos = (x, y)
        self._press_start_time = time.time()
        self._is_dragging = False
        self._long_press_triggered = False
    
    def handle_mouse_move(self, x: int, y: int) -> None:
        """Handle mouse move event"""
        if not self._is_pressed or self._press_start_pos is None:
            return
        
        self._current_pos = (x, y)
        
        # Calculate distance from start
        dx = x - self._press_start_pos[0]
        dy = y - self._press_start_pos[1]
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Check if this is a drag
        if distance > self.tap_threshold and not self._is_dragging:
            self._is_dragging = True
            
            if self.on_drag_start:
                event = GestureEvent(
                    gesture_type=GestureType.DRAG,
                    position=(x, y)
                )
                self.on_drag_start(event)
        
        # Continue drag
        if self._is_dragging and self.on_drag:
            event = GestureEvent(
                gesture_type=GestureType.DRAG,
                position=(x, y),
                distance=distance
            )
            self.on_drag(event)
    
    def handle_mouse_up(self, x: int, y: int) -> None:
        """Handle mouse button up event"""
        if not self._is_pressed or self._press_start_pos is None or self._press_start_time is None:
            return
        
        self._is_pressed = False
        duration = time.time() - self._press_start_time
        
        # Calculate movement
        dx = x - self._press_start_pos[0]
        dy = y - self._press_start_pos[1]
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Drag end
        if self._is_dragging:
            if self.on_drag_end:
                event = GestureEvent(
                    gesture_type=GestureType.DRAG,
                    position=(x, y),
                    distance=distance,
                    duration=duration
                )
                self.on_drag_end(event)
            
            self._is_dragging = False
            return
        
        # Check for swipe
        if distance > self.swipe_threshold:
            velocity = distance / duration if duration > 0 else 0
            
            if velocity > self.swipe_velocity_threshold:
                # Determine direction
                direction = self._get_swipe_direction(dx, dy)
                
                if self.on_swipe:
                    event = GestureEvent(
                        gesture_type=GestureType.SWIPE,
                        position=(x, y),
                        velocity=(dx / duration, dy / duration) if duration > 0 else (0, 0),
                        direction=direction,
                        distance=distance
                    )
                    self.on_swipe(event)
                return
        
        # Check for tap (small movement)
        if distance <= self.tap_threshold:
            current_time = time.time()
            
            # Check for double tap
            if (self._last_tap_time is not None and 
                self._last_tap_pos is not None and
                current_time - self._last_tap_time <= self.double_tap_interval):
                
                # Check if taps are close together
                tap_dx = x - self._last_tap_pos[0]
                tap_dy = y - self._last_tap_pos[1]
                tap_distance = (tap_dx * tap_dx + tap_dy * tap_dy) ** 0.5
                
                if tap_distance <= self.tap_threshold:
                    if self.on_double_tap:
                        event = GestureEvent(
                            gesture_type=GestureType.DOUBLE_TAP,
                            position=(x, y)
                        )
                        self.on_double_tap(event)
                    
                    # Reset tap tracking
                    self._last_tap_time = None
                    self._last_tap_pos = None
                    return
            
            # Single tap
            if self.on_tap:
                event = GestureEvent(
                    gesture_type=GestureType.TAP,
                    position=(x, y)
                )
                self.on_tap(event)
            
            # Track for double tap
            self._last_tap_time = current_time
            self._last_tap_pos = (x, y)
    
    def update(self, dt: float) -> None:
        """Update gesture state (call each frame)"""
        if not self._is_pressed or self._press_start_time is None:
            return
        
        # Check for long press
        duration = time.time() - self._press_start_time
        
        if (duration >= self.long_press_duration and 
            not self._long_press_triggered and 
            not self._is_dragging):
            
            self._long_press_triggered = True
            
            if self.on_long_press and self._current_pos:
                event = GestureEvent(
                    gesture_type=GestureType.LONG_PRESS,
                    position=self._current_pos,
                    duration=duration
                )
                self.on_long_press(event)
    
    def _get_swipe_direction(self, dx: float, dy: float) -> SwipeDirection:
        """Determine swipe direction from delta"""
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        
        if abs_dx > abs_dy:
            return SwipeDirection.RIGHT if dx > 0 else SwipeDirection.LEFT
        else:
            return SwipeDirection.DOWN if dy > 0 else SwipeDirection.UP
    
    def reset(self) -> None:
        """Reset gesture state"""
        self._is_pressed = False
        self._press_start_pos = None
        self._press_start_time = None
        self._current_pos = None
        self._is_dragging = False
        self._long_press_triggered = False
