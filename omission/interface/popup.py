"""
Popup Label Interface Component [Omission]
"""

import random

from kivy.clock import Clock
from kivy.uix.label import Label

class PopupLabel(Label):
    """
    A popup label item.
    """

    def __init__(self, **kwargs):
        """
        Initialize a new OmissionWindow.
        """
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.animate, 0.1)

    def random_location(self, parent_width, parent_height):
        """
        Select a random location on the screen.
        """
        # Select a random location on the screen.
        # FloatLayer places absolute 0,0 at the center.
        x_low_bound = -(parent_width / 2) + 100
        x_upp_bound = (parent_width / 2) - int(self.width) - 100
        self.x = random.randint(x_low_bound, x_upp_bound)
        y_low_bound = -(parent_height / 2) + 100
        y_upp_bound = (parent_height / 2) - int(self.height) - 100
        self.y = random.randint(y_low_bound, y_upp_bound)

    def set_size(self, size):
        """
        Set the text size and border width.
        """
        self.font_size = str(size*10) + "sp"
        self.outline_width = str(size) + "px"

    def animate(self, *args):
        """
        Move up 1 px and fade 10%. Ten step animation.
        Automatically removes itself from parent when done.
        """
        #pylint: disable=W0613
        self.y = self.y + 3
        self.opacity = self.opacity - 0.1
        # WHY is this line needed to update widget?
        #print("A: " + str(self.y) + " " + str(self.opacity))
        # If we're 0% opacity, the animation is done. Remove.
        if self.opacity <= 0:
            self.event.cancel()
            self.parent.remove_widget(self)
