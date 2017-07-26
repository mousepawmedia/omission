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

    def changed(self):
        """
        Called when a setting is changed, so we can update scores.
        """
        self.get_scores()

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
        # Store the settings for retrieval on switching back later.
        self.load_settings()

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
            self.get_settings(mode)
        elif mode == 'Survival':
            # Add the controls for Survival
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.try_settings)
            self.ids.box_controls.add_widget(self.survival_settings)
            self.get_settings(mode)
        elif mode == 'Infinite':
            # Add the control for Infinite
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.try_settings)
            self.get_settings(mode)

        self.get_scores()

    def get_settings(self, mode=None):
        """
        Load the saved settings into the interface.
        """
        saved = App.get_running_app().scoreloader.settings
        if mode == 'Timed':
            self.try_settings.ids.spn_tries.text = str(saved.timed.tries)
            self.try_settings.ids.spn_hint.text = str(saved.timed.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.timed.clue_at + 1)
            self.try_settings.ids.spn_passage.text = str(saved.timed.solution_pause)

            self.timed_settings.ids.spn_time.text = str(saved.timed.limit)
            self.timed_settings.ids.spn_bonus.text = str(saved.timed.bonus)
            self.timed_settings.ids.spn_penalty.text = str(saved.timed.penalty)

        elif mode == 'Survival':
            self.try_settings.ids.spn_tries.text = str(saved.survival.tries)
            self.try_settings.ids.spn_hint.text = str(saved.survival.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.survival.clue_at + 1)
            self.try_settings.ids.spn_passage.text = str(saved.survival.solution_pause)

            self.survival_settings.ids.spn_lives.text = str(saved.survival.limit)

        elif mode == 'Infinite':
            self.try_settings.ids.spn_tries.text = str(saved.infinite.tries)
            self.try_settings.ids.spn_hint.text = str(saved.infinite.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.infinite.clue_at + 1)
            self.try_settings.ids.spn_passage.text = str(saved.infinite.solution_pause)

    def get_scores(self, settings=None):
        """
        Load the scores into the interface.
        """
        # If we have a mode loaded.
        if self.mode:
            # If no settings were specified
            if not settings:
                settings = GameRoundSettings()
                self.load_settings(settings)
            # Use the datastring to get the scores.
            scores = App.get_running_app().scoreloader.get_scores(settings.get_datastring())
            scores_scores = ""
            scores_names = ""
            if scores:
                for item in scores:
                    scores_scores += str(item[0]) + "\n"
                    scores_names += str(item[1]) + "\n"
            else:
                scores_scores += "NO"
                scores_names += "SCORES"
            self.play_box.ids.lbl_scores_scores.text = scores_scores
            self.play_box.ids.lbl_scores_names.text = scores_names

    def load_settings(self, settings=None):
        """
        Load the settings from the interface.
        """
        # If no settings were specified...
        if not settings:
            # Store in the main settings.
            settings = self.settings
        # For any of the modes...
        if self.mode is not None:
            tries = int(self.try_settings.ids.spn_tries.text)
            hint = int(self.try_settings.ids.spn_hint.text) - 1
            clue = int(self.try_settings.ids.spn_clue.text) - 1
            settings.set_clues(tries, hint, clue)

            passage = self.try_settings.ids.spn_passage.text == 'True'
            settings.set_solution_pause(passage)

        if self.mode == 'Timed':
            time = int(self.timed_settings.ids.spn_time.text)
            bonus = int(self.timed_settings.ids.spn_bonus.text)
            penalty = int(self.timed_settings.ids.spn_penalty.text)
            settings.set_timed(time, bonus, penalty)
            App.get_running_app().scoreloader.settings.save_timed(settings)
        elif self.mode == 'Survival':
            lives = int(self.survival_settings.ids.spn_lives.text)
            settings.set_survival(lives)
            App.get_running_app().scoreloader.settings.save_survival(settings)
        elif self.mode == 'Infinite':
            settings.set_infinite()
            App.get_running_app().scoreloader.settings.save_infinite(settings)

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

    def changed(self):
        """
        When we change an event, call the parent's changed() function.
        """
        self.parent.parent.changed()

class TimedSettings(BoxLayout):
    """
    Settings for Timed mode.
    """

    def changed(self):
        """
        When we change an event, call the parent's changed() function.
        """
        self.parent.parent.changed()

class SurvivalSettings(BoxLayout):
    """
    Settings for Survival mode.
    """

    def changed(self):
        """
        When we change an event, call the parent's changed() function.
        """
        self.parent.parent.changed()

class TrySettings(BoxLayout):
    """
    Settings for Survival mode.
    """

    def changed(self):
        """
        When we change an event, call the parent's changed() function.
        """
        self.parent.parent.changed()
