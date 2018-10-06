"""
Content Item [Omission]
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

class ContentItem(object):
    """
    A single content item.
    """

    def __init__(self, passage):
        """
        Generates a new puzzle item from the given passage.
        """
        # Store the input passage as the original.
        self._original = passage
        # Store the number of instances of the letter we remove.
        self._removals = 0

        # Prepare random.
        random.seed()

        # There is an occasional glitch where no letters are removed.
        # This is a safeguard against that.
        while self._removals == 0:
            # Generate the puzzle by removing all instances of the
            # selected letter from the passage. Be sure to retain the
            # original passage for reference.
            self._puzzle = ""
            # Select a random letter from the passage.
            self._letter = random.choice(self._original)
            while not self._letter.isalpha():
                self._letter = random.choice(self._original).lower()

            # We do this manually in a loop for the express purpose of
            # tracking the number of removals we did.
            for char in self._original:
                # We replace all removed letters with underscores,
                # incrementing our removal counter for each removed.
                if char.lower() == self._letter:
                    self._puzzle += "_"
                    self._removals += 1
                # All other characters are copied.
                else:
                    self._puzzle += char

    def get_puzzle(self, underscores=False):
        """
        Return the puzzle with or without underscores.
        """
        # If requested, return the puzzle with the underscores still in place.
        if underscores:
            return self._puzzle
        # Otherwise, return the puzzle with underscores removed.
        else:
            # Make a copy without the underscores.
            puzzle = self._puzzle.replace("_", "")
            # Remove double spaces to conceal missing words.
            puzzle = puzzle.replace("  ", " ")
            # If we lead with a space...
            if puzzle[0] == " ":
                puzzle = puzzle[1:]
            # Capitalize the first letter without changing the other letters.
            puzzle = puzzle[0].upper() + puzzle[1:]
            # Return the modified form.
            return puzzle

    def get_answer(self):
        """
        Return the correct letter.
        """
        return self._letter

    def get_solution(self):
        """
        Return the complete passage.
        """
        return self._original

    def check_answer(self, letter):
        """
        Check if the given letter is the correct answer.
        """
        return letter.lower() == self._letter

    def get_removals(self):
        """
        Return the number of instances of the letter that were removed.
        """
        return self._removals
