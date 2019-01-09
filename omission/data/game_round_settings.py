"""
Game Round Settings [Omission]
Version: 2.0

The settings for a specific round of gameplay.

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

import re

from omission.common.game_enums import GameMode


class GameRoundSettings(object):
    """
    Contains the settings for a single round of gameplay.
    """

    pattern_datastring_settings_timed = re.compile(r'^DEF=T[:\d]+')
    pattern_datastring_settings_survial = re.compile(r'^DEF=S[:\d]+')
    pattern_datastring_settings_infinite = re.compile(r'^DEF=I[:\d]+')

    def __init__(self):
        # The gameplay mode for the round.
        self.mode = GameMode.Timed
        # The timer duration in timed mode OR the number of lives.
        self.limit = 30
        # The max number of attempts before discarding a puzzle.
        self.tries = 3
        # The try number to display the clue at (underscores)
        self.clue_at = 2
        # The try number to display the count at
        self.count_at = 1
        # The time to add to the clock on a correct guess in Timed mode
        self.bonus = 3
        # The time to remove from the clock on a wrong guess in Timed mode
        self.penalty = 1
        # The time under which we have to answer to extend the chain
        self.chain = 2
        # Whether to pause on solution
        self.solution_pause = True

    def set_timed(self, time=30, bonus=2, penalty=1, tries=3, count_at=1, clue_at=3, chain=2, solution_pause=True):
        """
        Switch to Timed mode
        :param time: timer duration in seconds
        :param bonus: seconds added to timer on correct guess
        :param penalty: seconds removed from timer on incorrect guess
        :param tries: attempts before puzzle is discarded
        :param count_at: tries until "letters removed" clue shown
        :param clue_at: tries until underscores shown
        :param chain: seconds until chain expires
        :param solution_pause: True to show, False to skip solution
        :return: None
        """
        self.mode = GameMode.Timed
        self.limit = time
        self.bonus = bonus
        self.penalty = penalty
        self.tries = tries
        # If > tries, hint won't ever be displayed
        # If 0, hint will always be displayed
        self.count_at = count_at
        self.clue_at = clue_at
        self.chain = chain
        self.solution_pause = solution_pause

    @classmethod
    def default_timed(cls):
        """
        Creates a default Timed game round settings object instance
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_timed()
        return r

    def set_survival(self, lives=5, tries=1, count_at=1, clue_at=3, chain=2, solution_pause=True):
        """
        Switch to Survival mode
        :param lives: lives per round
        :param tries: attempts before puzzle is discarded
        :param count_at: tries until "letters removed" clue shown
        :param clue_at: tries until underscores shown
        :param chain: seconds until chain expires
        :param solution_pause: True to show, False to skip solution
        :return: None
        """
        self.mode = GameMode.Survival
        self.limit = lives
        self.tries = tries
        # If > tries, hint won't ever be displayed
        # If 0, hint will always be displayed
        self.count_at = count_at
        self.clue_at = clue_at
        self.chain = chain
        self.solution_pause = solution_pause

    @classmethod
    def default_survival(cls):
        """
        Creates a default Survival game round settings object instance
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_survival()
        return r

    def set_infinite(self, tries=3, count_at=1, clue_at=3, chain=2, solution_pause=True):
        """
        Switch to Infinite mode
        :param tries: attempts before puzzle is discarded
        :param count_at: tries until "letters removed" clue shown
        :param clue_at: tries until underscores shown
        :param chain: seconds until chain expires
        :param solution_pause: True to show, False to skip solution
        :return: None
        """
        self.mode = GameMode.Infinite
        self.tries = tries
        # If > tries, hint won't ever be displayed
        # If 0, hint will always be displayed
        self.count_at = count_at
        self.clue_at = clue_at
        self.chain = chain
        self.solution_pause = solution_pause

    @classmethod
    def default_infinite(cls):
        """
        Creates a default Timed game round settings object instance
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_infinite()
        return r

    @property
    def datastring(self):
        """
        :return: the datastring representing the GameRoundSettings object
        """
        output = ""

        # T:time:bonus:penalty:tries:hint:clue:chain:solution
        if self.mode == GameMode.Timed:
            output += "T:" + \
                str(self.limit) + ":" + \
                str(self.bonus) + ":" + \
                str(self.penalty) + ":" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(self.chain) + ":" + \
                str(int(self.solution_pause))
        # S:lives:tries:hint:clue:chain:solution
        elif self.mode == GameMode.Survival:
            output += "S:" + \
                str(self.limit) + ":" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(self.chain) + ":" + \
                str(int(self.solution_pause))
        # I:tries:hint:clue:chain:solution
        elif self.mode == GameMode.Infinite:
            output += "I:" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(self.chain) + ":" + \
                str(int(self.solution_pause))
        return output

    def parse_datastring(self, datastring: str):
        """
        Redefine the game round settings based on a datastring
        :param datastring: the datastring to extract the settings from
        :return: True if datastring successfully parsed, else False
        """
        if datastring[:4] == 'DEF=':
            datastring = datastring[4:]
            data = datastring.split(':')

            # Validate and parse Timed gameround datastring
            if data[0] == 'T' and len(data) == 9:
                try:
                    self.mode = GameMode.Timed
                    self.limit = int(data[1])
                    self.bonus = int(data[2])
                    self.penalty = int(data[3])
                    self.tries = int(data[4])
                    self.count_at = int(data[5])
                    self.clue_at = int(data[6])
                    self.chain = int(data[7])
                    self.solution_pause = bool(int(data[8]))
                except (ValueError, IndexError):
                    return False
                else:
                    return True
            # Validate and parse Survival gameround datastring
            elif data[0] == 'S' and len(data) == 7:
                try:
                    self.mode = GameMode.Survival
                    self.limit = int(data[1])
                    self.tries = int(data[2])
                    self.count_at = int(data[3])
                    self.clue_at = int(data[4])
                    self.chain = int(data[5])
                    self.solution_pause = bool(int(data[6]))
                except (ValueError, IndexError):
                    return False
                else:
                    return True
            # Validate and parse Infinite gameround datastring
            elif data[0] == 'I' and len(data) == 6:
                try:
                    self.mode = GameMode.Infinite
                    self.tries = int(data[1])
                    self.count_at = int(data[2])
                    self.clue_at = int(data[3])
                    self.chain = int(data[4])
                    self.solution_pause = bool(int(data[5]))
                except (ValueError, IndexError):
                    return False
                else:
                    return True

        # in any other case, datastring wasn't valid
        return False
