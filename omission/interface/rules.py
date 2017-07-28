"""
Rules Interface [Omission]
"""

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

class Rules(BoxLayout):
    """
    Displays the game credits.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None
        self._viewing = 0

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
        Handles keyboard presses for the interface.
        """
        # pylint: disable=W0613
        if self._viewing == 0:
            # On ESC...
            if keycode[0] == 27:
                # Switch to the menu.
                self.parent.show_menu(self)
            # If a number key is pressed...
            elif str.isdigit(keycode[1]):
                self._display_item(int(keycode[1]))
        else:
            # Return to index on ENTER or ESC
            if keycode[1] == 'enter' or keycode[0] == 27:
                self._display_item(0)

        if keycode[1] == 'down':
            self._scroll(-0.1)
        if keycode[1] == 'pagedown':
            self._scroll(-0.3)
        elif keycode[1] == 'up':
            self._scroll(0.1)
        elif keycode[1] == 'pageup':
            self._scroll(0.3)


    def _scroll(self, amount=0):
        """
        Scroll the page.
        """
        # Scroll down
        if amount < 0:
            if self.ids.scroll.scroll_y > 0.0:
                newscroll = self.ids.scroll.scroll_y + amount
                if newscroll < 0.0:
                    newscroll = 0.0
                self.ids.scroll.scroll_y = newscroll
        # Scroll up
        elif amount > 0:
            if self.ids.scroll.scroll_y < 1.0:
                newscroll = self.ids.scroll.scroll_y + amount
                if newscroll > 1.0:
                    newscroll = 1.0
                self.ids.scroll.scroll_y = newscroll
        # Return to top of page.
        else:
            self.ids.scroll.scroll_y = 1.0


    def _display_item(self, item):
        """
        Displays the requested item.
        """
        # Store the item we're currently viewing.
        self._viewing = item
        # Scroll to top.
        self._scroll()
        if item == 0:
            self.ids.lbl_rules.text = """
== OMISSION RULES ==

Press a number key to view a section, or ESC to return to the menu.

1: Basic Gameplay
2: Strategies
3: Scoring
4: Chain Bonuses
5: Timed Mode
6: Survival Mode
7: Infinite Mode
8: Game Settings
ESC: Quit
"""
        elif item == 1:
            self.ids.lbl_rules.text = """
== 1. BASIC GAMEPLAY ==

In OMISSION, a passage is displayed on the screen with all instances of a \
SINGLE letter removed. Only one type of letter can be removed. The game \
erases all evidence of the missing letter, by stripping out extra spaces \
and ensuring the first displayed letter of the sentence is always capitalized.

You can PAUSE the game at any time by pressing the ESC key. While paused, \
you can press ENTER to resume, or ESC to quit.

You ANSWER by typing the letter on the keyboard. If your answer is correct, \
you'll receive points. Optionally, the solved passage will be displayed and \
the game paused until you press ENTER.

If your answer is incorrect, you'll lose one of your tries, and your guess \
will be displayed on the right of the screen. "Tries Left", in the upper-left \
corner of the screen, displays how many guesses you have left. If you run \
out of tries, the passage is skipped. Optionally, the correct answer will \
be displayed and the game paused until you press ENTER.

OMISSION provides two types of aids to help you if you're stuck. You can \
control when these are displayed in the game mode settings. (See the Rules \
section for each game mode.)

* The HINT displays how many instances of the letter were removed from the \
current passage. This is displayed under "Removals" in the upper-right corner \
of the screen.

* The CLUE displays underscores in the place of each removed letter.

There are three gameplay modes available:

* In TIMED, you solve as many passages as you can before the clock \
runs out.

* In SURVIVAL, you solve as many passages with as few mistakes as possible.

* In INFINITE, there are no limits - you play until you decide to quit.

See STRATEGIES for tips on how to win.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 2:
            self.ids.lbl_rules.text = """
== 2. STRATEGIES ==

#1: Look for obviously wrong words. For example, words like "th" and "mzing" \
clearly are missing letters.

#2: Don't trust what you see! If a letter is removed from the beginning of \
the sentence, it will capitalize what's left - "To be..." becomes "O be..."!

#3: Watch for words that don't make sense. "Any ice like cheese" has all \
valid words, but the sentence is nonsense. ("M" was removed from the first \
two words.)

