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
        self.scoreboards = OrderedDict()

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
        # Temporary datastring storage.
        datastring = ""

        if self._data:
            for line in self._data:
                # If we found a settings line...
                if re.match(r'SCO=.*', line):
                    # Store the datastring.
                    datastring = line[4:]
                    self.scoreboards[datastring] = Scoreboard(datastring)
                # Else if we found a score line...
                elif re.match(r'^:.*$', line) and datastring != "":
                    tokens = re.split(r':', line[1:])
                    try:
                        self.scoreboards[datastring].add_score(int(tokens[0]),
                                                               tokens[1])
                    except KeyError:
                        pass
                # If we find anything else, ignore the line.

    def write_out(self):
        """
        Write out the new file.
        """
        # Create the folders, if necessary.
        os.makedirs(self.directory, 0o777, True)

        # Generate the output for the file.
        output = ""
        output += self.settings.get_datastring()
        #pylint: disable=W0612
        for datastr, scoreboard in self.scoreboards.items():
            output += scoreboard.get_datastring()

        # Write out the output.
        with open(self.path, 'w') as scorefile:
            # Write out
            print(output, file=scorefile)

    def get_scores(self, setting_datastring):
        """
        Get the scores from the scoreboard for the given datastring.
        """
        try:
            scoreboard = self.scoreboards[setting_datastring]
            return scoreboard.get_scores()
        except KeyError:
            return None

    def check_score(self, setting_datastring, score):
        """
        Check if a score is worthy of adding to the scoreboard.
        """
        try:
            scoreboard = self.scoreboards[setting_datastring]
            return scoreboard.check_score(score)
        except KeyError:
            # We have no scores for that datastring,
            # and thus the score is DEFINITELY worth logging.
            return True

    def add_score(self, setting_datastring, score, name):
        """
        Add a new score to the scoreboard.
        """
        try:
            scoreboard = self.scoreboards[setting_datastring]
            # Add our score to it.
            scoreboard.add_score(score, name)
        except KeyError:
            # We need to create a new scoreboard and add our score to it.
            self.scoreboards[setting_datastring] = Scoreboard(setting_datastring)
            self.scoreboards[setting_datastring].add_score(score, name)

class Scoreboard(object):
    """
    Contains the scores for a single settings combination.
    """

    def __init__(self, setting_datastring):
        self.setting_datastring = setting_datastring
        self.scoreboard = OrderedDict()
        self.full = False
        # This determines how many scores we keep.
        self.retain = 8

    def add_score(self, score, name):
        """
        Add a new score.
        """
        self.scoreboard[score] = name
        self.sort_scores()

    def check_score(self, new_score):
        """
        Check if the score is worth logging.
        """
        # If any scores are logged...
        if len(self.scoreboard) >= self.retain:
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
        # Sort (descending)
        self.scoreboard = OrderedDict(reversed(sorted(self.scoreboard.items())))
        # Keep only the top 'n' items:
        # Counts how many elements we've seen.
        i = 0
        # For each item...
        for item in self.scoreboard:
            # If we have more than the max...
            if i >= self.retain:
                # Remove the item.
                del self.scoreboard[item]
            i += 1

    def get_scores(self):
        """
        Get the scores from this scoreboard.
        """
        # We'll return as a list of tuples.
        scores = []
        # Iterate through the OrderedDict...
        for score, name in self.scoreboard.items():
            # Append a tuple for each pair to our return list.
            scores.append((score, name))
        return scores

    def get_datastring(self):
        """
        Get the string representation of this object for writing to
        our settings file.
        """
        output = "SCO=" + str(self.setting_datastring) + "\n"
        for score, name in self.scoreboard.items():
            output += ":" + str(score) + ":" + str(name) + "\n"
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
