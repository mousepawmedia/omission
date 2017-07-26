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
        Handles keyboard progresses. Also calls all game reponses to
        user input. Thus, this is basically our governing function
        during gameplay.
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
        OMISSION \n
        \n
        Produced by MousePaw Games\n
        www.mousepawgames.com\n
        \n
        Concept by Jason C. McDonald\n
        """, """
        -- Programming --\n
        Jason C. McDonald\n
        Jarek Thomas\n
        Wesley Kerfoot\n
        """, """
        -- Content --\n
        Anne McDonald\n
        Jane McArthur\n
        """, """
        -- Sound Effects --\n
        Jason C. McDonald\n
        Created using LMMS\n
        """, """
        -- Game Testing --\n
        Chris "Fox" Frasier\n
        Allie Jensen\n
        Jarek Thomas\n
        (More go here)\n
        """, """
        -- Special Thanks --\n
        #python and #kivy IRC channels (Freenode)\n
        Project Gutenberg\n
        """, """
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
