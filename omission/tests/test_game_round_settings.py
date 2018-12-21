"""
Tests: Game Round Settings [Omission]
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

import random

from omission.data.game_round_settings import GameRoundSettings
from omission.data.game_enums import GameMode

# Initialize the random number generator.
random.seed()

def test_default_timed():
    """
    Validate that a distinct GameRoundSettings object with mode Timed is generated by `default_timed()`
    """
    timed1 = GameRoundSettings.default_timed()
    timed2 = GameRoundSettings.default_timed()
    # Ensure the mode is correct
    assert timed1.mode == GameMode.Timed
    # Ensure the instances are distinct
    timed1.solution_pause = False
    assert not timed1.solution_pause
    assert timed2.solution_pause


def test_default_survival():
    """
    Validate that a distinct GameRoundSettings object with mode Survival is generated by `default_survival()`
    """
    survival1 = GameRoundSettings.default_survival()
    survival2 = GameRoundSettings.default_survival()
    # Ensure the mode is correct
    assert survival1.mode == GameMode.Survival
    # Ensure the instances are distinct.
    survival1.solution_pause = False
    assert not survival1.solution_pause
    assert survival2.solution_pause


def test_default_infinite():
    """
    Validate that a distinct GameRoundSettings object with mode Infinite is generated by `default_infinite()`
    """
    infinite1 = GameRoundSettings.default_infinite()
    infinite2 = GameRoundSettings.default_infinite()
    # Ensure the mode is correct
    assert infinite1.mode == GameMode.Infinite
    # Ensure the instances are distinct.
    infinite1.solution_pause = False
    assert not infinite1.solution_pause
    assert infinite2.solution_pause


def test_datastring_timed():
    """
    Validate that the Timed GameRoundSettings datastring follows the correct format.
    """
    timed = GameRoundSettings.default_timed()

    # Generate random values for settings.
    test_data = [random.randint(0, 20) for i in range(7)]
    test_data.append(random.randint(0, 1))

    # Load test data into object.
    timed.set_timed(
        time=test_data[0],
        bonus=test_data[1],
        penalty=test_data[2],
        tries=test_data[3],
        count_at=test_data[4],
        clue_at=test_data[5],
        chain=test_data[6],
        solution_pause=bool(test_data[7])
    )

    # Check that the object data matches the test data
    timed.time = test_data[0]
    timed.bonus = test_data[1]
    timed.penalty = test_data[2]
    timed.tries = test_data[3]
    timed.count_at = test_data[4]
    timed.clue_at = test_data[5]
    timed.chain = test_data[6]
    timed.solution_pause = bool(test_data[7])

    # Get datastring and split by colons
    frags = timed.datastring.split(':')

    # Check that the datastring matches the test data
    # T:time:bonus:penalty:tries:hint:clue:chain:solution
    assert frags[0] == 'T'
    assert frags[1] == str(test_data[0])
    assert frags[2] == str(test_data[1])
    assert frags[3] == str(test_data[2])
    assert frags[4] == str(test_data[3])
    assert frags[5] == str(test_data[4])
    assert frags[6] == str(test_data[5])
    assert frags[7] == str(test_data[6])
    assert frags[8] == str(test_data[7])
    assert len(frags) == 9


def test_datastring_survival():
    """
    Validate that the Survival GameRoundSettings datastring follows the correct format.
    """
    survival = GameRoundSettings()

    # Generate random values for settings.
    test_data = [random.randint(0, 20) for i in range(5)]
    test_data.append(random.randint(0, 1))

    # Load test data into object.
    survival.set_survival(
        lives=test_data[0],
        tries=test_data[1],
        count_at=test_data[2],
        clue_at=test_data[3],
        chain=test_data[4],
        solution_pause=bool(test_data[5])
    )

    # Get datastring and split by colons
    frags = survival.datastring.split(':')

    # Check that the object data matches the test data
    survival.lives = test_data[0]
    survival.tries = test_data[1]
    survival.count_at = test_data[2]
    survival.clue_at = test_data[3]
    survival.chain = test_data[4]
    survival.solution_pause = bool(test_data[5])

    # Check that the datastring matches the test data
    # S:lives:tries:hint:clue:chain:solution
    assert frags[0] == 'S'
    assert frags[1] == str(test_data[0])
    assert frags[2] == str(test_data[1])
    assert frags[3] == str(test_data[2])
    assert frags[4] == str(test_data[3])
    assert frags[5] == str(test_data[4])
    assert frags[6] == str(test_data[5])
    assert len(frags) == 7


def test_datastring_infinite():
    """
    Validate that the Infinite GameRoundSettings datastring follows the correct format.
    """
    infinite = GameRoundSettings.default_infinite()

    # Generate random values for settings.
    test_data = [random.randint(0, 20) for i in range(4)]
    test_data.append(random.randint(0, 1))

    # Load test data into object.
    infinite.set_infinite(
        tries=test_data[0],
        count_at=test_data[1],
        clue_at=test_data[2],
        chain=test_data[3],
        solution_pause=bool(test_data[4])
    )

    # Check that the object data matches the test data
    infinite.tries = test_data[0]
    infinite.count_at = test_data[1]
    infinite.clue_at = test_data[2]
    infinite.chain = test_data[3]
    infinite.solution_pause = bool(test_data[4])

    # Get datastring and split by colons
    frags = infinite.datastring.split(':')

    # Check that the datastring matches the object data
    # I:tries:hint:clue:chain:solution
    assert frags[0] == 'I'
    assert frags[1] == str(test_data[0])
    assert frags[2] == str(test_data[1])
    assert frags[3] == str(test_data[2])
    assert frags[4] == str(test_data[3])
    assert frags[5] == str(test_data[4])
    assert len(frags) == 6


def test_datastring_parse():
    """
    Validate that a datastring is parsed correctly.
    """
    survival = GameRoundSettings.default_survival()
    test = GameRoundSettings.default_infinite()
    assert test.parse_datastring('DEF=' + survival.datastring)
    assert test.datastring == survival.datastring
