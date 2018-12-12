"""
Scoreboard [Omission]
Version: 2.0

Contains the high scores for each game type.

Author(s): Jason C. McDonald
"""

# LICENSE
# Copyright (c) 2018 MousePaw Media.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
# CONTRIBUTING
# See https://www.mousepawmedia.com/developers for information
# on how to contribute to our projects.

from collections import OrderedDict
import itertools
import re

from omission.common.classproperty import classproperty


class Scoreboard(object):
    """
    Contains the scores for a single settings combination.
    """

    # This determines how many scores we keep
    retain = 6

    # Datastring patterns
    pattern_datastring_scoreboard = re.compile(r'^SCO=[TSI:\d]')
    pattern_datastring_score = re.compile(r'^:[\d:]+')

    def __init__(self, datastring):
        """
        :param datastring: the datastring for the associated game round settings
        """
        self.gameround_datastring = datastring
        self.scoreboard = OrderedDict()

    def add_score(self, score, name):
        """
        Add a new score to the scoreboard
        :param score: the score
        :param name: the name of the player
        :return: None
        """
        self.scoreboard[score] = name
        self.sort_scores()

    def check_score(self, new_score):
        """
        Check if the score is worth logging.
        We use this to determine if we display the 'new high score' screen.
        :param new_score: the score to enter
        :return: True if worth logging, else False
        """
        # If the scoreboard is full...
        if len(self.scoreboard) >= self.retain:

            # Look thorough all our scores...
            for score in self.scoreboard:
                # As soon as we find a score smaller than the new one...
                if score < new_score:
                    # We want to log
                    return True

            # Otherwise, if we didn't find any smaller scores, we're not interested
            return False

        # If no scores are logged...
        else:
            # ...then we automatically want to log.
            return True

    def sort_scores(self):
        """
        Sort the scores and only retain the top n.
        :return: None
        """
        self.scoreboard = OrderedDict(
            # Keep only the top n items...
            itertools.islice(
                # ...which are sorted descending (highest value first)
                reversed(sorted(self.scoreboard.items())),
                # We control how many items to keep with the static property 'retain'
                0, self.retain))

    def get_scores(self):
        """
        :return: the scores from this scoreboard, as a list of tuples
        """
        return [(score, name) for score, name in self.scoreboard.items()]

    @property
    def datastring(self):
        """
        :return: The generated datastring for the scoreboard
        """
        r = f'SCO={self.gameround_datastring}\n'
        for score, name in self.scoreboard.items():
            r += f':{score}:{name}\n'
        return r

    def parse_score(self, datastring):
        """
        :param datastring: the datastring to parse
        :return: True if successful, else False
        """
        # Ensure the datastring fits the pattern for a score.
        if self.pattern_datastring_score.match(datastring):
            # Attempt to extract and store the score data.
            data = datastring.split(':')
            try:
                self.add_score(int(data[1]), data[2])
            except (IndexError, ValueError):
                return False
            else:
                return True
        # If the datastring isn't a score, report failure.
        else:
            return False


class Scoreboards(object):
    """
    Statically stores all the scoreboards, indexed by their game settings.
    """

    _boards = dict()

    # Tracks the last header we were parsing
    __last_parse_header = None

    @classmethod
    def get_scoreboard(cls, datastring: str):
        """
        Retrieve a scoreboard by its game round settings.
        :param datastring: the datastring for the game round settings
        :return: the scoreboard, if it exists; else None
        """
        try:
            return cls._boards[datastring]
        except KeyError:
            None

    @classmethod
    def create_scoreboard(cls, datastring: str):
        """
        Create a new scoreboard
        :param datastring: the datastring for the game round settings
        :return: the created scoreboard, else None if it already existed
        """
        if cls.get_scoreboard(datastring) is None:
            cls._boards[datastring] = Scoreboard(datastring)
            return cls._boards[datastring]
        else:
            return None

    @classmethod
    def store_scoreboard(cls, board: Scoreboard):
        """
        Store or update a scoreboard
        :param board: the scoreboard to store
        :return: None
        """
        cls._boards[board.gameround_datastring] = board

    @classmethod
    def delete_scoreboard(cls, datastring: str):
        """
        Delete a scoreboard by its game round settings.
        :param datastring: the datastring for the game round settings
        :return: True if deleted, False if it wasn't present
        """
        if cls._boards.pop(datastring, False):
            return True
        # Otherwise, if no such board was found...
        return False

    @classproperty
    def datastring(cls):
        r = ""
        for data, board in cls._boards.items():
            r += board.datastring
        return r

    @classmethod
    def parse_datastring(cls, datastring: str):
        # If we have a new scoreboard header, parse it out and store it.
        if Scoreboard.pattern_datastring_scoreboard.match(datastring):
            try:
                # Parse out the game round settings for the scoreboard
                cls.__last_parse_header = datastring.split('=')[1]
                # Create the new scoreboard if it doesn't already exist.
                if not cls.get_scoreboard(cls.__last_parse_header):
                    cls.create_scoreboard(cls.__last_parse_header)
            except (IndexError, ValueError):
                return False
            else:
                return True
        # If we already received a scoreboard header, and the datastring isn't a new one...
        elif cls.__last_parse_header:
            # Attempt to parse the datastring as a score.
            board = cls.get_scoreboard(cls.__last_parse_header)
            return board.parse_score(datastring)
        else:
            # If the datastring failed to be parsed as a scoreboard heading or score, report failure...
            return False
