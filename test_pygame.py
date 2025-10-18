"""
Test Pygame Backend

Quick test to verify the Pygame backend is working.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pocketpy import App, View, State, VBox, Label, Button


class TestView(View):
    def __init__(self):
        super().__init__()
        self.counter = State(0)
    
    def increment(self):
        self.counter.value += 1
        print(f"Count: {self.counter.value}")
    
    def body(self):
        return VBox(children=[
            Label(text=self.counter, font_size=64, color="#000000"),
            Button(
                text="Increment",
                font_size=20,
                on_press=lambda: setattr(self.counter, 'value', self.counter.value + 1)
            )
        ])


if __name__ == "__main__":
    app = App(title="Pygame Test", use_pygame=True, width=400, height=300)
    app.set_view(TestView)
    
    print("Opening Pygame window...")
    print("Click the button to increment the counter!")
    print("Close the window to exit.")
    print()
    
    app.run()
    
    print("Test complete!")
