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
        elif widget_type in ('vbox', 'hbox', 'grid', 'stack'):
            self.draw_layout(widget_data, surface)
        elif widget_type == 'textinput':
            self.draw_textinput(widget_data, surface)
        elif widget_type == 'switch':
            self.draw_switch(widget_data, surface)
        elif widget_type == 'slider':
            self.draw_slider(widget_data, surface)
        elif widget_type == 'card':
            self.draw_card(widget_data, surface)
        elif widget_type == 'divider':
            self.draw_divider(widget_data, surface)
    
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
    
    def draw_textinput(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """Draw text input widget"""
        x, y = data.get('position', (0, 0))
        width = data.get('width', 200)
        height = data.get('height', 40)
        text = data.get('text', '')
        placeholder = data.get('placeholder', '')
        bg_color = self.parse_color(data.get('background_color', '#FFFFFF'))
        border_color = self.parse_color(data.get('border_color', '#C6C6C8'))
        text_color = self.parse_color(data.get('color', '#000000'))
        placeholder_color = self.parse_color(data.get('placeholder_color', '#8E8E93'))
        font_size = data.get('font_size', 16)
        is_focused = data.get('is_focused', False)
        padding = data.get('padding', (8, 12))
        pad_v, pad_h = padding if isinstance(padding, tuple) else (padding, padding)
        
        # Draw background
        pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=8)
        
        # Draw border (thicker if focused)
        border_width = 2 if is_focused else 1
        pygame.draw.rect(surface, border_color, (x, y, width, height), border_width, border_radius=8)
        
        # Draw text or placeholder
        font = self.get_font('sans-serif', font_size)
        display_text = text if text else placeholder
        color = text_color if text else placeholder_color
        
        if display_text:
            text_surface = font.render(display_text, True, color)
            text_x = x + pad_h
            text_y = y + (height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))
        
        # Store bounds
        data['_bounds'] = (x, y, width, height)
    
    def draw_switch(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """Draw switch toggle widget"""
        x, y = data.get('position', (0, 0))
        width = data.get('width', 51)
        height = data.get('height', 31)
        value = data.get('value', False)
        on_color = self.parse_color(data.get('on_color', '#34C759'))
        off_color = self.parse_color(data.get('off_color', '#C6C6C8'))
        thumb_color = self.parse_color(data.get('thumb_color', '#FFFFFF'))
        disabled = data.get('disabled', False)
        
        # Background
        bg_color = on_color if value else off_color
        if disabled:
            bg_color = tuple(min(c + 50, 255) for c in bg_color)
        
        pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=height//2)
        
        # Thumb position
        thumb_radius = (height - 4) // 2
        thumb_x = x + width - thumb_radius - 2 if value else x + thumb_radius + 2
        thumb_y = y + height // 2
        
        # Draw thumb shadow
        pygame.draw.circle(surface, (0, 0, 0, 30), (thumb_x + 1, thumb_y + 1), thumb_radius)
        
        # Draw thumb
        pygame.draw.circle(surface, thumb_color, (thumb_x, thumb_y), thumb_radius)
        
        # Store bounds
        data['_bounds'] = (x, y, width, height)
    
    def draw_slider(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """Draw slider widget"""
        x, y = data.get('position', (0, 0))
        width = data.get('width', 200)
        height = data.get('height', 4)
        percentage = data.get('percentage', 0.5)
        track_color = self.parse_color(data.get('track_color', '#C6C6C8'))
        active_color = self.parse_color(data.get('active_color', '#007AFF'))
        thumb_color = self.parse_color(data.get('thumb_color', '#FFFFFF'))
        
        track_y = y + 10
        
        # Draw track
        pygame.draw.rect(surface, track_color, (x, track_y, width, height), border_radius=2)
        
        # Draw active portion
        active_width = int(width * percentage)
        if active_width > 0:
            pygame.draw.rect(surface, active_color, (x, track_y, active_width, height), border_radius=2)
        
        # Draw thumb
        thumb_x = x + active_width
        thumb_y = track_y + height // 2
        thumb_radius = 10
        
        # Thumb shadow
        pygame.draw.circle(surface, (0, 0, 0, 50), (thumb_x + 1, thumb_y + 1), thumb_radius)
        
        # Thumb
        pygame.draw.circle(surface, thumb_color, (thumb_x, thumb_y), thumb_radius)
        pygame.draw.circle(surface, active_color, (thumb_x, thumb_y), thumb_radius - 2)
        
        # Store bounds
        data['_bounds'] = (x, y - 10, width, 30)
    
    def draw_card(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """Draw card widget"""
        x, y = data.get('position', (0, 0))
        width = data.get('width', 300)
        height = data.get('height', 200)
        bg_color = self.parse_color(data.get('background_color', '#FFFFFF'))
        border_radius = data.get('border_radius', 12)
        elevation = data.get('elevation', 'md')
        
        # Shadow based on elevation
        shadow_offsets = {'none': 0, 'sm': 2, 'md': 4, 'lg': 8, 'xl': 12}
        shadow_offset = shadow_offsets.get(elevation, 4)
        
        if shadow_offset > 0:
            shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, width, height)
            pygame.draw.rect(surface, (0, 0, 0, 30), shadow_rect, border_radius=border_radius)
        
        # Draw card
        pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=border_radius)
        
        # Draw border if specified
        border_color = data.get('border_color')
        border_width = data.get('border_width', 0)
        if border_color and border_width > 0:
            pygame.draw.rect(surface, self.parse_color(border_color), (x, y, width, height), border_width, border_radius=border_radius)
        
        # Draw children
        children = data.get('children', [])
        padding = data.get('padding', 16)
        pad = padding if isinstance(padding, int) else padding[0]
        
        for child in children:
            # Offset children by padding
            if 'position' in child:
                child_x, child_y = child['position']
                child['position'] = (x + pad, y + pad)
            self.draw_widget(child, surface)
    
    def draw_divider(self, data: Dict[str, Any], surface: pygame.Surface) -> None:
        """Draw divider line"""
        x, y = data.get('position', (0, 0))
        orientation = data.get('orientation', 'horizontal')
        thickness = data.get('thickness', 1)
        color = self.parse_color(data.get('color', '#E5E5EA'))
        length = data.get('length', self.width if orientation == 'horizontal' else self.height)
        
        if orientation == 'horizontal':
            pygame.draw.rect(surface, color, (x, y, length, thickness))
        else:
            pygame.draw.rect(surface, color, (x, y, thickness, length))
    
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
                
                if hit_widget:
                    widget_type = hit_widget.get('type')
                    
                    if widget_type == 'button' or widget_type == 'switch':
                        # Call the on_press handler
                        on_press = hit_widget.get('on_press')
                        if on_press and callable(on_press):
                            on_press()
                            return True  # Trigger redraw
                    
                    elif widget_type == 'slider':
                        # Handle slider click
                        on_drag = hit_widget.get('on_drag')
                        if on_drag and callable(on_drag):
                            bounds = hit_widget.get('_bounds', (0, 0, 200, 30))
                            slider_x = bounds[0]
                            slider_width = bounds[2]
                            relative_x = x - slider_x
                            on_drag(relative_x, slider_width)
                            return True
        
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
