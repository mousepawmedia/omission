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
from omission.game.game_item import GameItem


class GameRound(object):
    """
    A single round of gameplay. Generates the content for the round and
    manages the score and gameplay dynamics
    """

    def __init__(self, settings: GameRoundSettings, life_signal,
                 gameover_callback=None, tick_callback=None,
                 tick_duration: (float, int) = 1.0):
        """
        Create a new gameplay round.
        :param settings: the settings for the game round
        :param life_signal:
        :param gameover_callback: the function to call when the game is over
        :param tick_callback: the function to call on every game tick
        """

        self._gameover_callback = gameover_callback
        self._tick_callback = tick_callback

        self.loader = ContentLoader()
        self._settings = settings

        # If we're playing Timed mode...
        if self._settings.mode == GameMode.Timed:
            # Create and hook up a finite timer.
            self._timer = GameTimer(self._settings.limit, life_signal, self.gameover, self.tick, tick_duration)
        # Otherwise, for all other modes...
        else:
            # Create and hook up an infinite timer.
            self._timer = GameTimer(0, life_signal, None, self.tick)

        # We'll default to -1 for infinite lives
        self._lives = -1

        # If we're playing Survival mode...
        if self._settings.mode == GameMode.Survival:
            # Create the life counter.
            self._lives = self._settings.limit

        # Flag whether we're paused
        self._paused = False
        # The current puzzle item. Generate one to start with.
        self.item = GameItem(self.loader, self._settings.tries)
        # The current score
        self._score = 0
        # The last item score
        self._item_score = 0
        # The current chain multiplier. Default 1.
        self._chain = 1

    def start_round(self):
        """
        Start the round.
        :return: None
        """
        # Load the first item, if nothing is already loaded.
        if not self.item:
            self.new_item()
        # Start the game timer.
        self._timer.start()

    def new_item(self):
        """
        Load a new game item into the round.
        :return: None
        """
        # Get a new item.
        self.item = GameItem(self.loader, self._settings.tries)
        # Set a new lap on our timer (start of question)
        self._timer.mark_lap()

    @property
    def lives(self):
        """
        :return: the number of lives remaining (-1 if infinite)
        """
        return self._lives

    @property
    def percent_remaining(self):
        if self._settings.mode == GameMode.Timed:
            return self._timer.remaining_percent
        elif self._settings.mode == GameMode.Survival:
            return (self._lives / self._settings.limit) * 100
        elif self._settings.mode == GameMode.Infinite:
            return 100

    @property
    def seconds(self):
        """
        :return: time remaining (in Timed mode) or time elapsed
        """
        return self._timer.seconds

    @property
    def mode(self):
        """
        :return: the GameMode of the round
        """
        return self._settings.mode

    @property
    def score(self):
        return self._score

    @property
    def item_score(self):
        return self._item_score

    @property
    def chain(self):
        return self._chain

    @property
    def solution(self):
        return self.item.solution

    @property
    def answer(self):
        return self.item.answer

    @property
    def removals(self) -> str:
        """
        Retrieves the removals as a string, accounting for when the hint is supposed to be displayed
        :return: string showing removal count, or "?", as appropriate
        """
        if (self.item.tries_used + 1) >= self._settings.count_at:
            return str(self.item.removals)
        else:
            return "?"

    @property
    def puzzle(self):
        """
        Retrieves the puzzle, accounting for when the underscores (clue) are supposed to be displayed
        :return: puzzle, with or without underscores as appropriate
        """
        # We must account for the off-by-one: in settings, first try is 1; in item, first try is 0
        if (self.item.tries_used + 1) >= self._settings.clue_at:
            return self.item.get_puzzle(underscores=True)
        else:
            return self.item.get_puzzle(underscores=False)

    def check_answer(self, letter: str, progress=False):
        """
        Pass answer in.
        :return: GameStatus
        """
        # If the answer is correct...
        if self.item.check_answer(letter):

            # Figure out the score before we do ANYTHING else
            self.calculate_item_score()

            if self.mode == GameMode.Timed:
                # Add five seconds to the time.
                # Be sure to do this AFTER calculating score!
                self._timer.add_time(self._settings.bonus)

            if progress:
                # Get the next item.
                self.new_item()

            # Indicate the answer was correct
            return GameStatus.Correct

        # Otherwise, if the answer was incorrect...
        else:
            # In Timed mode, give penalty
            if self.mode == GameMode.Timed:
                self._timer.remove_time(self._settings.penalty)

            # Expire any chains.
            self._chain = 1

            # If we've still got tries left...
            if self.item.has_tries:
                # Indicate the answer was incorrect
                return GameStatus.Incorrect

            # Otherwise, if we've used all our tries...
            else:
                # No attempts on this puzzle left.

                # If we're on Survival mode...
                if self.mode == GameMode.Survival:
                    # Remove a life
                    self._lives -= 1
                    # If we're out of lives
                    if self._lives <= 0:
                        self.gameover()

                if progress:
                    self.new_item()

                # Indicate the answer was incorrect AND skipped.
                return GameStatus.Skipped

    def calculate_item_score(self):
        """
        Calculate the item score and add it to the main score.
        :return: None
        """
        # Stop time, to prevent processing time from leaking into score.
        self._timer.stop()

        # Get the number of letters that were removed, but don't go above 10.
        letters = min(self.item.removals, 10)

        # Calculate the base score based on letters removed
        # 1 letter = 100 points, 5 letters = 60 points, 10+ letters = 10 points
        base_score = 100-((letters-1)*10)

        # Calculate the attempt bonus: +1x for each remaining try (minimum 1x, to prevent zeroing out score)
        try_bonus = max(self.item.tries_left + 1, 1)

        # Calculate the time bonus: 5s= +1x, 4s = +2x, ... 1s = +5x (no bonus for 6+)
        time = max(self._timer.since_lap(), 6)
        time_bonus = 6 - time

        # Calculate the item score using bonuses and current chain
        self._item_score = base_score * (try_bonus + time_bonus) * self._chain
        # Add to the main score
        self._score += self._item_score

        # Update the chain bonus for NEXT time (if claimed!)
        if time < self._settings.chain:
            self._chain += 1
        else:
            self._chain = 1

        # Resume time
        self._timer.start()

    @property
    def paused(self):
        """
        :return: True if paused, else False
        """
        return self._paused

    def pause(self):
        """
        Pause the game
        :return: None
        """
        if not self._paused:
            self._paused = True
            self._timer.stop()

    def resume(self):
        """
        Unpause the game
        :return: None
        """
        if self._paused:
            self._paused = False
            self._timer.start()

    def gameover(self):
        """
        End the game, calling the gameover callback function, and passing the final score to it.
        :return: None
        """
        # Stop the timer
        self._timer.stop()
        # If we have a gameover callback, call it now...
        if self._gameover_callback:
            self._gameover_callback(self._score)

    def tick(self):
        """
        Runs every second
        :return: None
        """
        # If we had a chain, but it should have expired...
        if self._chain > 1 and self._timer.since_lap() >= self._settings.chain:
            self._chain = 1
        # If we have a tick callback, call it now...
        if self._tick_callback:
            self._tick_callback()

