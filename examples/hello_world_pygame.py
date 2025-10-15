"""
Hello World Example with Pygame Rendering

This example demonstrates PocketPy with actual graphical rendering:
- Opens a real window using Pygame
- Renders widgets visually
- Mouse clicks work on buttons
- Counter increments when you click the button
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketpy import App, View, State, VBox, Label, Button


class HelloWorldView(View):
    """A simple hello world view with a counter."""
    
    def __init__(self):
        super().__init__()
        # Create reactive state
        self.counter = State(0)
        self.message = State("Hello, PocketPy!")
    
    def increment(self):
        """Increment the counter."""
        self.counter.value += 1
        print(f"Counter incremented to: {self.counter.value}")
    
    def reset(self):
        """Reset the counter to zero."""
        self.counter.value = 0
        print("Counter reset to 0")
    
    def body(self):
        """Define the UI structure."""
        return VBox(
            children=[
                Label(
                    text=self.message,
                    font_size=24,
                    color="#333333",
                    padding=(20, 20)
                ),
                Label(
                    text=self.counter,
                    font_size=48,
                    color="#007AFF",
                    padding=(10, 20)
                ),
                Button(
                    text="Increment",
                    on_press=self.increment,
                    background_color="#007AFF",
                    padding=(12, 24)
                ),
                Button(
                    text="Reset",
                    on_press=self.reset,
                    background_color="#FF3B30",
                    padding=(12, 24)
                ),
            ],
            spacing=15,
            padding=(20, 20),
            background_color="#F5F5F5"
        )


def main():
    """Run the hello world app with Pygame rendering."""
    print("=" * 60)
    print("PocketPy - Hello World (Pygame Edition)")
    print("=" * 60)
    print()
    print("This example opens a graphical window.")
    print("Click the buttons to interact!")
    print()
    
    app = App(
        title="PocketPy - Hello World",
        use_pygame=True,
        width=600,
        height=400
    )
    app.set_view(HelloWorldView)
    app.run()


if __name__ == "__main__":
    main()
