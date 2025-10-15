# Getting Started with PocketPy

Welcome to PocketPy! This guide will help you build your first mobile app using our Python framework.

## Installation

```bash
# Install from PyPI (when available)
pip install pocket-py

# Or install from source
git clone https://github.com/xoity/pocket-py.git
cd pocket-py
pip install -e .
```

## Your First App in 5 Minutes

### Step 1: Import PocketPy

```python
from pocketpy import App, View, State, VBox, Label, Button
```

### Step 2: Create a View

A View defines what your screen looks like:

```python
class HelloView(View):
    def __init__(self):
        super().__init__()
        # Create reactive state
        self.message = State("Hello, PocketPy!")
    
    def body(self):
        # Define UI structure declaratively
        return VBox(
            children=[
                Label(text=self.message, font_size=24),
                Button(text="Click Me", on_press=self.on_button_click)
            ]
        )
    
    def on_button_click(self):
        self.message.value = "Button clicked!"
```

### Step 3: Run the App

```python
app = App(title="My First App")
app.set_view(HelloView)
app.run()
```

That's it! You've created your first PocketPy app.

## Understanding the Basics

### State - Reactive Data

`State` objects hold data that automatically updates the UI when changed:

```python
# Create state
self.counter = State(0)

# Use in UI
Label(text=self.counter)

# Update (UI automatically refreshes)
self.counter.value += 1
```

### Views - Screen Structure

Views use the MVVM pattern. The `body()` method returns your UI structure:

```python
class MyView(View):
    def body(self):
        return VBox(children=[
            Label(text="Title"),
            Button(text="Action")
        ])
```

### Widgets - UI Components

Widgets are the building blocks. PocketPy includes:

- **Label**: Display text
- **Button**: Clickable buttons
- **VBox**: Vertical layout
- **HBox**: Horizontal layout

### Styling

Style widgets using keyword arguments:

```python
Label(
    text="Styled Text",
    font_size=20,
    color="#007AFF",
    background_color="#F0F0F0",
    padding=(10, 20)
)
```

## Common Patterns

### Counter App

```python
class CounterView(View):
    def __init__(self):
        super().__init__()
        self.count = State(0)
    
    def increment(self):
        self.count.value += 1
    
    def body(self):
        return VBox(children=[
            Label(text=self.count, font_size=48),
            Button(text="Increment", on_press=self.increment)
        ])
```

### Form Input

```python
class FormView(View):
    def __init__(self):
        super().__init__()
        self.name = State("")
        self.email = State("")
    
    def submit(self):
        print(f"Name: {self.name.value}")
        print(f"Email: {self.email.value}")
    
    def body(self):
        return VBox(children=[
            Label(text="Name:"),
            # TextInput widget (to be implemented)
            Label(text="Email:"),
            # TextInput widget (to be implemented)
            Button(text="Submit", on_press=self.submit)
        ])
```

### Multiple Screens (Concept)

```python
class MainView(View):
    def __init__(self):
        super().__init__()
        self.current_screen = State("home")
    
    def navigate_to(self, screen):
        self.current_screen.value = screen
    
    def body(self):
        if self.current_screen.value == "home":
            return HomeScreen()
        elif self.current_screen.value == "settings":
            return SettingsScreen()
```

## Layout Strategies

### Vertical Stack

```python
VBox(
    children=[
        Label(text="Top"),
        Label(text="Middle"),
        Label(text="Bottom")
    ],
    spacing=10  # Space between items
)
```

### Horizontal Row

```python
HBox(
    children=[
        Button(text="Left"),
        Button(text="Center"),
        Button(text="Right")
    ],
    spacing=5
)
```

### Nested Layouts

```python
VBox(children=[
    Label(text="Header"),
    HBox(children=[
        Button(text="Button 1"),
        Button(text="Button 2")
    ]),
    Label(text="Footer")
])
```

## Event Handling

### Button Clicks

```python
def handle_click():
    print("Button clicked!")

Button(text="Click Me", on_press=handle_click)
```

### With Lambda

```python
Button(
    text="Increment",
    on_press=lambda: self.counter.value += 1
)
```

### With Parameters

```python
def set_value(value):
    self.data.value = value

Button(
    text="Set to 10",
    on_press=lambda: set_value(10)
)
```

## Best Practices

### 1. Organize Your Code

```python
# views/home_view.py
from pocketpy import View, VBox, Label

class HomeView(View):
    def body(self):
        return VBox(children=[
            Label(text="Home Screen")
        ])
```

### 2. Separate Business Logic

```python
# models/counter_model.py
class CounterModel:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1

# views/counter_view.py
class CounterView(View):
    def __init__(self):
        super().__init__()
        self.model = CounterModel()
        self.count = State(0)
```

### 3. Reusable Components

```python
def create_titled_button(title, on_press):
    return VBox(children=[
        Label(text=title, font_size=12),
        Button(text="Action", on_press=on_press)
    ])
```

### 4. Clean State Management

```python
# Good: Clear state changes
def update_user(self):
    self.username.value = "New Name"

# Avoid: Mutating objects directly
# self.user.name = "New Name"  # Won't trigger update
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` folder for complete apps
2. **Read Architecture**: See `ARCHITECTURE.md` for technical details
3. **Build Something**: Start with a simple counter or todo list
4. **Join Community**: Share your projects and get help

## Troubleshooting

### State Not Updating UI

Make sure you're setting `state.value`:

```python
# Correct
self.counter.value += 1

# Won't work
self.counter = self.counter.value + 1
```

### Widgets Not Showing

Ensure your View's `body()` method returns a widget:

```python
def body(self):
    return VBox(children=[...])  # Must return widget
```

### Import Errors

Check your imports are from `pocketpy`:

```python
from pocketpy import App, View, State
# Not from pocketpy.core or pocketpy.widgets
```

## Resources

- **Examples**: `examples/` folder
- **API Reference**: `ARCHITECTURE.md`
- **GitHub**: https://github.com/xoity/pocket-py
- **Issues**: https://github.com/xoity/pocket-py/issues

Happy coding with PocketPy! 🐍📱
