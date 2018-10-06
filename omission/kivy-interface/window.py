"""
User Interface [Omission]
"""

# This is needed to force use of SDL2 for audio, needed for Windows and
# for Snapcraft.
import os
os.environ['KIVY_AUDIO'] = 'sdl2'

# Workaround for https://github.com/kivy/kivy/issues/3576 and https://github.com/kivy/kivy/issues/5476
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')

#pylint: disable=C0413

import os.path

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from omission.data.data_loader import DataLoader
from omission.interface.credits import Credits
from omission.interface.game import Gameplay
from omission.interface.highscore import Highscore
from omission.interface.menu import Menu
from omission.interface.popup import PopupLabel
from omission.interface.rules import Rules

# We need this imported, just to ensure it is seen by the .kv file
# pylint: disable=W0401,W0614
from omission.interface.decorative_widgets import *

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

        self.show_menu()
        #self.show_highscore("", 0)

    def show_credits(self, to_remove=None):
        """
        Show the main menu.
        """
        if to_remove:
            self.remove_widget(to_remove)
        creds = Credits()
        self.add_widget(creds)
        creds.display()

    def show_menu(self, to_remove=None):
        """
        Show the main menu.
        """
        if to_remove:
            self.remove_widget(to_remove)
        menu = Menu()
        self.add_widget(menu)

    def show_rules(self, to_remove=None):
        """
        Show the main menu.
        """
        if to_remove:
            self.remove_widget(to_remove)
        rules = Rules()
        self.add_widget(rules)
        rules.display()

    def show_highscore(self, datastring, score, to_remove=None):
        """
        Display the highscore prompt screen.
        """
        if to_remove:
            self.remove_widget(to_remove)
        highscore = Highscore()
        highscore.set_info(datastring, score)
        self.add_widget(highscore)

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

    def popup_score(self, message, flash):
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
        # Set the flash
        popup.set_flash(flash)
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
        self.dataloader = DataLoader()

    def build_config(self, config):
        """
       Configure the application.
       """

        # Icon
        Config.set('kivy', 'window_icon', os.path.join(os.path.dirname(__file__), "resources", "icons", "omission_icon.png"))

        # Moved to top
        # Config.set('graphics', 'multisamples', '0')

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
        self.icon = os.path.join(os.path.dirname(__file__), os.pardir, "resources", "icons", "omission_icon.png")

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
        self.dataloader.write_out()
