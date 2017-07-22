"""
Menu Interface [Omission]
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from omission.game.gameround import GameRoundSettings

class Menu(BoxLayout):
    """
    The main menu of the game.
    """
    def __init__(self, **kwargs):
        """
        Initialize a new Menu box.
        """
        super().__init__(**kwargs)
        self.settings = GameRoundSettings()
        # The control panels for mode-specific settings.
        self.info_box = InfoBox()
        self.play_box = PlayBox()
        self.try_settings = TrySettings()
        self.timed_settings = TimedSettings()
        self.survival_settings = SurvivalSettings()

        self.mode = ""
        self.switch_mode(None)

    def press_play(self):
        """
        Callback for Play button.
        """
        self.load_settings()
        self.parent.start_game(self.settings, self)

    def press_toggle(self, mode, button):
        """
        Switch between game modes on menu using toggle buttons.
        """
        if button.state == "down":
            if mode == 'Timed':
                pass
            elif mode == 'Survival':
                pass
            elif mode == 'Infinite':
                pass
            self.switch_mode(mode)
        else:
            self.switch_mode(None)

    def switch_mode(self, mode=None):
        """
        Switch which settings we see and load.
        """
        # Store the mode.
        self.mode = mode

        # Remove all the varying boxes.
        self.ids.box_controls.remove_widget(self.info_box)
        self.ids.box_controls.remove_widget(self.play_box)
        self.ids.box_controls.remove_widget(self.try_settings)
        self.ids.box_controls.remove_widget(self.survival_settings)
        self.ids.box_controls.remove_widget(self.timed_settings)

        if not mode:
            # Display info instead of control boxes.
            self.ids.box_controls.add_widget(self.info_box)
        elif mode == 'Timed':
            # Add the controls for Timed.
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.try_settings)
            self.ids.box_controls.add_widget(self.timed_settings)
        elif mode == 'Survival':
            # Add the controls for Survival
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.try_settings)
            self.ids.box_controls.add_widget(self.survival_settings)
        elif mode == 'Infinite':
            # Add the control for Infinite
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.try_settings)

    def load_settings(self):
        """
        Load the settings from the interface.
        """
        tries = int(self.try_settings.ids.spn_tries.text)
        hint = int(self.try_settings.ids.spn_hint.text) - 1
        clue = int(self.try_settings.ids.spn_clue.text) - 1
        self.settings.set_clues(tries, hint, clue)

        passage = self.try_settings.ids.spn_passage.text == 'True'
        self.settings.set_solution_pause(passage)

        if self.mode == 'Timed':
            time = int(self.timed_settings.ids.spn_time.text)
            bonus = int(self.timed_settings.ids.spn_bonus.text)
            penalty = int(self.timed_settings.ids.spn_penalty.text)
            self.settings.set_timed(time, bonus, penalty)
        elif self.mode == 'Survival':
            lives = int(self.survival_settings.ids.spn_lives.text)
            self.settings.set_survival(lives)
        elif self.mode == 'Infinite':
            self.settings.set_infinite()

class InfoBox(BoxLayout):
    """
    Information about the game.
    """

    def press_rules(self):
        """
        Display the rules.
        """
        pass

    def press_credits(self):
        """
        Display the credits.
        """
        pass

    #pylint: disable=R0201
    def press_quit(self):
        """
        Quit the game.
        """
        App.get_running_app().stop()

class PlayBox(BoxLayout):
    """
    Play button and score box.
    """

    def press_play(self):
        """
        Passes the play button action back to the containing Menu.
        """
        # MUST go back two parents, based on the .kv layout.
        self.parent.parent.press_play()

class TimedSettings(BoxLayout):
    """
    Settings for Timed mode.
    """

class SurvivalSettings(BoxLayout):
    """
    Settings for Survival mode.
    """

class TrySettings(BoxLayout):
    """
    Settings for Survival mode.
    """
