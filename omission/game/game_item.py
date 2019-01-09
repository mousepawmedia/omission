"""
Game Item [Omission]
Version: 2.0

A single 'question' (content item) within a round.

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

from omission.game.content_loader import ContentLoader

class GameItem(object):

    def __init__(self, loader: ContentLoader):
        """
        Generate a new puzzle using the given content loader.
        :param loader: the ContentLoader to use
        """
        # The original passage (solution)
        self._original = loader.get_next()
        # The passage with a letter removed
        self._puzzle = ""
        # The number of instances of the letter we remove.
        self._removals = 0

        # Prepare random
        random.seed()

        # There is an occasional glitch where no letters are removed.
        # This is a safeguard against that.
        while self._removals == 0:
            # Generate the puzzle by removing all instances of the
            # selected letter from the passage. Be sure to retain the
            # original passage for reference
            self._letter = random.choice(self._original)
            while not self._letter.isalpha():
                self._letter = random.choice(self._original).lower()

            # We do this manually in a loop for the express purpose of
            # tracking the number of removals we did.
            for char in self._original:
                # We replace all removed letters with underscores,
                # incrementing our removal counter for each removed.
                if char.lower() == self._letter:
                    self._puzzle += '_'
                    self._removals += 1
                # All other characters are copied
                else:
                    self._puzzle += char

    def get_puzzle(self, underscores=False):
        """
        Return the puzzle with or without underscores.
        :param underscores: whether to include the underscores
        :return: the puzzle as a string
        """
        # If requested, return the puzzle with the underscores still in place.
        if underscores:
            return self._puzzle
        # Otherwise, strip the underscores and return.
        else:
            # Make a copy without the underscores.
            puzzle = self._puzzle.replace('_', '')
            # Remove double spaces to conceal missing words.
            puzzle = puzzle.replace('  ', ' ')
            # If we lead with a space, remove it.
            if puzzle[0] == ' ':
                puzzle = puzzle[1:]
            # Capitalize the first letter without changing the other letters.
            puzzle = puzzle[0].upper() + puzzle[1:]
            # Return the obfuscated form.
            return puzzle

    def get_answer(self):
        """
        :return: the missing letter
        """
        return self._letter

    def get_solution(self):
        """
        :return: the complete passage
        """
        return self._original

    def check_answer(self, letter: str):
        """
        Check if the given letter is the correct answer.
        :return: True if correct, else False
        """
        return letter.lower() == self._letter

    def get_removals(self):
        """
        :return: the number of instances of the letter that were removed
        """
        return self._removals
