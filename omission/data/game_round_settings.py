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

from omission.data.data_enums import GameMode


class GameRoundSettings(object):
    """
    Contains the settings for a single round of gameplay.
    """

    def __init__(self):
        # The gameplay mode for the round.
        self.mode = GameMode.Timed
        # The timer length in timed mode OR the number of lives.
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

    def set_timed(self, time=30, bonus=2, penalty=1, tries=3):
        """
        Switch to Timed mode
        :param time: timer length in seconds
        :param bonus: seconds added to timer on correct guess
        :param penalty: seconds removed from timer on incorrect guess
        :param tries: attempts before puzzle is discarded
        :return: None
        """
        self.mode = GameMode.Timed
        self.limit = time
        self.bonus = bonus
        self.penalty = penalty
        self.tries = tries

    @classmethod
    def default_timed(cls):
        """
        Creates a default Timed game round settings object
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_timed()
        return r

    def set_survival(self, lives=5, tries=1):
        """
        Switch to Survival mode
        :param lives: lives per round
        :param tries: attempts before puzzle is discarded
        :return: None
        """
        self.mode = GameMode.Survival
        self.limit = lives
        self.tries = tries

    @classmethod
    def default_survival(cls):
        """
        Creates a default Survival game round settings object
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_survival()
        return r

    def set_infinite(self, tries=3):
        """
        Switch to Infinite mode
        :param tries: attempts before puzzle is discarded
        :return: None
        """
        self.mode = GameMode.Infinite
        self.tries = tries

    @classmethod
    def default_infinite(cls):
        """
        Creates a default Timed game round settings object
        :return: GameRoundSettings
        """
        r = GameRoundSettings()
        r.set_infinite()
        return r

    # NOTE: While pure setters may not be perfectly Pythonic, it ensures the interface is consistent.
    def set_solution_pause(self, solution_pause=True):
        """
        Set whether to show the solution.
        :param solution_pause: True to show, False to skip solution
        :return: None
        """
        self.solution_pause = solution_pause

    def set_chain(self, chain=2):
        """
        Set the cutoff time for chain bonuses
        :param chain: seconds until chain expires
        :return: None
        """
        self.chain = chain

    def set_clues(self, count_at=1, clue_at=3):
        """
        Define the clue timings
        If > tries, it won't ever be displayed
        If 0, it will always be displayed
        :param count_at: tries until "letters removed" clue shown
        :param clue_at: tries until underscores shown
        :return: None
        """
        self.count_at = count_at
        self.clue_at = clue_at

    def __str__(self):
        """
        :return: the datastring representing the GameRoundSettings object
        """
        output = ""

        # DEF=T:time:bonus:penalty:tries:hint:clue:chain:solution
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
        # DEF=S:lives:tries:hint:clue:chain:solution
        elif self.mode == GameMode.Survival:
            output += "S:" + \
                str(self.limit) + ":" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(self.chain) + ":" + \
                str(int(self.solution_pause))
        # DEF=I:tries:hint:clue:chain:solution
        elif self.mode == GameMode.Infinite:
            output += "I:" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(self.chain) + ":" + \
                str(int(self.solution_pause))
        return output