"""
Content Loader [Omission]
Version: 2.0

Loads and generates content from resource files.

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
import os.path
import pkg_resources


class ContentLoader(object):
    """
    Loads content from the content file, parses it, and enables
    random retrieval of passages.
    """

    def __init__(self):
        """
        Open the file and load the contents in.
        """
        # Seed random.
        random.seed()
        # Start tracking the last given index.
        self._index = 0
        # Load the content from the file into an array.
        path = pkg_resources.resource_filename(
            __name__,
            os.path.join(os.pardir, 'resources', 'content', 'content.txt')
        )

        with open(path, 'rt', encoding='utf-8') as content_file:
            raw_content = content_file.read()

        # Passages are separated by double newlines (blank lines).
        self._content = re.split(r'\n\n', raw_content)
        # Shuffle the content.
        self.reshuffle()

    def get_next(self):
        """
        Get a random passage from the file.
        :return: a string of content
        """
        # If we've overshot the length of the array (unlikely)...
        if self._index >= len(self._content):
            self.reshuffle()
        else:
            # We increment first.
            self._index += 1

        # Return the item before our current index position.
        return self._content[self._index - 1]

    def reshuffle(self, restart=True):
        """
        Reshuffle the content and optionally restart our walk through it.
        :return: None
        """
        random.shuffle(self._content)
        if restart:
            self._index = 0
