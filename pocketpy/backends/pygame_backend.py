"""
Pygame rendering backend for PocketPy framework
"""

import pygame
from typing import Any, Dict, Optional, Tuple


class PygameBackend:
    """
    Pygame-based rendering backend for PocketPy.
    
    Handles window creation, event processing, and widget rendering.
    """
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "PocketPy App"):
        """
        Initialize the Pygame backend.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.title = title
        
        # Create window
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Font cache
        self.font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        
        # Running state
        self.running = False
    
    def get_font(self, family: str, size: int) -> pygame.font.Font:
        """
        Get or create a cached font.
        
        Args:
            family: Font family name (ignored for now, uses default)
            size: Font size in points
            
        Returns:
            Pygame Font object
        """
        key = (family, size)
        if key not in self.font_cache:
            self.font_cache[key] = pygame.font.Font(None, size)
        return self.font_cache[key]
    
    def parse_color(self, color_str: Optional[str]) -> Tuple[int, int, int]:
        """
        Parse hex color string to RGB tuple.
        
        Args:
            color_str: Hex color string like "#FF0000" or None
            
        Returns:
            RGB tuple (r, g, b)
        """
        if not color_str:
            return (255, 255, 255)
        
        # Remove # prefix
        color_str = color_str.lstrip('#')
        
        # Parse hex
        try:
            r = int(color_str[0:2], 16)
            g = int(color_str[2:4], 16)
            b = int(color_str[4:6], 16)
            return (r, g, b)
        except (ValueError, IndexError):
            return (255, 255, 255)
    
    def draw_widget(self, widget_data: Dict[str, Any], surface: pygame.Surface) -> None:
        """
        Draw a single widget based on its data dictionary.
        
        Args:
            widget_data: Widget description dictionary from build()
            surface: Pygame surface to draw on
        """
        widget_type = widget_data.get('type')
        
        # Draw based on widget type
        if widget_type == 'label':
            self.draw_label(widget_data, surface)
        elif widget_type == 'button':
            self.draw_button(widget_data, surface)
        elif widget_type in ('vbox', 'hbox'):
            self.draw_layout(widget_data, surface)
    
    def draw_label(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """
        Draw a label widget.
        
        Args:
            data: Label data dictionary
            surface: Pygame surface to draw on
        """
        x, y = data.get('position', (0, 0))
        text = data.get('text', '')
        font_size = data.get('font_size', 24)
        font_family = data.get('font_family', 'sans-serif')
        color = self.parse_color(data.get('color', '#000000'))
        
        # Get font
        font = self.get_font(font_family, font_size)
        
        # Render text with antialiasing
        text_surface = font.render(str(text), True, color)
        
        # Draw text
        surface.blit(text_surface, (x, y))
    
    def draw_button(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """
        Draw a button widget.
        
        Args:
            data: Button widget data
            surface: Pygame surface
        """
        text = str(data.get('text', ''))
        x, y = data.get('position', (0, 0))
        
        # Get padding
        padding = data.get('padding', (10, 20))
        if isinstance(padding, tuple):
            pad_v = padding[0] if len(padding) > 0 else 10
            pad_h = padding[1] if len(padding) > 1 else pad_v
        else:
            pad_v = pad_h = padding
        
        # Get colors
        bg_color = self.parse_color(data.get('background_color', '#007AFF'))
        text_color = self.parse_color(data.get('color', '#FFFFFF'))
        
        # Get font
        font_size = data.get('font_size', 14)
        font = self.get_font('sans-serif', font_size)
        
        # Render text to get size
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        
        # Calculate button size
        button_width = text_width + (pad_h * 2)
        button_height = text_height + (pad_v * 2)
        
        # Store bounds for hit testing (we'll add this to the data)
        data['_bounds'] = (x, y, button_width, button_height)
        
        # Draw shadow for depth
        shadow_offset = 2
        shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, button_width, button_height)
        pygame.draw.rect(surface, (150, 150, 150), shadow_rect, border_radius=8)
        
        # Draw button background with rounded corners
        button_rect = pygame.Rect(x, y, button_width, button_height)
        if not data.get('disabled', False):
            pygame.draw.rect(surface, bg_color, button_rect, border_radius=8)
        else:
            # Lighter color for disabled
            disabled_color = tuple(min(c + 50, 255) for c in bg_color)
            pygame.draw.rect(surface, disabled_color, button_rect, border_radius=8)
        
        # Draw button border
        border_color = tuple(max(c - 30, 0) for c in bg_color)
        pygame.draw.rect(surface, border_color, button_rect, 2, border_radius=8)
        
        # Draw text centered
        text_x = x + pad_h
        text_y = y + pad_v
        surface.blit(text_surface, (text_x, text_y))
    
    def draw_layout(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """
        Draw a layout container (VBox or HBox).
        
        Args:
            data: Layout widget data
            surface: Pygame surface
        """
        # Draw background if specified
        x, y = data.get('position', (0, 0))
        width = data.get('width')
        height = data.get('height')
        bg_color = data.get('background_color')
        
        if bg_color:
            # Calculate layout size if not specified
            if not width:
                width = self.width
            if not height:
                height = self.height
            
            color = self.parse_color(bg_color)
            pygame.draw.rect(surface, color, (x, y, width, height))
        
        # Draw all children
        children = data.get('children', [])
        for child in children:
            self.draw_widget(child, surface)
    
    def draw(self, root_widget_data: Dict[str, Any]) -> None:
        """
        Draw the entire widget tree.
        
        Args:
            root_widget_data: Root widget data dictionary
        """
        # Clear screen with light gray background
        self.screen.fill((245, 245, 247))
        
        # Draw widget tree
        self.draw_widget(root_widget_data, self.screen)
        
        # Update display
        pygame.display.flip()
    
    def hit_test(self, x: int, y: int, widget_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Perform hit testing to find which widget was clicked.
        
        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            widget_data: Widget data to test
            
        Returns:
            Widget data if hit, None otherwise
        """
        # Check if this widget has bounds
        bounds = widget_data.get('_bounds')
        if bounds:
            wx, wy, ww, wh = bounds
            if wx <= x <= wx + ww and wy <= y <= wy + wh:
                return widget_data
        
        # Check children (for layouts)
        children = widget_data.get('children', [])
        for child in reversed(children):  # Check top to bottom
            result = self.hit_test(x, y, child)
            if result:
                return result
        
        return None
    
    def handle_event(self, event: pygame.event.Event, root_widget_data: Dict[str, Any]) -> bool:
        """
        Handle a Pygame event.
        
        Args:
            event: Pygame event
            root_widget_data: Root widget data for hit testing
            
        Returns:
            True if should continue running, False to quit
        """
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                hit_widget = self.hit_test(x, y, root_widget_data)
                
                if hit_widget and hit_widget.get('type') == 'button':
                    # Call the button's on_press handler
                    on_press = hit_widget.get('on_press')
                    if on_press and callable(on_press):
                        on_press()
                        return True  # Trigger redraw
        
        return True
    
    def run(self, app_instance) -> None:
        """
        Run the main event loop.
        
        Args:
            app_instance: PocketPy App instance
        """
        self.running = True
        
        print(f"Pygame window opened: {self.width}x{self.height}")
        print("Click the buttons to interact!")
        
        while self.running:
            # Build UI tree ONCE per frame (important for callbacks!)
            if app_instance._root_widget:
                ui_tree = app_instance._root_widget.build()
            else:
                ui_tree = {}
            
            # Handle events using the SAME tree
            for event in pygame.event.get():
                should_continue = self.handle_event(event, ui_tree)
                if not should_continue:
                    self.running = False
                    break
            
            # Draw frame using the SAME tree
            if ui_tree:
                self.draw(ui_tree)
            
            # Cap FPS
            self.clock.tick(self.fps)
        
        # Cleanup
        pygame.quit()
        print("Pygame window closed.")
