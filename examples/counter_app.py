"""
Counter App Example for PocketPy

A more advanced example showing:
- Multiple State objects
- Dynamic text generation
- Button styling with hover effects
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketpy import App, View, State, VBox, HBox, Label, Button


class CounterView(View):
    """A counter app with increment and decrement buttons."""
    
    def __init__(self):
        super().__init__()
        self.count = State(0)
        self.step = State(1)
    
    def increment(self):
        """Increment counter by step value."""
        self.count.value += self.step.value
    
    def decrement(self):
        """Decrement counter by step value."""
        self.count.value -= self.step.value
    
    def reset(self):
        """Reset counter to zero."""
        self.count.value = 0
    
    def set_step(self, value):
        """Set the step value."""
        self.step.value = value
    
    def body(self):
        """Define the UI structure."""
        return VBox(
            children=[
                # Title
                Label(
                    text="Counter App",
                    font_size=32,
                    color="#1C1C1E",
                    text_align="center",
                    padding=(30, 20)
                ),
                
                # Counter display
                VBox(
                    children=[
                        Label(
                            text="Current Count:",
                            font_size=16,
                            color="#6E6E73",
                            text_align="center"
                        ),
                        Label(
                            text=self.count,
                            font_size=64,
                            color="#007AFF",
                            text_align="center",
                            padding=(10, 0)
                        ),
                    ],
                    background_color="#FFFFFF",
                    padding=(30, 20),
                    margin=(10, 10)
                ),
                
                # Control buttons
                HBox(
                    children=[
                        Button(
                            text="-",
                            on_press=self.decrement,
                            background_color="#FF3B30",
                            font_size=24,
                            width=80,
                            height=60
                        ),
                        Button(
                            text="+",
                            on_press=self.increment,
                            background_color="#34C759",
                            font_size=24,
                            width=80,
                            height=60
                        ),
                    ],
                    spacing=15,
                    padding=(20, 20)
                ),
                
                # Step size controls
                Label(
                    text="Step Size:",
                    font_size=14,
                    color="#6E6E73",
                    text_align="center",
                    padding=(10, 0)
                ),
                HBox(
                    children=[
                        Button(
                            text="1",
                            on_press=lambda: self.set_step(1),
                            background_color="#007AFF",
                            width=60,
                            height=40
                        ),
                        Button(
                            text="5",
                            on_press=lambda: self.set_step(5),
                            background_color="#007AFF",
                            width=60,
                            height=40
                        ),
                        Button(
                            text="10",
                            on_press=lambda: self.set_step(10),
                            background_color="#007AFF",
                            width=60,
                            height=40
                        ),
                    ],
                    spacing=10,
                    padding=(10, 20)
                ),
                
                # Reset button
                Button(
                    text="Reset",
                    on_press=self.reset,
                    background_color="#8E8E93",
                    width=200,
                    padding=(12, 0),
                    margin=(20, 0)
                ),
            ],
            spacing=10,
            background_color="#F2F2F7",
            padding=(0, 0)
        )


def main():
    """Run the counter app."""
    app = App(title="PocketPy - Counter App")
    app.set_view(CounterView)
    app.run()


if __name__ == "__main__":
    main()
