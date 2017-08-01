"""
Game Interface [Omission]
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

from omission.data import img_loader
from omission.interface.helpful import sec_to_timestring, score_to_scorestring
from omission.game.contentloader import ContentLoader
from omission.game.gameround import GameRound, GameMode, GameStatus
from omission.game.gameround import GameRoundSettings

class Gameplay(BoxLayout):
    """
    The gameplay interface.
    """
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        """
        Initialize a new Gameplay box.
        """
        super().__init__(**kwargs)
        self.loader = ContentLoader()
        self.settings = GameRoundSettings()
        self.playing = False
        self.gameround = None

        self.soundplayer = App.get_running_app().dataloader.soundplayer

        #Track guesses.
        self._guesses = []
        # Indicates whether we're paused for a solution.
        self.solution_pause = False
        # Holds keyboard bindings.
        self._keyboard = None
        # Reset the interface.
        self.reset()

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
        # Get the key we pressed.
        key = keycode[1]
        if self.playing:
            # If we pressed a letter key.
            if len(key) == 1 and key.isalpha() and self.check_guesses(key) \
            and not self.gameround.is_paused():
                status = self.gameround.answer(key)
                # If the answer was right...
                if status == GameStatus.Correct:
                    # Update the score. Sound is played from here.
                    self.update_score()
                    # Clear our guess list.
                    self.update_guesses()
                    # Show the solution.
                    self.show_feedback(True)
                # If the answer was wrong, but we have guesses left...
                elif status == GameStatus.Incorrect:
                    # Display the keypress.
                    self.parent.popup_key(key)
                    # Wrong, log our guess.
                    self.update_guesses(key)
                    # Update the puzzle and hint.
                    self.update_puzzle()
                    # Update the game status.
                    self.update_status()
                elif status == GameStatus.Skipped:
                    # Display the keypress.
                    self.parent.popup_key(key)
                    # Wrong, clear our guesses and move on.
                    self.update_guesses()
                    # IF the game is NOT over...
                    if self.playing:
                        # Play low bell.
                        self.soundplayer.play_lowbell()
                        # Show the solution.
                        self.show_feedback(False)
                        # NOTE: Without this check, the gameover doesn't
                        # get displayed, because this call to show_feedback
                        # overrides it.
            # If we're paused and press the ENTER key.
            elif key == 'enter' and self.gameround.is_paused():
                # Resume the game.
                self.resume_game()
            # If we press the ESC key, pause the game.
            elif keycode[0] == 27 and not self.gameround.is_paused():
                # Pause the game.
                self.pause_game()
            elif keycode[0] == 27 and self.gameround.is_paused():
                # Quit the game.
                self.quit_game()
        else:
            if key == 'enter':
                # Quit the game.
                self.quit_game()

    def set_settings(self, settings):
        """
        Define the settings object for the new round.
        """
        self.settings = settings

    def play(self):
        """
        Play the game.
        """
        # Ensure the keyboard is hooked up. This is disconnected at quit.
        self._bind_keyboard()
        self.gameround = GameRound(App.get_running_app().set_kill_callback,
                                   self.gameover, self.tick, self.loader,
                                   self.settings)
        self.playing = True
        self.gameround.start_round()
        self.update_status(True)
        self.update_puzzle()

    def gameover(self):
        """
        The game is over.
        """
        # Stop the game
        self.playing = False
        # Reset the interface
        self.reset()
        # Play the gameover sound.
        self.soundplayer.play_gameover()
        # Show the last solution
        self.show_feedback(False, True)

    def tick(self):
        """
        Runs every second.
        """
        self.update_status()

    def show_feedback(self, correct, gameover=False):
        """
        Show the solution, pausing the game during.
        """
        solution_str = ""
        # If we're supposed to pause on solution.
        if self.gameround.settings.solution_pause:
            solution = self.gameround.get_solution()

            # If we got the answer correct, say so...
            if correct:
                solution_str += "CORRECT!" + "\n\n"

            # Otherwise, if the answer was wrong...
            else:
                # Update the rest of the interface: lives, tries, etc.
                self.update_status(False, True)
                solution_str += "ANSWER: " + str(solution[0]) + "\n\n"

            # Either way, display the solution.
            solution_str += str(solution[1]) + "\n\n"

            # If the game is over...
            if not gameover:
                solution_str += "ENTER to continue.\nESC to quit."
            else:
                solution_str += "GAME OVER\nENTER to return to menu."
            self.ids.lbl_puzzle.text = solution_str

            # Pause the game in solution mode.
            self.pause_game(True)

        # If we're not supposed to pause...
        elif not self.gameround.settings.solution_pause:
            # If the game IS over...
            if gameover:
                # Set a string, which we'll display anyway.
                solution_str = "GAME OVER\nENTER to return to menu."
                self.ids.lbl_puzzle.text = solution_str
                # Update the rest of the interface: lives, tries, etc.
                self.update_status(False, True)
            # We always pause, since resuming handles game progression.
            self.pause_game(True)
            # If the game is NOT over...
            if not gameover:
                # Automatically continue.
                self.resume_game()

    def pause_game(self, as_solution=False):
        """
        Pause the game.
        """
        if self.gameround and not self.gameround.is_paused():
            self.gameround.pause()
            if as_solution:
                self.solution_pause = True
            else:
                self.solution_pause = False
                self.ids.lbl_puzzle.text = "GAME PAUSED\nENTER to resume." + \
                                        "\nESC to quit."

    def resume_game(self, *arg):
        """
        Resume the game after a pause.
        """
        # pylint: disable=W0613
        if self.gameround.is_paused():
            self.gameround.resume()
            if self.solution_pause:
                self.next_puzzle()
            else:
                self.update_puzzle()
                self.update_status()

    def next_puzzle(self):
        """
        Load and display the next puzzle.
        """
        # Get the next puzzle.
        self.gameround.new_item()
        # Show the puzzle.
        self.update_puzzle()
        # Update the game status.
        self.update_status()

    def check_guesses(self, guess):
        """
        Check if the guess was already used.
        """
        return not guess in self._guesses

    def update_puzzle(self):
        """
        Update the puzzle and removed letters hint.
        """
        puzzle = self.gameround.get_puzzle()
        self.ids.lbl_puzzle.text = puzzle[0]
        if puzzle[1] > 0:
            self.ids.lbl_removals.text = str(puzzle[1])
        else:
            self.ids.lbl_removals.text = "?"

    def update_guesses(self, guess=None):
        """
        Update the guesses.
        """
        if guess:
            # Add the guess to the list.
            self._guesses.append(guess)
        # If we didn't pass a guess.
        else:
            # Empty the list.
            self._guesses[:] = []

        guess_str = ""
        for ltr in self._guesses:
            guess_str += ltr + '\n'

        # Print the guesses in the interface.
        self.ids.lbl_guess.text = guess_str

    def update_score(self):
        """
        Update the score displayed on the screen.
        """
        score = self.gameround.get_score()
        self.ids.lbl_score.text = score_to_scorestring(score[0])
        # Update chain.
        if score[2] > 1:
            self.ids.lbl_chain.text = "x" + str(score[2])
            # Play bonus sound.
            self.soundplayer.play_bonus(score[2] - 1)
            # Flash popup
            self.parent.popup_score("+" + str(score[1]), True)
        else:
            # No chain.
            self.ids.lbl_chain.text = ""
            # Play ding.
            self.soundplayer.play_ding()
            # Flash popup
            self.parent.popup_score("+" + str(score[1]), False)

    def update_status(self, check_mode=False, no_alarm=False):
        """
        Update the interface.
        """
        # pylint: disable=R0912
        info = self.gameround.get_status()
        if check_mode:
            if info[0] == GameMode.Survival:
                self.ids.img_mode.source = img_loader.load_image("heart.png")
            elif info[0] == GameMode.Timed:
                self.ids.img_mode.source = img_loader.load_image("clock.png")
            elif info[0] == GameMode.Infinite:
                self.ids.img_mode.source = img_loader.load_image("infinity.png")

        # Update remaining time.
        self.ids.bar_remaining.value = info[1]

        # Update time remaining label.
        self.ids.lbl_remaining.text = sec_to_timestring(info[2])
        if info[0] == GameMode.Survival:
            self.ids.lbl_lives.text = "[" + str(info[3]) + "]"
            self.ids.lbl_lives.size_hint_x = 0.1
        else:
            self.ids.lbl_lives.text = ""
            self.ids.lbl_lives.size_hint_x = 0.0

        # Our default colors are green.
        color = get_color_from_hex("#00FF00")
        outline_color = get_color_from_hex('#007700')

        # In Timed or Survival mode, change color to reflect remaining time/lives.
        if info[0] == GameMode.Timed or info[0] == GameMode.Survival:
            # If we have 1/6 or less remaning, display as RED.
            if info[1] <= 16:
                color = get_color_from_hex("#FF0000")
                outline_color = get_color_from_hex('#960000')
                # Also play warning sound.
                if not no_alarm:
                    self.soundplayer.play_alarm()
            # If we 1/3 or less remaining, display as ORANGE.
            elif info[1] <= 33:
                color = get_color_from_hex("#FFB600")
                outline_color = get_color_from_hex('#960000')
            # If we have 50% or less remaining, display as YELLOW-ORANGE.
            elif info[1] <= 50:
                color = get_color_from_hex("#C8FF00")
                outline_color = get_color_from_hex('#960000')
            # If we have 75% or less remaining, display as YELLOW-GREEN.
            elif info[1] <= 75:
                color = get_color_from_hex("#C8FF00")
                outline_color = get_color_from_hex('#007700')
            # Otherwise, we use the default.

            self.ids.lbl_remaining.color = color
            self.ids.lbl_remaining.outline_color = outline_color
            self.ids.lbl_lives.color = color
            self.ids.lbl_lives.outline_color = outline_color

        # Update tries.
        self.ids.lbl_tries.text = str(self.gameround.get_tries())

        # Check if the chain has expired.
        if not info[4]:
            self.ids.lbl_chain.text = ""

    def reset(self):
        """
        Reset the interface to game-over mode.
        """
        self.ids.lbl_score.text = score_to_scorestring(0)
        self.ids.bar_remaining.value = 0
        self.ids.lbl_remaining.text = sec_to_timestring(0)
        self.ids.lbl_tries.text = "?"
        self.ids.lbl_removals.text = "?"
        self.ids.lbl_chain.text = ""
        self.ids.lbl_guess.text = ""
        self.ids.lbl_puzzle.text = "GAME OVER\nENTER to return to menu."

    def quit_game(self):
        """
        Quit the game and return to the main menu.
        """
        # Not playing game.
        self.playing = False
        # Disconnect our gameround callback.
        App.get_running_app().set_kill_callback(None)
        # Disconnect the keyboard.
        self._unbind_keyboard()

        # Check for score logging.
        datastring = self.gameround.settings.get_datastring()
        score = self.gameround.get_score()
        if App.get_running_app().dataloader.check_score(datastring, score[0]):
            self.parent.show_highscore(datastring, score[0], self)
        else:
            # Switch to the menu.
            self.parent.show_menu(self)
