"""
Highscore Prompt Interface [Omission]
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

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

    def submit(self):
        """
        Validate the name, submit the score, and close.
        """
        # Get the name entered in the text box.
        name = self.ids.txt_name.text
        # If we actually have a name...
        if not name == "":
            # Register the high score.
            App.get_running_app().scoreloader.add_score(self.datastring,
                                                        self.score, name)
            # Switch to the menu.
            self.parent.show_menu(self)
