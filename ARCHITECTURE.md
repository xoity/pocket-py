# PocketPy Development Guide

## Architecture Overview

PocketPy follows the MVVM (Model-View-ViewModel) architectural pattern with a declarative UI approach.

### Core Components

1. **State** (`pocketpy.core.state`)
   - Observable data container
   - Automatically notifies listeners on value changes
   - Core of the reactive system

2. **View** (`pocketpy.core.app`)
   - Base class for screen definitions
   - Implements `body()` method that returns Widget tree
   - Similar to SwiftUI Views or React Components

3. **App** (`pocketpy.core.app`)
   - Main application controller
   - Manages lifecycle and event loop
   - Initializes rendering backend

4. **Widget** (`pocketpy.widgets.base`)
   - Base class for all UI components
   - Handles mounting/unmounting
   - Subscribes to State changes
   - Implements `build()` method

### Widget Lifecycle

``` bash
Widget Created
    ↓
mount() - Attached to UI tree
    ↓
build() - Rendered to screen
    ↓
State Change → Rebuild
    ↓
unmount() - Removed from UI tree
```

### Data Flow

``` bash
State.value changed
    ↓
Notify listeners
    ↓
Widget._trigger_rebuild()
    ↓
Widget.build()
    ↓
UI Update
```

## Creating Custom Widgets

```python
from pocketpy.widgets.base import Widget
from pocketpy.core.state import State

class CustomButton(Widget):
    def __init__(self, label, on_click, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.on_click = on_click
        
        # Watch state if label is a State object
        if isinstance(label, State):
            self.watch(label)
    
    def build(self):
        return {
            "type": "custom_button",
            "label": self.label.value if isinstance(self.label, State) else self.label,
            "position": (self.x, self.y),
            "width": self.width,
            "height": self.height,
            "background_color": self.background_color,
            "on_click": self.on_click
        }
```

## Creating Custom Layouts

```python
from pocketpy.widgets.base import Widget

class GridLayout(Widget):
    def __init__(self, columns=2, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
    
    def build(self):
        # Calculate grid positions
        for i, child in enumerate(self.children):
            row = i // self.columns
            col = i % self.columns
            child.x = self.x + (col * child.width)
            child.y = self.y + (row * child.height)
        
        return {
            "type": "grid",
            "columns": self.columns,
            "children": [child.build() for child in self.children]
        }
```

## State Management Patterns

### Simple State

```python
class MyView(View):
    def __init__(self):
        super().__init__()
        self.name = State("John")
```

### Computed Values

```python
class MyView(View):
    def __init__(self):
        super().__init__()
        self.first_name = State("John")
        self.last_name = State("Doe")
    
    @property
    def full_name(self):
        return f"{self.first_name.value} {self.last_name.value}"
```

### State Observers

```python
def __init__(self):
    super().__init__()
    self.count = State(0)
    
    # Subscribe to changes
    def on_count_change():
        print(f"Count changed to {self.count.value}")
    
    self.count.subscribe(on_count_change)
```

## Best Practices

1. **Keep Views Simple**: Views should only describe UI structure
2. **Logic in Methods**: Put business logic in view methods, not in `body()`
3. **Immutable State Updates**: Always set `state.value`, don't mutate objects
4. **Component Reusability**: Create custom widgets for reusable components
5. **Meaningful Names**: Use descriptive names for state and methods

## Future Roadmap

- [ ] Rendering backend (Pygame/Kivy/SDL)
- [ ] Gesture recognizers
- [ ] Animations
- [ ] Navigation system
- [ ] Platform-specific widgets
- [ ] Hot reload
- [ ] DevTools
- [ ] Testing utilities

## Contributing

PocketPy is in early development. Contributions are welcome!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pocketpy.git
cd pocketpy

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black pocketpy
```

## API Reference

### Core Classes

#### `State(initial_value)`

Observable data container.

**Methods:**

- `subscribe(listener)`: Add a change listener
- `value` (property): Get/set the current value

#### `View`

Base class for declarative views.

**Methods:**

- `body()`: Must return a Widget tree

#### `App(title, **kwargs)`

Main application class.

**Methods:**

- `set_view(view_class)`: Set the root view
- `run()`: Start the app
- `stop()`: Stop the app

#### `Widget(**kwargs)`

Base class for UI components.

**Common Properties:**

- `width`, `height`: Dimensions
- `background_color`: Hex color string
- `padding`: (vertical, horizontal) tuple
- `margin`: (vertical, horizontal) tuple

**Methods:**

- `build()`: Return visual representation (override in subclasses)
- `mount()`: Called when added to UI tree
- `unmount()`: Called when removed from UI tree
- `watch(state)`: Subscribe to state changes

### Built-in Widgets

#### `Label(text, **kwargs)`

Text display widget.

**Properties:**

- `text`: String or State object
- `font_size`: Integer
- `font_family`: String
- `color`: Hex color
- `text_align`: 'left', 'center', 'right'

#### `Button(text, on_press, **kwargs)`

Clickable button widget.

**Properties:**

- `text`: String or State object
- `on_press`: Callback function
- `font_size`: Integer
- `disabled`: Boolean

### Layout Containers

#### `VBox(children, **kwargs)`

Vertical layout container.

**Properties:**

- `children`: List of widgets
- `spacing`: Space between children
- `alignment`: 'start', 'center', 'end', 'stretch'

#### `HBox(children, **kwargs)`

Horizontal layout container.

**Properties:**

- `children`: List of widgets
- `spacing`: Space between children
- `alignment`: 'start', 'center', 'end', 'stretch'
