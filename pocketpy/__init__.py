"""
PocketPy - A modern Python mobile framework with beautiful UI components
"""

__version__ = "0.2.0"
__author__ = "PocketPy Team"
__email__ = "team@pocketpy.dev"

# Core components
from pocketpy.core.app import App, View
from pocketpy.core.state import State
from pocketpy.core.theme import Theme, ColorScheme, Typography, Spacing, Shadows
from pocketpy.core.animation import AnimationController, Easing, Transition
from pocketpy.core.gestures import GestureRecognizer, GestureEvent, GestureType, SwipeDirection
from pocketpy.core.navigator import Navigator, Route, NavigationBar

# Base widget
from pocketpy.widgets.base import Widget

# Basic widgets
from pocketpy.widgets.label import Label
from pocketpy.widgets.button import Button
from pocketpy.widgets.textinput import TextInput
from pocketpy.widgets.image import Image
from pocketpy.widgets.switch import Switch
from pocketpy.widgets.slider import Slider
from pocketpy.widgets.card import Card

# Layout widgets
from pocketpy.layout.vbox import VBox
from pocketpy.layout.hbox import HBox
from pocketpy.layout.advanced import Grid, Stack, Spacer, Divider, ScrollView

__all__ = [
    # Core
    "App",
    "View",
    "State",
    "Theme",
    "ColorScheme",
    "Typography",
    "Spacing",
    "Shadows",
    "AnimationController",
    "Easing",
    "Transition",
    "GestureRecognizer",
    "GestureEvent",
    "GestureType",
    "SwipeDirection",
    "Navigator",
    "Route",
    "NavigationBar",
    
    # Widgets
    "Widget",
    "Label",
    "Button",
    "TextInput",
    "Image",
    "Switch",
    "Slider",
    "Card",
    
    # Layouts
    "VBox",
    "HBox",
    "Grid",
    "Stack",
    "Spacer",
    "Divider",
    "ScrollView",
]
