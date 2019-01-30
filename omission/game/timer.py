"""
Game Timer [Omission]
Version: 2.0

Threaded game timer.

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

from threading import Timer


class GameTimer(object):
    """
    The timer object for a game round.
    """

    def __init__(self, duration: int, life_signal, gameover_callback=None, tick_callback=None, tick_duration=1.0):
        """
        Create a new GameTimer
        :param duration: duration in seconds. If 0, infinite until stopped.
        :param life_signal: The signal that calls for the timer to stop.
        :param gameover_callback: The function to call when the timer is done.
        :param tick_callback: The function to call on each tick.
        :param tick_duration: the duration of each tick (default 1.0 second)
        """

        self.duration = duration
        self.tick_length = tick_duration
        self.gameover_callback = gameover_callback
        self.tick_callback = tick_callback

        # The self._timer object is defined by self.start()
        self._timer = None

        # The number of seconds that have elapsed
        self.elapsed = 0
        # The last lap time. Used for tracking time between answers.
        self.lap = 0
        # Death flag
        self.alive = True

        # Register death function with the given lifespan signal.
        life_signal(self.die)

    def _timer_step(self):
        """
        Fires every second, updating the timer object.
        :return: None
        """
        self.elapsed += 1
        if self.duration > 0 and self.elapsed >= self.duration:
            self._timer_done()
        else:
            # If there's still time left...
            if self.tick_callback:
                self.tick_callback()
            # Elapse another second.
            self.start()

    def _timer_done(self):
        """
        The timer is finished.
        :return: None
        """
        if self.gameover_callback:
            self.gameover_callback()

    @property
    def remaining_percent(self):
        """
        :return: the number of seconds in the timer as a percentage.
        """
        # For finite timers...
        if self.duration > 0:
            return 100 - int(self.elapsed / self.duration * 100)
        # Otherwise, if this is an infinite timer...
        else:
            # Always return 100%
            return 100

    @property
    def seconds(self):
        """
        :return: the remaining number of seconds in a finite timer OR
        the number of seconds elapsed in an infinite timer.
        """
        # For finite timers...
        if self.duration > 0:
            return self.duration - self.elapsed
        # Otherwise, if this is an infinite timer...
        else:
            return self.elapsed

    def add_time(self, seconds):
        """
        :param seconds: number of seconds to add to timer
        :return: None
        """
        self.elapsed -= seconds
        if self.elapsed < 0:
            self.elapsed = 0

    def remove_time(self, seconds):
        """
        :param seconds: number of seconds to remove from the timer
        :return: None
        """
        self.elapsed += seconds
        # Elapsed should never be greater than the finite timer's max
        if self.duration > 0 and self.elapsed >= self.duration:
            self.elapsed = self.duration

    def mark_lap(self):
        """
        Hit the lap button on the stopwatch.
        :return: None
        """
        self.lap = self.elapsed

    def since_lap(self):
        """
        :return: the number of seconds elapsed since last lap
        """
        return self.elapsed - self.lap

    def reset(self):
        """
        Reset the timer
        :return: None
        """
        self.elapsed = 0

    def stop(self):
        """
        Stop the timer without resetting anything.
        :return: None
        """
        if self._timer:
            self._timer.cancel()
        self._timer = None

    def start(self):
        """
        Start/resume the timer.
        :return:
        """
        self._timer = None
        if not self._timer:
            self._timer = Timer(self.tick_length, self._timer_step)
        if self.alive:
            self._timer.start()

    def die(self):
        """
        Order the timer to die.
        :return: None
        """
        self.alive = False
