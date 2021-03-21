"""
Message Popup [Omission]
"""

from kivy.app import App
from kivy.uix.popup import Popup

class PopupMessage(Popup):
    """
    A popup message with a single OK button.
    """

    # pylint: disable=R0902
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title_font = App.get_running_app().dataloader.fontloader.decorative()

    def set(self, title, message):
        """
        Set the title and message of the popup.
        """
        self.title = title
        self.ids.lbl_msg.text = message
