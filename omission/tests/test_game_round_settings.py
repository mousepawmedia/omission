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

from omission.data.game_round_settings import GameRoundSettings
from omission.data.data_enums import GameMode

def test_default_timed():
    timed1 = GameRoundSettings.default_timed()
    timed2 = GameRoundSettings.default_timed()
    assert timed1.mode == GameMode.Timed
    # Ensure the instances are distinct
    timed1.set_solution_pause(False)
    assert not timed1.solution_pause
    assert timed2.solution_pause


def test_default_survival():
    survival1 = GameRoundSettings.default_survival()
    survival2 = GameRoundSettings.default_survival()
    assert survival1.mode == GameMode.Survival
    # Ensure the instances are distinct.
    survival1.set_solution_pause(False)
    assert not survival1.solution_pause
    assert survival2.solution_pause


def test_default_infinite():
    infinite1 = GameRoundSettings.default_infinite()
    infinite2 = GameRoundSettings.default_infinite()
    assert infinite1.mode == GameMode.Infinite
    # Ensure the instances are distinct.
    infinite1.set_solution_pause(False)
    assert not infinite1.solution_pause
    assert infinite2.solution_pause