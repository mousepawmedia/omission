"""
Content Loader [Omission]
"""

import random
import re
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
        path = pkg_resources.resource_filename(__name__, "../resources/content/content.txt")
        with open(path) as contentfile:
            rawcontent = contentfile.read()
        # Passages are separated by double newlines (blank lines).
        self._content = re.split(r'\n\n', rawcontent)
        # Shuffle the content.
        self.reshuffle()

    def get_next(self):
        """
        Get a random passage from the file.
        """
        # If we've overshot the length of the array (unlikely)...
        if self._index >= len(self._content):
            self.reshuffle()
        else:
            # We increment first.
            self._index += 1

        # Return the item before our current index position.
        return self._content[self._index-1]

    def reshuffle(self, restart=True):
        """
        Reshuffle the content and optionally restart our walk through it.
        """
        # Reshuffle the array of content.
        random.shuffle(self._content)
        if restart:
            self._index = 0
