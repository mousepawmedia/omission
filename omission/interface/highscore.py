"""
Highscore Prompt Interface [Omission]
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class Highscore(BoxLayout):
    """
    Displays the prompt for entering a name for a new high score.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datastring = None
        self.score = None

    def set_info(self, datastring, score):
        """
        Set the information for the highscore box.
        """
        self.datastring = datastring
        self.score = score
        self.ids.lbl_score.text = str(self.score)

    def submit(self, name):
        """
        Validate the name, submit the score, and close.
        """
        # If we actually have a name...
        if not name == "":
            # Register the high score.
            App.get_running_app().dataloader.add_score(self.datastring,
                                                       self.score, name)
            # Switch to the menu.
            self.parent.show_menu(self)

class NameTextInput(TextInput):
    """
    Extend the TextInput widget to introduce a character maximum.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = App.get_running_app().dataloader.fontloader.decorative()

    def insert_text(self, substring, from_undo=False):
        """
        Prevent too many characters.
        """
        limit = 12
        if len(self.text) >= limit:
            substring = ""
        return super().insert_text(substring, from_undo=from_undo)

    def submit(self):
        """
        Mirror to parent's submit.
        """
        # Get the name entered in the text box.
        name = self.text
        self.parent.submit(name)
