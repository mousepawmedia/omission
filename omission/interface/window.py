"""
User Interface [Omission]
"""

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from omission.scores.score_loader import ScoreLoader
from omission.interface.game import Gameplay
from omission.interface.menu import Menu
from omission.interface.popup import PopupLabel
#from omission.interface.rules import Rules
#from omission.interface.credits import Credits

kivy.require('1.10.0')

class OmissionWindow(FloatLayout):
    """
    Parent class for the app. Most of the callback functions needed by the
    application will need to go here, so they can be accessed by any
    Kivy widget via `root.whatever()`
    """

    def __init__(self, **kwargs):
        """
        Initialize a new OmissionWindow.
        """
        super().__init__(**kwargs)

        self.menu = Menu()
        self.show_menu()

    def show_menu(self, to_remove=None):
        """
        Show the main menu.
        """
        if to_remove:
            self.remove_widget(to_remove)
        menu = Menu()
        self.add_widget(menu)

    def start_game(self, settings, to_remove=None):
        """
        Start a new game.
        """
        if to_remove:
            self.remove_widget(to_remove)
        gameplay = Gameplay()
        gameplay.set_settings(settings)
        self.add_widget(gameplay)
        gameplay.play()

    def popup_score(self, message):
        """
        Add a popup to a random location on the screen.
        """
        # Create a new popup.
        popup = PopupLabel()
        # Set the message.
        popup.text = message
        # Set a random location for the popup.
        popup.random_location(self.width, self.height)
        # Set the popup size.
        popup.set_size(4)
        # Add the widget.
        self.add_widget(popup)

    def popup_key(self, message):
        """
        Add a popup to a random location on the screen.
        """
        # Create a new popup.
        popup = PopupLabel()
        # Set the message.
        popup.text = message
        # Set a random location for the popup.
        popup.random_location(self.width, self.height)
        # Set the popup size.
        popup.set_size(3)
        # Add the widget.
        self.add_widget(popup)


class OmissionApp(App):
    """
   Application-level class, builds the application
   """

    def __init__(self, **kwargs):
        """
        Initialize a new OmissionWindow.
        """
        super().__init__(**kwargs)
        self.kill_callback = None
        self.min_size = (800, 600)

        # Create our score loader.
        self.scoreloader = ScoreLoader()

    def build_config(self, config):
        """
       Configure the application.
       """

        # Prevent the window from resizing too small. (SDL2 windows only).
        Config.set('graphics', 'minimum_width', self.min_size[0])
        Config.set('graphics', 'minimum_height', self.min_size[1])
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        # Prevent exit on ESC
        Config.set('kivy', 'exit_on_escape', '0')

    def build(self):
        """
        This function starts the application by constructing
        it from widgets and properties.
        """

        # Set the title and icon.
        self.title = "Omission"
        #self.icon = "icons/app/elements_icon_512.png"

        # Create the window.
        omission_app = OmissionWindow()

        # Bind the resize event.
        Window.bind(on_resize=self.check_resize)

        # Return the application.
        return omission_app

    def check_resize(self, instance, new_x, new_y):
        """
        Prevent resizing our screen too small if we're not using SDL2.
        If we resize too small, it will snap back to the minimum size.
        """
        # pylint: disable=W0613
        # Prevent resizing X too small...
        if new_x < self.min_size[0]:
            Window.size = (self.min_size[0], Window.size[1])
        # Prevent resizing Y too small..
        if new_y < self.min_size[1]:
            Window.size = (Window.size[0], self.min_size[1])

    def set_kill_callback(self, callback):
        """
        Ensures the callback is called when the application is set to stop.
        Overwrites old kill callbacks.
        """
        self.kill_callback = callback

    def on_stop(self):
        """
        The application is about to stop.
        """
        if self.kill_callback:
            self.kill_callback()
        self.scoreloader.write_out()
