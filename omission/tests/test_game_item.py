"""
Tests: Game Item [Omission]
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

from omission.game.game_item import GameItem
from omission.game.content_loader import ContentLoader

def test_puzzle_generation():
    loader = ContentLoader()
    for i in range(loader.total_items):
        item = GameItem(loader)
        original = item._original.upper()
        rebuilt = item._puzzle.replace('_', item._letter).upper()
        assert item._removals == item._puzzle.find('_')
        assert original == rebuilt

def test_puzzle_obfuscation():
    loader = ContentLoader()
    for i in range(loader.total_items):
        item = GameItem(loader)
        puzzle = item.get_puzzle(underscores=False)
        assert not puzzle[0].islower()
        assert not puzzle[0] == ' '
        assert puzzle.find("  ") == -1

def test_puzzle_obfuscation_safe():
    """
    Ensure the puzzle obfuscation does not damage the actual letters.
    """
    loader = ContentLoader()
    for i in range(loader.total_items):
        item = GameItem(loader)
        original = item.get_solution().upper()
        puzzle = item.get_puzzle(underscores=False).upper()
        original = original.replace(' ', '')
        puzzle = puzzle.replace(' ', '')
        original.replace(item.get_answer(), '')
        assert original == puzzle
