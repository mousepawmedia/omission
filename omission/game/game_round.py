"""
Game Round [Omission]
Version: 2.0

Generates and manages a single round of gameplay.

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

from omission.common.game_enums import GameMode, GameStatus
from omission.data.game_round_settings import GameRoundSettings
from omission.game.content_loader import ContentLoader
from omission.game.timer import GameTimer


class GameRound(object):
    """
    A single round of gameplay. Generates the content for the round and
    manages the score and gameplay dynamics
    """

    def __init__(self, settings: GameRoundSettings, life_signal,
                 gameover_callback=None, tick_callback=None):
        """
        Create a new gameplay round.
        :param settings: the settings for the game round
        :param life_signal:
        :param gameover_callback: the function to call when the game is over
        :param tick_callback: the function to call on every game tick
        """

        self._gameover_callback = gameover_callback
        self._tick_callback = tick_callback

        self._loader = ContentLoader()
        self._settings = settings

        # If we're playing Timed mode...
        if self.settings.mode == GameMode.Timed:
            # Create and hook up a finite timer.
            self._timer = GameTimer(self.settings.limit, life_signal, self.gameover, self.tick)
        # Otherwise, for all other modes...
        else:
            # Create and hook up an infinite timer.
            self._timer = GameTimer(0, life_signal, None, self.tick)

        # If we're playing Survival mode...
        if self.settings.mode == GameMode.Survival:
            # Create the life counter.
            self._lives = self.settings.limit

        # Flag whether we're paused
        self.paused = False
        # The current puzzle item
        self.item = None
        # The current attempt
        self.attempt = 0
        # The current score
        self.score = 0
        # The last item score
        self.item_score = 0
        # The current chain multiplier. Default 1.
        self.chain = 1

    def start_round(self):
        """
        Start the round.
        :return: None
        """
        # Load the first item.
        self.new_item()
        # Start the game timer.
        self._timer.start()

    def new_item(self):
        # Get a new item.
        self.item = ContentItem(self._loader.get_next())
        # Reset tries
        self.attempt = 0
        # Set a new lap on our timer (start of question)
        self._timer.mark_lap()

    def get_status(self):
        pass

    def get_puzzle(self):
        pass

    def get_tries(self):
        pass

    def answer(self):
        pass

    def calculate_item_score(self):
        pass

    def get_score(self):
        pass

    def get_soluiton(self):
        pass

    def pause(self):
        pass

    def is_paused(self):
        pass

    def resume(self):
        pass

    def gameover(self):
        pass

    def tick(self):
        pass
