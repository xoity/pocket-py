"""
Todo App Demo
A complete todo list application showcasing PocketPy framework
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pocketpy import (
    App, View, State, Theme,
    VBox, HBox, Card, Spacer, Divider,
    Label, Button, TextInput, Switch
)


class TodoItem:
    """Todo item data class"""
    def __init__(self, text: str, completed: bool = False):
        self.text = text
        self.completed = State(completed)


class TodoAppView(View):
    """Beautiful todo list application"""
    
    def __init__(self):
        super().__init__()
        
        # State
        self.todos: list[TodoItem] = [
            TodoItem("Build mobile framework", True),
            TodoItem("Add beautiful widgets", True),
            TodoItem("Create demo apps", False),
            TodoItem("Deploy to production", False),
        ]
        self.new_todo_text = State("")
        self.filter_completed = State(False)
        self.refresh = State(0)  # Trigger rebuilds
    
    def add_todo(self):
        """Add a new todo"""
        text = self.new_todo_text.value.strip()
        if text:
            self.todos.append(TodoItem(text))
            self.new_todo_text.value = ""
            self.refresh.value += 1
            print(f"✅ Added todo: {text}")
    
    def toggle_todo(self, todo: TodoItem):
        """Toggle todo completion"""
        todo.completed.value = not todo.completed.value
        status = "completed" if todo.completed.value else "incomplete"
        print(f"📝 Todo '{todo.text}' marked as {status}")
    
    def delete_todo(self, todo: TodoItem):
        """Delete a todo"""
        self.todos.remove(todo)
        self.refresh.value += 1
        print(f"🗑️  Deleted todo: {todo.text}")
    
    def get_visible_todos(self):
        """Get todos based on filter"""
        if self.filter_completed.value:
            return [t for t in self.todos if t.completed.value]
        return self.todos
    
    def get_stats(self):
        """Get todo statistics"""
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t.completed.value)
        remaining = total - completed
        return total, completed, remaining
    
    def body(self):
        total, completed, remaining = self.get_stats()
        visible_todos = self.get_visible_todos()
        
        # Build todo item cards
        todo_cards = []
        for todo in visible_todos:
            todo_card = Card(
                children=[
                    HBox(
                        children=[
                            # Checkbox (switch)
                            Switch(
                                value=todo.completed,
                                on_change=lambda val, t=todo: self.toggle_todo(t)
                            ),
                            
                            # Todo text
                            Label(
                                text=todo.text,
                                font_size=16,
                                color="#8E8E93" if todo.completed.value else "#000000"
                            ),
                            
                            Spacer(),
                            
                            # Delete button
                            Button(
                                text="Delete",
                                font_size=14,
                                background_color="#FF3B30",
                                on_press=lambda t=todo: self.delete_todo(t)
                            )
                        ],
                        spacing=12
                    )
                ],
                elevation="sm",
                padding=16,
                margin=(8, 0)
            )
            todo_cards.append(todo_card)
        
        return VBox(
            children=[
                # Header
                Card(
                    children=[
                        Label(
                            text="📝 Todo App",
                            font_size=32,
                            color="#007AFF"
                        ),
                        Label(
                            text=f"{remaining} remaining • {completed} completed",
                            font_size=14,
                            color="#8E8E93"
                        )
                    ],
                    elevation="lg",
                    padding=20
                ),
                
                # Add todo section
                Card(
                    children=[
                        Label(
                            text="Add New Todo",
                            font_size=18,
                            color="#000000"
                        ),
                        TextInput(
                            value=self.new_todo_text,
                            placeholder="What needs to be done?",
                            font_size=16,
                            on_submit=lambda text: self.add_todo()
                        ),
                        Button(
                            text="Add Todo",
                            font_size=16,
                            background_color="#34C759",
                            on_press=self.add_todo
                        )
                    ],
                    elevation="md",
                    padding=16,
                    margin=(12, 0)
                ),
                
                # Filter section
                Card(
                    children=[
                        HBox(
                            children=[
                                Label(
                                    text="Show Completed Only",
                                    font_size=14,
                                    color="#3C3C43"
                                ),
                                Spacer(),
                                Switch(
                                    value=self.filter_completed,
                                    on_change=lambda val: setattr(self.refresh, 'value', self.refresh.value + 1)
                                )
                            ],
                            spacing=12
                        )
                    ],
                    elevation="sm",
                    padding=12,
                    margin=(12, 0)
                ),
                
                Divider(),
                
                # Todo list
                *todo_cards,
                
                # Empty state
                Label(
                    text="No todos to show" if not visible_todos else "",
                    font_size=16,
                    color="#8E8E93"
                ) if not visible_todos else Spacer(),
                
                # Footer
                Label(
                    text="Built with PocketPy Framework",
                    font_size=12,
                    color="#8E8E93"
                )
            ],
            spacing=12,
            padding=16
        )


if __name__ == "__main__":
    # Create app with beautiful theme
    theme = Theme.light()
    
    app = App(
        title="Todo App - PocketPy",
        use_pygame=True,
        theme=theme,
        width=500,
        height=900
    )
    
    app.set_view(TodoAppView)
    
    print("📝 Todo App - PocketPy Framework")
    print("=" * 50)
    print("✨ Features:")
    print("  • Add and delete todos")
    print("  • Mark todos as complete")
    print("  • Filter completed todos")
    print("  • Real-time statistics")
    print("  • Beautiful card-based UI")
    print("=" * 50)
    print("\n🚀 Opening todo app...\n")
    
    app.run()
    
    print("\n✅ Todo app closed!")
