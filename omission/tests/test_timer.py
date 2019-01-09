"""
Tests: Game Timer [Omission]
Version: 2.0

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

from omission.game.timer import GameTimer


def test_finite_runs():
    """
    Ensure that the timer runs.
    """

    duration = 10
    iterations = 0
    completed = False

    def tick():
        nonlocal iterations
        iterations += 1

    def done():
        nonlocal completed, iterations
        iterations += 1
        completed = True

    timer = GameTimer(duration, lambda x: x, gameover_callback=done, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not completed:
        pass

    assert iterations == duration
    assert completed


def test_finite_lap():
    """
    Ensure the laps work as expected.
    """

    duration = 20
    lap_at = 11
    iterations = 0
    marked = False
    completed = False

    def tick():
        nonlocal iterations
        iterations += 1

    def done():
        nonlocal completed, iterations
        iterations += 1
        completed = True

    timer = GameTimer(duration, lambda x: x, gameover_callback=done, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not completed:
        if not marked and iterations == lap_at:
            timer.mark_lap()
            marked = True

    assert timer.since_lap() == duration - lap_at


def test_finite_add_time():
    """
    Test adding time to the clock.
    """

    duration = 20
    iterations = 0
    add = 5
    completed = False
    added = False

    def tick():
        nonlocal iterations
        iterations += 1

    def done():
        nonlocal completed, iterations
        iterations += 1
        completed = True

    timer = GameTimer(duration, lambda x: x, gameover_callback=done, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not completed:
        if not added and iterations == duration / 2:
            timer.add_time(add)
            added = True

    assert iterations == duration + add


def test_finite_remove_time():
    """
    Test removing time from the clock.
    """

    duration = 20
    remove = 5
    iterations = 0
    completed = False
    removed = False

    def tick():
        nonlocal iterations
        iterations += 1

    def done():
        nonlocal completed, iterations
        iterations += 1
        completed = True

    timer = GameTimer(duration, lambda x: x, gameover_callback=done, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not completed:
        if not removed and iterations == duration / 2:
            timer.remove_time(remove)
            removed = True

    assert iterations == duration - remove


def test_finite_time():
    """
    Test the getters of a finite timer.
    """

    duration = 20
    check_at = duration / 2
    iterations = 0
    completed = False
    checked = False

    def tick():
        nonlocal iterations
        iterations += 1

    def done():
        nonlocal completed, iterations
        iterations += 1
        completed = True

    timer = GameTimer(duration, lambda x: x, gameover_callback=done, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not completed:
        if not checked and iterations == check_at:
            # Pause the timer, to ensure our results are accurate
            timer.stop()
            # Check the seconds remaining
            assert timer.get_seconds() == duration - check_at
            # Check the percentage remaining
            assert timer.get_remaining_percent() == (check_at / duration) * 100
            # Yes, we checked. Don't do it again.
            checked = True
            # Resume the timer
            timer.start()

    assert timer.get_seconds() == 0
    assert timer.get_remaining_percent() == 0


def test_infinite_time():
    """
    Test the getters of an infinite timer.
    """

    check_at = 20
    iterations = 0
    checked = False

    def tick():
        nonlocal iterations
        iterations += 1

    timer = GameTimer(0, lambda x: x, tick_callback=tick, tick_duration=0.01)
    timer.start()

    while not checked:
        if iterations == check_at:
            # Stop the timer, to ensure our results are accurate.
            timer.stop()
            # Check the seconds elapsed
            assert timer.get_seconds() == check_at
            # Check the percentage is always 100%
            assert timer.get_remaining_percent() == 100
            # Yes, we checked. Don't do it again.
            checked = True
            # Don't resume the timer. We're done.

