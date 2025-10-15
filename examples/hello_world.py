"""
Hello World Example for PocketPy

This example demonstrates the basics of building a PocketPy app:
- Creating a View with declarative UI
- Using State for reactive updates
- Using layouts (VBox) to arrange widgets
- Handling button clicks
"""

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
    
    def reset(self):
        """Reset the counter to zero."""
        self.counter.value = 0
    
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
    """Run the hello world app."""
    app = App(title="PocketPy - Hello World")
    app.set_view(HelloWorldView)
    app.run()


if __name__ == "__main__":
    main()
