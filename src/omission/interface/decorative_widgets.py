"""
Reusable Widgets [Omission]
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton

class DecorativeButton(Button):
    """
    A decorative button.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.decorative()

class DecorativeLabel(Label):
    """
    A decorative label.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.decorative()

class DecorativeSpinner(Spinner):
    """
    A decorative spinner.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.decorative()

#pylint: disable=R0901
class DecorativeToggleButton(ToggleButton):
    """
    A decorative toggle button.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.decorative()

class PassageLabel(Label):
    """
    A decorative label.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.passage()
