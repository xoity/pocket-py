"""
Advanced layout widgets: Grid, Stack, Spacer, Divider
"""

from typing import Optional, List
from pocketpy.widgets.base import Widget


class Grid(Widget):
    """
    A grid layout container.
    
    Example:
        >>> grid = Grid(
        ...     columns=3,
        ...     spacing=16,
        ...     children=[Label("1"), Label("2"), Label("3"), Label("4")]
        ... )
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        columns: int = 2,
        rows: Optional[int] = None,
        spacing: int = 8,
        column_spacing: Optional[int] = None,
        row_spacing: Optional[int] = None,
        padding: int | tuple = 0,
        background_color: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a Grid layout.
        
        Args:
            children: Child widgets
            columns: Number of columns
            rows: Number of rows (auto if None)
            spacing: Spacing between cells
            column_spacing: Horizontal spacing (overrides spacing)
            row_spacing: Vertical spacing (overrides spacing)
            padding: Internal padding
            background_color: Background color
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.children = children or []
        self.columns = columns
        self.rows = rows
        self.spacing = spacing
        self.column_spacing = column_spacing if column_spacing is not None else spacing
        self.row_spacing = row_spacing if row_spacing is not None else spacing
        self.grid_padding = padding
        self.background_color = background_color
    
    def build(self) -> dict:
        """Build the grid's visual representation"""
        built_children = [child.build() for child in self.children]
        
        return {
            "type": "grid",
            "children": built_children,
            "columns": self.columns,
            "rows": self.rows,
            "column_spacing": self.column_spacing,
            "row_spacing": self.row_spacing,
            "padding": self.grid_padding,
            "background_color": self.background_color,
            "width": self.width,
            "height": self.height,
            "margin": self.margin,
            "position": (self.x, self.y)
        }


class Stack(Widget):
    """
    A stack layout (Z-index layering).
    
    Children are rendered on top of each other.
    
    Example:
        >>> stack = Stack(
        ...     children=[
        ...         Image(src="bg.png"),
        ...         Label("Overlay Text")
        ...     ],
        ...     alignment="center"
        ... )
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        alignment: str = "center",  # "center", "top-left", "top-right", etc.
        **kwargs
    ):
        """
        Initialize a Stack layout.
        
        Args:
            children: Child widgets (rendered bottom to top)
            alignment: How to align children
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.children = children or []
        self.alignment = alignment
    
    def build(self) -> dict:
        """Build the stack's visual representation"""
        built_children = [child.build() for child in self.children]
        
        return {
            "type": "stack",
            "children": built_children,
            "alignment": self.alignment,
            "width": self.width,
            "height": self.height,
            "margin": self.margin,
            "position": (self.x, self.y)
        }


class Spacer(Widget):
    """
    A flexible spacer for layouts.
    
    Example:
        >>> # Push elements to opposite ends
        >>> HBox(children=[
        ...     Button("Left"),
        ...     Spacer(),
        ...     Button("Right")
        ... ])
    """
    
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        flex: int = 1,
        **kwargs
    ):
        """
        Initialize a Spacer.
        
        Args:
            width: Fixed width (None for flexible)
            height: Fixed height (None for flexible)
            flex: Flex ratio for flexible sizing
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.spacer_width = width
        self.spacer_height = height
        self.flex = flex
    
    def build(self) -> dict:
        """Build the spacer's visual representation"""
        return {
            "type": "spacer",
            "width": self.spacer_width,
            "height": self.spacer_height,
            "flex": self.flex,
            "position": (self.x, self.y)
        }


class Divider(Widget):
    """
    A horizontal or vertical divider line.
    
    Example:
        >>> VBox(children=[
        ...     Label("Section 1"),
        ...     Divider(),
        ...     Label("Section 2")
        ... ])
    """
    
    def __init__(
        self,
        orientation: str = "horizontal",  # "horizontal" or "vertical"
        thickness: int = 1,
        color: str = "#E5E5EA",
        length: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize a Divider.
        
        Args:
            orientation: "horizontal" or "vertical"
            thickness: Line thickness in pixels
            color: Line color
            length: Line length (None for full width/height)
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.orientation = orientation
        self.thickness = thickness
        self.divider_color = color
        self.length = length
    
    def build(self) -> dict:
        """Build the divider's visual representation"""
        return {
            "type": "divider",
            "orientation": self.orientation,
            "thickness": self.thickness,
            "color": self.divider_color,
            "length": self.length,
            "margin": self.margin,
            "position": (self.x, self.y)
        }


class ScrollView(Widget):
    """
    A scrollable container.
    
    Example:
        >>> scroll = ScrollView(
        ...     child=VBox(children=[...many items...]),
        ...     height=400
        ... )
    """
    
    def __init__(
        self,
        child: Optional[Widget] = None,
        scroll_direction: str = "vertical",  # "vertical", "horizontal", "both"
        show_scrollbar: bool = True,
        **kwargs
    ):
        """
        Initialize a ScrollView.
        
        Args:
            child: Child widget to make scrollable
            scroll_direction: Scroll direction
            show_scrollbar: Whether to show scrollbar
            **kwargs: Additional styling properties
        """
        super().__init__(**kwargs)
        
        self.child = child
        self.scroll_direction = scroll_direction
        self.show_scrollbar = show_scrollbar
        
        self._scroll_offset_x = 0
        self._scroll_offset_y = 0
    
    def scroll(self, dx: int, dy: int) -> None:
        """Scroll by delta"""
        self._scroll_offset_x += dx
        self._scroll_offset_y += dy
        self._trigger_rebuild()
    
    def build(self) -> dict:
        """Build the scroll view's visual representation"""
        built_child = self.child.build() if self.child else {}
        
        return {
            "type": "scrollview",
            "child": built_child,
            "scroll_direction": self.scroll_direction,
            "show_scrollbar": self.show_scrollbar,
            "scroll_offset": (self._scroll_offset_x, self._scroll_offset_y),
            "width": self.width,
            "height": self.height,
            "margin": self.margin,
            "position": (self.x, self.y),
            "on_scroll": self.scroll
        }