#4: A single word can have multiple removals. "te" may look like "h" is \
missing, but it could be missing an "l" to make it "tell" instead!

#5: Be aware of unfamiliar words, like "irremeable" and "bilva". Before \
jumping on an unusual word, check for more obvious clues first.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 3:
            self.ids.lbl_rules.text = """
== 3. SCORING ==

The less letters removed in the passage, the faster your answer, and the \
more tries you have left, the higher your score! If you have one of the top \
eight scores at game's end, you'll be prompted to enter your name.

Separate high scores are stored for each game mode and combination of \
settings.

Your score is calculated following a simple algorithm:

1. The base score is (10 - # removals), although it is never less than 1.

2. Your tries multiplier is (max tries - remaining tries). It is never less \
than 1.

3. Your time multiplier is (5 - solve time). It is never less than 0.

4. Your item score is (base score * (tries multiplier + time multiplier).

5. If you claimed a chain bonus, then your item score becomes (item score * \
chain bonus).

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 4:
            self.ids.lbl_rules.text = """
== 4. CHAIN BONUSES ==

When you quickly solve a passage, a CHAIN BONUS appears to the right of the \
screen. If you answer the next passage while the bonus is displayed, your \
score for that passage will be multiplied by the bonus.

Each time you claim a chain bonus, it increases in size. But be careful! \
If you answer incorrectly or too slowly, it will vanish.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 5:
            self.ids.lbl_rules.text = """
== 5. TIMED MODE ==

In TIMED mode, you must solve passages quickly before the clock \
runs out. Each correct answer will add time to the clock, and \
each incorrect answer will remove time.

Settings:

* TIMER LENGTH: The number of seconds to start with.
* BONUS: The seconds to add on every correct answer.
* PENALTY: The seconds to remove on every incorrect answer.
* TRIES: The number of attempts before the passage is skipped.
* HINT ON: The attempt to show the removal count on.
* CLUE ON: The attempt to show the underscores on.
* CHAIN TIME: The number of seconds before a chain expires.
* SHOW PASSAGE: Whether to display the full passage after solving or skipping.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 6:
            self.ids.lbl_rules.text = """
== 6. SURVIVAL MODE ==

In SURVIVAL mode, you must solve passages with as few mistakes as \
possible. Every time a passage is skipped, you lose a life. There is \
no time limit in survival mode.

Settings:

* LIVES: The number of lives.
* TRIES: The number of attempts before the passage is skipped.
* HINT ON: The attempt to show the removal count on.
* CLUE ON: The attempt to show the underscores on.
* CHAIN TIME: The number of seconds before a chain expires.
* SHOW PASSAGE: Whether to display the full passage after solving or skipping.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 7:
            self.ids.lbl_rules.text = """
== 7. INFINITE MODE ==

In INFINITE mode, you can play as long as you like! There are no limits. \
When you're done playing, just press ESC to pause, and ESC again to quit.

* TRIES: The number of attempts before the passage is skipped.
* HINT ON: The attempt to show the removal count on.
* CLUE ON: The attempt to show the underscores on.
* CHAIN TIME: The number of seconds before a chain expires.
* SHOW PASSAGE: Whether to display the full passage after solving or skipping.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        elif item == 8:
            self.ids.lbl_rules.text = """
== 8. GAME SETTINGS ==

There are two global settings, which are set from the main menu when no \
mode is selected. Both are stored between games.

You can set the VOLUME of the game sound effects to OFF, LOW, MED, or HIGH. \

Two DISPLAY MODES are provided: NORMAL uses the Orbitron and Source Sans Pro \
fonts, and is suitable for most players. DYSLEXIC uses the OpenDyslexic font, \
which may be easier for dyslexic players. After changing DISPLAY MODE, you \
will need to quit and restart the game.

== END OF PAGE: Press ENTER or ESC to return. ==
"""
        # If we got an invalid index number...
        else:
            # Just return to the index.
            self._viewing = 0

    def display(self):
        """
        Automatically progress the credits.
        """
        # Bind the keyboard.
        self._bind_keyboard()

        self._display_item(0)

    def close(self):
        """
        Close the credits window.
        """
        self._unbind_keyboard()
        self.parent.show_menu(self)
