"""
Theme system for PocketPy framework

Provides color schemes, typography, spacing, and styling constants
for building beautiful, consistent UIs.
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ColorScheme:
    """Color scheme for light or dark mode"""
    
    # Primary colors
    primary: str = "#007AFF"
    primary_dark: str = "#0051D5"
    primary_light: str = "#4DA6FF"
    
    # Secondary colors
    secondary: str = "#5856D6"
    secondary_dark: str = "#3634A3"
    secondary_light: str = "#8B8AE8"
    
    # Semantic colors
    success: str = "#34C759"
    warning: str = "#FF9500"
    error: str = "#FF3B30"
    info: str = "#5AC8FA"
    
    # Grayscale
    background: str = "#F2F2F7"
    surface: str = "#FFFFFF"
    card: str = "#FFFFFF"
    border: str = "#C6C6C8"
    divider: str = "#E5E5EA"
    
    # Text colors
    text_primary: str = "#000000"
    text_secondary: str = "#3C3C43"
    text_tertiary: str = "#8E8E93"
    text_disabled: str = "#C7C7CC"
    
    # Interactive states
    hover: str = "#F2F2F7"
    active: str = "#E5E5EA"
    focus: str = "#007AFF"
    disabled_bg: str = "#E5E5EA"
    
    # Overlay colors
    overlay: str = "#00000050"
    shadow: str = "#00000020"


@dataclass
class Typography:
    """Typography scale and font definitions"""
    
    # Font families
    font_primary: str = "sans-serif"
    font_secondary: str = "serif"
    font_monospace: str = "monospace"
    
    # Font sizes
    size_xs: int = 12
    size_sm: int = 14
    size_md: int = 16
    size_lg: int = 18
    size_xl: int = 24
    size_2xl: int = 32
    size_3xl: int = 48
    size_4xl: int = 64
    
    # Font weights (for future use)
    weight_light: int = 300
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700
    
    # Line heights
    line_height_tight: float = 1.2
    line_height_normal: float = 1.5
    line_height_relaxed: float = 1.75


@dataclass
class Spacing:
    """Spacing scale for consistent layouts"""
    
    # Base spacing unit (in pixels)
    unit: int = 8
    
    # Spacing values
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    xxxl: int = 64
    
    # Specific use cases
    padding_button: Tuple[int, int] = (12, 24)
    padding_card: int = 16
    padding_screen: int = 20
    
    margin_small: int = 8
    margin_medium: int = 16
    margin_large: int = 24
    
    # Border radius
    radius_sm: int = 4
    radius_md: int = 8
    radius_lg: int = 12
    radius_xl: int = 16
    radius_full: int = 9999


@dataclass
class Shadows:
    """Shadow definitions for depth and elevation"""
    
    # Shadow colors (RGBA)
    shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 25)
    
    # Shadow offsets (x, y, blur)
    shadow_sm: Tuple[int, int, int] = (0, 1, 2)
    shadow_md: Tuple[int, int, int] = (0, 2, 4)
    shadow_lg: Tuple[int, int, int] = (0, 4, 8)
    shadow_xl: Tuple[int, int, int] = (0, 8, 16)
    shadow_2xl: Tuple[int, int, int] = (0, 12, 24)


@dataclass
class Animation:
    """Animation timing and easing configurations"""
    
    # Duration in milliseconds
    duration_fast: int = 150
    duration_normal: int = 300
    duration_slow: int = 500
    
    # Easing functions (for reference)
    easing_linear: str = "linear"
    easing_ease_in: str = "ease-in"
    easing_ease_out: str = "ease-out"
    easing_ease_in_out: str = "ease-in-out"
    easing_spring: str = "spring"


class Theme:
    """
    Complete theme configuration for PocketPy apps.
    
    Supports both light and dark modes with comprehensive styling options.
    
    Example:
        >>> theme = Theme.light()
        >>> app = App(theme=theme)
        
        >>> # Dark mode
        >>> dark_theme = Theme.dark()
        >>> app = App(theme=dark_theme)
        
        >>> # Custom theme
        >>> custom_colors = ColorScheme(primary="#FF6B6B", background="#1A1A1A")
        >>> custom_theme = Theme(colors=custom_colors)
    """
    
    def __init__(
        self,
        colors: Optional[ColorScheme] = None,
        typography: Optional[Typography] = None,
        spacing: Optional[Spacing] = None,
        shadows: Optional[Shadows] = None,
        animation: Optional[Animation] = None,
        mode: str = "light"
    ):
        """
        Initialize a theme.
        
        Args:
            colors: Color scheme (defaults to light mode)
            typography: Typography configuration
            spacing: Spacing configuration
            shadows: Shadow configuration
            animation: Animation configuration
            mode: Theme mode ("light" or "dark")
        """
        self.mode = mode
        self.colors = colors or ColorScheme()
        self.typography = typography or Typography()
        self.spacing = spacing or Spacing()
        self.shadows = shadows or Shadows()
        self.animation = animation or Animation()
    
    @classmethod
    def light(cls) -> "Theme":
        """Create a light theme (iOS-inspired)"""
        colors = ColorScheme(
            primary="#007AFF",
            background="#F2F2F7",
            surface="#FFFFFF",
            card="#FFFFFF",
            text_primary="#000000",
            text_secondary="#3C3C43",
            border="#C6C6C8"
        )
        return cls(colors=colors, mode="light")
    
    @classmethod
    def dark(cls) -> "Theme":
        """Create a dark theme (iOS-inspired)"""
        colors = ColorScheme(
            primary="#0A84FF",
            primary_dark="#006DD9",
            primary_light="#409CFF",
            background="#000000",
            surface="#1C1C1E",
            card="#2C2C2E",
            border="#38383A",
            divider="#3A3A3C",
            text_primary="#FFFFFF",
            text_secondary="#EBEBF5",
            text_tertiary="#EBEBF599",
            text_disabled="#545456",
            hover="#2C2C2E",
            active="#3A3A3C",
            disabled_bg="#3A3A3C",
            overlay="#000000AA",
            shadow="#00000040"
        )
        return cls(colors=colors, mode="dark")
    
    @classmethod
    def material(cls) -> "Theme":
        """Create a Material Design theme"""
        colors = ColorScheme(
            primary="#6200EE",
            primary_dark="#3700B3",
            primary_light="#BB86FC",
            secondary="#03DAC6",
            secondary_dark="#018786",
            secondary_light="#66FFF9",
            background="#FFFFFF",
            surface="#FFFFFF",
            error="#B00020",
            text_primary="#000000DE",
            text_secondary="#00000099",
            text_tertiary="#00000061"
        )
        
        spacing = Spacing(
            padding_button=(10, 16),
            radius_sm=4,
            radius_md=4,
            radius_lg=8
        )
        
        return cls(colors=colors, spacing=spacing, mode="light")
    
    @classmethod
    def material_dark(cls) -> "Theme":
        """Create a Material Design dark theme"""
        colors = ColorScheme(
            primary="#BB86FC",
            primary_dark="#3700B3",
            primary_light="#E1BEE7",
            secondary="#03DAC6",
            background="#121212",
            surface="#1E1E1E",
            card="#2C2C2C",
            border="#424242",
            text_primary="#FFFFFF",
            text_secondary="#FFFFFFB3",
            text_tertiary="#FFFFFF80"
        )
        
        return cls(colors=colors, mode="dark")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple.
        
        Args:
            hex_color: Hex color string like "#FF0000"
            
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgba_to_tuple(self, hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
        """
        Convert hex color to RGBA tuple.
        
        Args:
            hex_color: Hex color string
            alpha: Alpha value (0-255)
            
        Returns:
            RGBA tuple (r, g, b, a)
        """
        r, g, b = self.hex_to_rgb(hex_color)
        return (r, g, b, alpha)


# Default themes
DEFAULT_LIGHT_THEME = Theme.light()
DEFAULT_DARK_THEME = Theme.dark()
