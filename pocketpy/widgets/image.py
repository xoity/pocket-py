"""
Image widget for displaying images
"""

from typing import Optional
from pocketpy.widgets.base import Widget


class Image(Widget):
    """
    An image display widget.
    
    Example:
        >>> image = Image(
        ...     src="path/to/image.png",
        ...     width=200,
        ...     height=150,
        ...     fit="cover"
        ... )
    """
    
    def __init__(
        self,
        src: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fit: str = "contain",  # "contain", "cover", "fill", "scale-down"
        border_radius: int = 0,
        opacity: float = 1.0,
        **kwargs
    ):
        """
        Initialize an Image widget.
        
        Args:
            src: Image source path or URL
            width: Image width
            height: Image height
            fit: How to fit image in container
            border_radius: Corner radius
            opacity: Image opacity (0.0 to 1.0)
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.src = src
        self.img_width = width
        self.img_height = height
        self.fit = fit
        self.border_radius = border_radius
        self.opacity = opacity
        
        self._image_loaded = False
        self._image_surface = None
    
    def build(self) -> dict:
        """Build the image's visual representation"""
        return {
            "type": "image",
            "src": self.src,
            "width": self.img_width or self.width or 100,
            "height": self.img_height or self.height or 100,
            "fit": self.fit,
            "border_radius": self.border_radius,
            "opacity": self.opacity,
            "margin": self.margin,
            "position": (self.x, self.y),
            "_image_surface": self._image_surface
        }
