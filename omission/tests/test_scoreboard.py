"""
Tests: Scoreboard [Omission]
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
import re

from omission.data.scoreboard import Scoreboards, Scoreboard

random.seed()
SAMPLE_NAMES = ["Gallus", "Ocellus", "Silverstream", "Yona", "Sandbar", "Smoulder"]
SAMPLE_GAME_ROUND_SETTINGS = "I:0:0:0:0:0"
MIN_SCORE = 100
MAX_SCORE = 10000


def generate_sample_data(items=Scoreboard.retain):
    sample_data = []
    # Generate n random scores.
    for i in range(0, items):
        sample_data.append(
            (
                random.randint(MIN_SCORE, MAX_SCORE),
                SAMPLE_NAMES[random.randint(0, len(SAMPLE_NAMES) - 1)]
            )
        )
    return sample_data


def generate_sample_scoreboard(data=None, items=Scoreboard.retain, game_round_settings=SAMPLE_GAME_ROUND_SETTINGS):
    if not data:
        # Generate enough sample data to fill up the scoreboard
        data = generate_sample_data(items)

    scoreboard = Scoreboard(game_round_settings)

    for d in data:
        scoreboard.add_score(d[0], d[1])

    return scoreboard


def test_scoreboard_add_and_get():
    sample_data = generate_sample_data()
    scoreboard = generate_sample_scoreboard(data=sample_data)

    sample_data = sorted(sample_data, key=lambda x: x[0])

    scores = scoreboard.get_scores()
    scores = sorted(scores, key=lambda x: x[0])

    # Ensure the sample data matches what's in the scoreboard
    for (score, sample) in zip(scores, sample_data):
        assert score[0] == sample[0]
        assert score[1] == sample[1]


def test_scoreboard_sort():
    scoreboard = generate_sample_scoreboard()

    scores = scoreboard.get_scores()
    scores_manual_sorted = sorted(scores, key=lambda x: x[0], reverse=True)

    # Ensure the data was sorted when we got it.
    for (score, sample) in zip(scores, scores_manual_sorted):
        assert score[0] == sample[0]
        assert score[1] == sample[1]


def test_scoreboard_datastring():
    # Create a scoreboard and retrieve its scores and datastring
    scoreboard = generate_sample_scoreboard()
    scores = scoreboard.get_scores()
    datastring = scoreboard.datastring

    frags = datastring.splitlines()

    # Validate the top line of the datastring
    assert frags[0] == f'SCO={scoreboard.gameround_datastring}'
    # Validate the scores in the datastring
    for i, s in enumerate(scores):
        assert frags[i+1] == f':{s[0]}:{s[1]}'


def test_scores_parse():
    sample_scoreboard = generate_sample_scoreboard()
    test_scoreboard = Scoreboard(SAMPLE_GAME_ROUND_SETTINGS)
    datastrings = sample_scoreboard.datastring.splitlines()
    for d in datastrings[1:]:
        assert test_scoreboard.parse_score(d)

    assert sample_scoreboard.datastring == test_scoreboard.datastring


def test_check_score():
    # Generate an empty scoreboard
    scoreboard = Scoreboard(SAMPLE_GAME_ROUND_SETTINGS)
    # Any score should be accepted if the scoreboard is empty
    assert scoreboard.check_score(MIN_SCORE - 1)

    # Generate a scoreboard with one empty slot
    scoreboard = generate_sample_scoreboard(items=Scoreboard.retain-1)
    # Any score should be accepted if the scoreboard has empty slots
    assert scoreboard.check_score(MIN_SCORE - 1)

    # Generate a full scoreboard
    scoreboard = generate_sample_scoreboard()
    # A score lower than all scores present should be rejected
    assert not scoreboard.check_score(MIN_SCORE - 1)
    # A score higher than another score (or all scores) present should be accepted
    assert scoreboard.check_score(MAX_SCORE + 1)


def test_invalid_board():
    # Attempt to access a non-existent board
    assert Scoreboards.get_scoreboard("DEADBEEF") is None


def test_valid_board():
    # Generate and store a test scoreboard
    test_board = Scoreboard(SAMPLE_GAME_ROUND_SETTINGS)
    Scoreboards.store_scoreboard(test_board)

    # Access and validate the scoreboard
    retrieved = Scoreboards.get_scoreboard(SAMPLE_GAME_ROUND_SETTINGS)
    assert retrieved.gameround_datastring == SAMPLE_GAME_ROUND_SETTINGS


def test_boards_datastring():
    # Define our patterns
    boarddata = re.compile(r'^SCO=[TSI][:\d]+\d$')
    scoredata = re.compile(r'^:\d+:\w+$')

    datastring = Scoreboards.datastring
    frags = datastring.splitlines()

    for f in frags:
        assert boarddata.match(f) or scoredata.match(f)


def test_boards_parse():
    # Ensure we don't have a scoreboard like the one we're parsing in
    Scoreboards.delete_scoreboard(SAMPLE_GAME_ROUND_SETTINGS)

    # Parse in the datastring for a sample scoreboard
    sample_scoreboard = generate_sample_scoreboard()
    datastring = sample_scoreboard.datastring
    for d in datastring.splitlines():
        assert Scoreboards.parse_datastring(d)

    # Ensure the data was correctly parsed and used to create a new board.
    board = Scoreboards.get_scoreboard(SAMPLE_GAME_ROUND_SETTINGS)
    assert board is not None
    assert board.datastring == sample_scoreboard.datastring



