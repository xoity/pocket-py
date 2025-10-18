# PocketPy Rendering Backends

## Pygame Backend

The Pygame backend provides actual graphical rendering for PocketPy applications.

### Features

- ✅ Opens a native OS window
- ✅ Renders widgets (Label, Button, VBox, HBox)
- ✅ Mouse click handling with hit-testing
- ✅ Reactive state updates trigger visual refreshes
- ✅ 60 FPS rendering
- ✅ Font rendering with size control
- ✅ Color support (hex colors)
- ✅ Button hover effects (planned)

### Installation

```bash
pip install pygame
```

### Usage

```python
from pocketpy import App, View, State, VBox, Label, Button

class MyView(View):
    def __init__(self):
        super().__init__()
        self.counter = State(0)
    
    def body(self):
        return VBox(children=[
            Label(text=self.counter, font_size=48),
            Button(
                text="Click Me",
                on_press=lambda: setattr(self.counter, 'value', self.counter.value + 1)
            )
        ])

# Enable Pygame rendering
app = App(
    title="My App",
    use_pygame=True,  # This enables Pygame backend
    width=800,
    height=600
)
app.set_view(MyView)
app.run()
```

### How It Works

1. **Initialization**: Creates a Pygame window with specified dimensions
2. **Event Loop**: Processes mouse clicks, keyboard input, and window events at 60 FPS
3. **Rendering**: Traverses the widget tree and renders each widget:
   - Labels: Renders text with specified font and color
   - Buttons: Draws rectangles with text and borders
   - Layouts: Arranges children and draws backgrounds
4. **Hit Testing**: When mouse is clicked, finds which button was clicked based on position
5. **Event Dispatch**: Calls the appropriate `on_press` handler for clicked buttons
6. **State Updates**: When state changes, rebuilds and redraws the UI tree

### API

#### PygameBackend

```python
PygameBackend(width=800, height=600, title="PocketPy App")
```

**Parameters:**

- `width`: Window width in pixels (default: 800)
- `height`: Window height in pixels (default: 600)
- `title`: Window title string

**Methods:**

- `run(app_instance)`: Start the event loop
- `draw(widget_tree)`: Render a widget tree
- `hit_test(x, y, widget_tree)`: Find widget at position

### Widget Rendering

#### Labels

- Renders text at position with specified font size and color
- Supports State objects for reactive text

#### Buttons

- Draws filled rectangle with border
- Renders centered text
- Calculates size based on text + padding
- Stores bounds for click detection
- Supports disabled state (grayed out)

#### Layouts (VBox/HBox)

- Renders background color if specified
- Recursively renders all children
- Respects spacing between children

### Limitations (Current)

- No scroll containers yet
- No text input widgets yet
- No images or custom graphics
- No animations
- Hit testing only works for buttons (not labels or layouts)
- Font family ignored (uses default system font)
- No retina/high-DPI scaling yet

### Future Enhancements

- [ ] TextInput widget
- [ ] Image widget
- [ ] ScrollView container
- [ ] Gesture recognition
- [ ] Animations and transitions
- [ ] Custom font loading
- [ ] High-DPI/retina support
- [ ] Better layout measurement
- [ ] Hover effects
- [ ] Focus management
- [ ] Keyboard navigation

### Examples

See the `examples/` folder:

- `hello_world_pygame.py` - Interactive counter with graphical rendering
- `test_pygame.py` - Simple button click test

### Performance

- Runs at 60 FPS
- Full redraw each frame (no dirty region optimization yet)
- Font caching to avoid re-creating fonts
- Simple hit-testing algorithm (tree traversal)

### Debugging

The backend prints useful information:

```
Pygame window opened: 800x600
Click the buttons to interact!
```

Button clicks also print to console:

```
Counter incremented to: 1
Counter incremented to: 2
```

### Console Mode Fallback

If Pygame is not installed, the app automatically falls back to console mode:

```python
app = App(title="My App", use_pygame=True)
# If pygame not found:
# Warning: Pygame not installed. Install with: pip install pygame
# Falling back to console mode...
```

## Other Backends (Future)

### Kivy Backend (Planned)

- Native mobile support (iOS/Android)
- Touch gesture recognition
- Better mobile widgets

### SDL2 Backend (Planned)

- Lower-level graphics control
- Better performance
- GPU acceleration

### Native Bridges (Planned)

- Direct iOS UIKit integration
- Direct Android Views integration
- Platform-specific look and feel

## Creating Custom Backends

To create a custom backend, implement a class with:

```python
class MyBackend:
    def __init__(self, width, height, title):
        # Initialize your rendering system
        pass
    
    def run(self, app_instance):
        # Run event loop
        while running:
            # 1. Handle events
            # 2. Build UI tree: ui_tree = app_instance._root_widget.build()
            # 3. Render UI tree: self.draw(ui_tree)
            # 4. Dispatch clicks: call widget['on_press']()
        pass
    
    def draw(self, widget_tree):
        # Render the widget tree
        pass
```

Then use it:

```python
app._backend = MyBackend(800, 600, "My App")
app._backend.run(app)
```

## Troubleshooting

**Window doesn't open:**

- Check that Pygame is installed: `pip install pygame`
- Verify you set `use_pygame=True` in App constructor

**Clicks don't work:**

- Ensure buttons have `on_press` callbacks
- Check console for error messages
- Verify button is visible (not off-screen)

**Text not rendering:**

- Check font_size is reasonable (>0, <200)
- Verify color is valid hex string ("#RRGGBB")

**Window closes immediately:**

- Check for exceptions in console
- Ensure view's `body()` returns a valid widget

---

**Ready to build real graphical apps!** 🎨🖱️
