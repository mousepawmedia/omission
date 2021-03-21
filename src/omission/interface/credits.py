"""
Credits Interface [Omission]
"""

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

class Credits(BoxLayout):
    """
    Displays the game credits.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None

    def _bind_keyboard(self):
        """
        Bind the keyboard.
        """
        # Listen for keyboard events.
        self._keyboard = Window.request_keyboard(self._unbind_keyboard, self)
        self._keyboard.bind(on_key_down=self._on_kbd_down)

    def _unbind_keyboard(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_kbd_down)
            self._keyboard = None

    # pylint: disable=R0201
    def _on_kbd_down(self, keyboard, keycode, text, modifiers):
        """
        Handles keyboard events, namely the enter and esc keys.
        """
        # pylint: disable=W0613
        if keycode[1] == 'enter' or keycode[0] == 27:
            # Switch to the menu.
            self.parent.show_menu(self)

    def _display_next(self):
        """
        Return the credits text.
        """
        credits_text = ("""
OMISSION
Produced by MousePaw Games

Concept by Jason C. McDonald
""", """
-- Programming --
Jason C. McDonald
Jarek Thomas
""", """
-- Content --
Anne McDonald
Jane McArthur
""", """
-- Sound Effects --
Jason C. McDonald
Created using LMMS
""", """
-- Fonts --
Orbitron
by Matt McInerney
SIL Open Font License

Source Sans Pro
by Adobe Systems Incorporated
SIL Open Font License
""", """
-- Fonts (cont.) --
Open Dyslexic
by Abbie Gonzalez
http://dyslexicfonts.com

Based on Bitstream Vera
by Jim Lyles
Bitstream Vera License v1.00
""", """
-- Game Testing --
Chris "Fox" Frasier
Allie Jensen
Jarek Thomas
Ethan Thompson
Jane McArthur
""", """
-- Special Thanks --
#python and #kivy IRC channels (Freenode)
Project Gutenberg
""", """
-- License --
OMISSION is open source, and licensed under
The 3-Clause BSD License.
This means, you're free to download and share!
""", """
-- License (Cont.) --
The OMISSION text content (content.txt) is Public Domain.
""", """
-- License (Cont.) --
The OMISSION logo and sound effects are
Copyright 2021 MousePaw Media. All Rights Reserved.
""", """
MousePaw Games
Scamper Into Adventure!
www.mousepawgames.com

Press ENTER or ESC to return to menu.
""")

        for item in credits_text:
            self.ids.lbl_credits.text = item
            yield True

        # Stop the timer when we're done.
        yield False

    def display(self):
        """
        Automatically progress the credits.
        """
        # Bind the keyboard.
        self._bind_keyboard()

        timeout = 3

        display = self._display_next()
        def _next(*args):
            # pylint: disable=W0613
            return display.__next__()

        # Run the initial function.
        _next()
        # Run repeat calls on a clock
        Clock.schedule_interval(_next, timeout)

    def close(self):
        """
        Close the credits window.
        """
        self._unbind_keyboard()
        self.parent.show_menu(self)
