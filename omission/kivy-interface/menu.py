"""
Menu Interface [Omission]
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from omission.game.gameround import GameRoundSettings
from omission.interface.message import PopupMessage

class Menu(BoxLayout):
    """
    The main menu of the game.
    """
    # pylint: disable=R0902
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
        self.infinite_settings = InfiniteSettings()

        # Prevent reacting to changes WHILE loading settings.
        self._change_killswitch = False

        self.mode = ""
        self.switch_mode(None)

    def changed(self):
        """
        Called when a setting is changed, so we can update scores.
        """
        if not self._change_killswitch:
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
        self.ids.box_controls.remove_widget(self.infinite_settings)

        if not mode:
            # Display info instead of control boxes.
            self.ids.box_controls.add_widget(self.info_box)
            self.get_settings()
        elif mode == 'Timed':
            # Add the controls for Timed.
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.timed_settings)
            self.ids.box_controls.add_widget(self.try_settings)
            self.get_settings(mode)
            self.get_scores()
        elif mode == 'Survival':
            # Add the controls for Survival
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.survival_settings)
            self.ids.box_controls.add_widget(self.try_settings)
            self.get_settings(mode)
            self.get_scores()
        elif mode == 'Infinite':
            # Add the control for Infinite
            self.ids.box_controls.add_widget(self.play_box)
            self.ids.box_controls.add_widget(self.infinite_settings)
            self.ids.box_controls.add_widget(self.try_settings)
            self.get_settings(mode)
            self.get_scores()

    def get_settings(self, mode=None):
        """
        Load the saved settings into the kivy-interface.
        """
        # Prevent UI changes from triggering a save.
        self._change_killswitch = True

        saved = App.get_running_app().dataloader.settings
        if mode == 'Timed':
            self.timed_settings.ids.spn_time.text = str(saved.timed.limit)
            self.timed_settings.ids.spn_bonus.text = str(saved.timed.bonus)
            self.timed_settings.ids.spn_penalty.text = str(saved.timed.penalty)
            self.timed_settings.ids.spn_tries.text = str(saved.timed.tries)

            self.try_settings.ids.spn_hint.text = str(saved.timed.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.timed.clue_at + 1)
            self.try_settings.ids.spn_chain.text = str(saved.timed.chain)
            self.try_settings.ids.spn_passage.text = str(saved.timed.solution_pause)

        elif mode == 'Survival':
            self.survival_settings.ids.spn_lives.text = str(saved.survival.limit)
            self.survival_settings.ids.spn_tries.text = str(saved.survival.tries)

            self.try_settings.ids.spn_hint.text = str(saved.survival.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.survival.clue_at + 1)
            self.try_settings.ids.spn_chain.text = str(saved.survival.chain)
            self.try_settings.ids.spn_passage.text = str(saved.survival.solution_pause)

        elif mode == 'Infinite':
            self.infinite_settings.ids.spn_tries.text = str(saved.infinite.tries)

            self.try_settings.ids.spn_hint.text = str(saved.infinite.count_at + 1)
            self.try_settings.ids.spn_clue.text = str(saved.infinite.clue_at + 1)
            self.try_settings.ids.spn_chain.text = str(saved.infinite.chain)
            self.try_settings.ids.spn_passage.text = str(saved.infinite.solution_pause)

        else:
            vol_str = "Vol: "
            vol = App.get_running_app().dataloader.soundplayer.get_volume()
            if vol == 0:
                vol_str += "Off"
            elif vol <= 3:
                vol_str += "Low"
            elif vol <= 6:
                vol_str += "Med"
            else:
                vol_str += "High"
            self.info_box.ids.spn_vol.text = vol_str

            dys = App.get_running_app().dataloader.fontloader.get_dyslexic_mode()
            if dys:
                self.info_box.ids.spn_dys.text = "Dyslexic"
            else:
                self.info_box.ids.spn_dys.text = "Normal"

        # UI changes should now cause settings to be saved.
        self._change_killswitch = False

    def get_scores(self):
        """
        Load the scores into the kivy-interface.
        """
        self.load_settings()
        # If we have a mode loaded.
        if self.mode:
            # Use the datastring to get the scores.
            scores = App.get_running_app().dataloader.get_scores(self.settings.get_datastring())
            scores_str = ""
            if scores:
                for item in scores:
                    scores_str += str(item[0]) + " | " + str(item[1]) + "\n"
            self.play_box.ids.lbl_scores.text = scores_str

    def load_settings(self):
        """
        Load the settings from the kivy-interface.
        """
        # For any of the modes...
        if self.mode:
            hint = int(self.try_settings.ids.spn_hint.text) - 1
            clue = int(self.try_settings.ids.spn_clue.text) - 1
            self.settings.set_clues(hint, clue)

            chain = int(self.try_settings.ids.spn_chain.text)
            self.settings.set_chain(chain)

            passage = self.try_settings.ids.spn_passage.text == 'True'
            self.settings.set_solution_pause(passage)

        if self.mode == 'Timed':
            time = int(self.timed_settings.ids.spn_time.text)
            bonus = int(self.timed_settings.ids.spn_bonus.text)
            penalty = int(self.timed_settings.ids.spn_penalty.text)
            tries = int(self.timed_settings.ids.spn_tries.text)
            self.settings.set_timed(time, bonus, penalty, tries)
            App.get_running_app().dataloader.settings.save_timed(self.settings)
        elif self.mode == 'Survival':
            lives = int(self.survival_settings.ids.spn_lives.text)
            tries = int(self.survival_settings.ids.spn_tries.text)
            self.settings.set_survival(lives, tries)
            App.get_running_app().dataloader.settings.save_survival(self.settings)
        elif self.mode == 'Infinite':
            tries = int(self.infinite_settings.ids.spn_tries.text)
            self.settings.set_infinite(tries)
            App.get_running_app().dataloader.settings.save_infinite(self.settings)

class InfoBox(BoxLayout):
    """
    Information about the game.
    """

    def press_rules(self):
        """
        Display the rules.
        """
        self.parent.parent.parent.show_rules(self.parent.parent)

    def press_credits(self):
        """
        Display the credits.
        """
        self.parent.parent.parent.show_credits(self.parent.parent)

    #pylint: disable=R0201
    def press_quit(self):
        """
        Quit the game.
        """
        self.parent.parent.load_settings()
        App.get_running_app().stop()

    def font_mode(self):
        """
        Switch between normal and dyslexic display modes.
        """
        dys = App.get_running_app().dataloader.fontloader.get_dyslexic_mode()

        if self.ids.spn_dys.text == "Normal":
            mode = False
        elif self.ids.spn_dys.text == "Dyslexic":
            mode = True

        if mode != dys:
            App.get_running_app().dataloader.fontloader.set_dyslexic_mode(mode)
            popup_message = PopupMessage()
            popup_message.set("Display Mode Changed",
                              "You must restart Omission to apply your changes.")
            popup_message.open()

    def volume(self):
        """
        Change the volume.
        """
        vol_str = self.ids.spn_vol.text
        if vol_str == "Vol: Off":
            App.get_running_app().dataloader.soundplayer.set_volume(0)
        elif vol_str == 'Vol: Low':
            App.get_running_app().dataloader.soundplayer.set_volume(3)
        elif vol_str == 'Vol: Med':
            App.get_running_app().dataloader.soundplayer.set_volume(6)
        elif vol_str == 'Vol: High':
            App.get_running_app().dataloader.soundplayer.set_volume(10)

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

class InfiniteSettings(BoxLayout):
    """
    Settings for Infinite mode.
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
