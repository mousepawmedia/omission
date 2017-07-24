"""
Scores and Settings Loader [Omission]
"""

from collections import OrderedDict
import copy
import os.path
import re

from appdirs import user_data_dir

from omission.game.gameround import GameRoundSettings
from omission.interface.sound import SoundPlayer

# Our data layout following these conventions:
# DEF=T:3:2:3:1:30:3:1
# DEF=S:3:2:3:1:3
# DEF=I:3:2:3:1
# SCO=T:3:2:3:1:30:3:1
# :852:Fred
# :1936523:Jason
# :5832:Jarek
# :100:Bob
# SCO=T:5:2:3:1:30:3:1

class ScoreLoader(object):
    """
    Load scores and other stored data from our config file.
    """

    def __init__(self):
        """
        Initialize a new score loader object.
        """
        self.settings = Settings()
        self.soundplayer = SoundPlayer()
        self.scoreboards = []

        appname = "Omission"
        appauthor = "MousePaw Media"
        self.directory = user_data_dir(appname, appauthor)
        self.path = os.path.join(self.directory, "scores.data")
        self._data = None

        try:
            with open(self.path) as scorefile:
                rawdata = scorefile.read()
            self._data = re.split(r'\n', rawdata)
        except FileNotFoundError:
            # The file doesn't yet exist, that's fine. Carry on.
            pass

        self.parse_settings()
        self.parse_scores()

    def parse_settings(self):
        """
        Parse our settings out of our file data.
        """
        if self._data:
            for line in self._data:
                # If we found a settings line...
                if re.match(r'DEF=.*', line):
                    tokens = re.split(r':', line)
                    if tokens[0] == "DEF=T":
                        self.settings.timed.set_clues(int(tokens[1]),
                                                      int(tokens[2]),
                                                      int(tokens[3]))
                        self.settings.timed.set_solution_pause(bool(int(tokens[4])))
                        self.settings.timed.set_timed(int(tokens[5]),
                                                      int(tokens[6]),
                                                      int(tokens[7]))
                    elif tokens[0] == "DEF=S":
                        self.settings.survival.set_clues(int(tokens[1]),
                                                         int(tokens[2]),
                                                         int(tokens[3]))
                        self.settings.survival.set_solution_pause(bool(int(tokens[4])))
                        self.settings.survival.set_survival(int(tokens[5]))
                    elif tokens[0] == "DEF=I":
                        self.settings.infinite.set_clues(int(tokens[1]),
                                                         int(tokens[2]),
                                                         int(tokens[3]))
                        self.settings.infinite.set_solution_pause(bool(int(tokens[4])))

    def parse_scores(self):
        """
        Parse scores out of our file data.
        """
        if self._data:
            for line in self._data:
                scores = None
                # If we found a settings line...
                if re.match(r'SCO=.*', line):
                    scoreboard = Scoreboard(line[4:])
                    # Append the score object to our list.
                    self.scoreboards.append(copy.deepcopy(scoreboard))
                # Else if we found a score line...
                elif re.match(r'^:.*$', line) and scoreboard:
                    tokens = re.split(r':', line[1:])
                    scoreboard.add_score(tokens[0], tokens[1])
                # Else if we find anything else...
                else:
                    # If we HAVE a scores object.
                    if scores:
                        # Append the score object to our list.
                        self.scoreboards.append(copy.deepcopy(scoreboard))

    def write_out(self):
        """
        Write out the new file.
        """
        # Create the folders, if necessary.
        os.makedirs(self.directory, 0o777, True)

        # Generate the output for the file.
        output = ""
        output += self.settings.get_datastring()
        for scoreboard in self.scoreboards:
            output += scoreboard.get_datastring()

        # Write out the output.
        with open(self.path, 'w') as scorefile:
            # Write out
            print(output, file=scorefile)

    def check_score(self, setting_datastring, score):
        """
        Check if a score is worthy of adding to the scoreboard.
        """
        for scoreboard in self.scoreboards:
            if setting_datastring == scoreboard.setting_datastring:
                return scoreboard.check_score(score)

        # If we reach this far, we have no scores for that datastring,
        # and the score is therefore DEFINITELY worth logging.
        return True

    def add_score(self, setting_datastring, score, name):
        """
        Add a new score to the scoreboard.
        """
        for scoreboard in self.scoreboards:
            # If the scoreboard exists...
            if setting_datastring == scoreboard.setting_datastring:
                # Add our score to it.
                scoreboard.add_score(score, name)
                return

        # If we reach this far, we need to create a new scoreboard
        # and add our score to it.
        new_scoreboard = Scoreboard(setting_datastring)
        new_scoreboard.add_score(score, name)
        self.scoreboards.append(new_scoreboard)


class Scoreboard(object):
    """
    Contains the scores for a single settings combination.
    """

    def __init__(self, setting_datastring):
        self.setting_datastring = setting_datastring
        self.scoreboard = OrderedDict()

    def add_score(self, score, name):
        """
        Add a new score.
        """
        self.scoreboard[str(score)] = name
        self.sort_scores()
        # TODO: These aren't actually saving?ig

    def check_score(self, new_score):
        """
        Check if the score is worth logging.
        """
        # If any scores are logged...
        if len(self.scoreboard):
            for score in self.scoreboard:
                # As soon as we find a score the new one is greater than...
                if new_score > score:
                    # Return True
                    return True
            return False
        # If no scores are logged...
        else:
            return True

    def sort_scores(self):
        """
        Sort the scores and only retain the top 10.
        """
        # Clear the main dictionary for refilling.
        self.scoreboard.clear()
        # Sort.
        self.scoreboard = OrderedDict(sorted(self.scoreboard.items()))
        # Keep only the top 10.
        i = 0
        for item in self.scoreboard:
            if i >= 10:
                del self.scoreboard[item]
            i += 1

    def get_scores(self):
        """
        Get data.
        """
        pass

    def get_datastring(self):
        """
        Get the string representation of this object for writing to
        our settings file.
        """
        output = "SCO=" + str(self.setting_datastring) + "\n"
        for key in self.scoreboard:
            output += ":" + str(key) + ":" + str(self.scoreboard[key]) + "\n"
        return output

class Settings(object):
    """
    Contains the default settings for each mode.
    """

    def __init__(self):
        self.timed = GameRoundSettings()
        self.timed.set_timed()
        self.survival = GameRoundSettings()
        self.survival.set_survival()
        self.infinite = GameRoundSettings()
        self.infinite.set_infinite()

    def save_timed(self, settings):
        """
        Copy the given Timed Mode settings into our object.
        """
        self.timed = copy.deepcopy(settings)

    def save_survival(self, settings):
        """
        Copy the given Survival Mode settings into our object.
        """
        self.survival = copy.deepcopy(settings)

    def save_infinite(self, settings):
        """
        Copy the given Infinite Mode settings into our object.
        """
        self.infinite = copy.deepcopy(settings)

    def get_datastring(self):
        """
        Get the string representation of this Settings object for writing to
        our settings file.
        """
        output = ""

        # Write Timed settings.
        output += "DEF=" + self.timed.get_datastring() + "\n"
        # Write Survival settings.
        output += "DEF=" + self.survival.get_datastring() + "\n"
        # Write Infinite settings.
        output += "DEF=" + self.infinite.get_datastring() + "\n"

        return output
