# PocketPy Examples

This folder contains example applications built with PocketPy.

## Running Examples

To run any example, make sure you have PocketPy installed and run:

```bash
python hello_world.py
```

## Available Examples

### 1. Hello World (`hello_world.py`)

The simplest PocketPy app demonstrating:

- Basic View structure
- State management with reactive updates
- Button click handlers
- VBox layout container

### 2. Counter App (`counter_app.py`)

A more advanced example showing:

- Multiple State objects
- Complex layouts with HBox and VBox
- Dynamic styling
- Custom event handlers with lambda functions
- Step-based counter logic

## Creating Your Own App

Here's the basic structure of a PocketPy app:

```python
from pocketpy import App, View, State, VBox, Label, Button

class MyView(View):
    def __init__(self):
        super().__init__()
        # Create your state
        self.data = State("initial value")
    
    def body(self):
        # Define your UI declaratively
        return VBox(
            children=[
                Label(text=self.data),
                Button(text="Update", on_press=self.update_data)
            ]
        )
    
    def update_data(self):
        self.data.value = "new value"

# Run the app
app = App(title="My App")
app.set_view(MyView)
app.run()
```

## Key Concepts

### Declarative UI

PocketPy uses a declarative approach where you define what your UI should look like based on the current state:

```python
def body(self):
    return VBox(
        children=[
            Label(text="Hello"),
            Button(text="Click Me")
        ]
    )
```

### Reactive State

State objects automatically trigger UI updates when changed:

```python
self.counter = State(0)

def increment(self):
    self.counter.value += 1  # UI updates automatically!
```

### Styling

Style widgets using Pythonic keyword arguments:

```python
Button(
    text="Click Me",
    background_color="#007AFF",
    font_size=16,
    padding=(10, 20),
    width=200
)
```

### Layouts

Organize widgets with layout containers:

- **VBox**: Arranges children vertically
- **HBox**: Arranges children horizontally

```python
HBox(
    children=[
        Button(text="Left"),
        Button(text="Right")
    ],
    spacing=10
)
```

## Next Steps

- Explore the examples
- Modify them to learn how PocketPy works
- Create your own applications
- Check out the main README for API documentation
