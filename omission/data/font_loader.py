"""
Font Loader [Omission]
Version: 2.0

Loads fonts from resource directories.

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

import os.path
import pkg_resources

class FontLoader(object):
    """
    Loads the correct font based on settings.
    """

    def __init__(self):
        self.dyslexic_mode = False

        fontfolder = os.path.abspath(os.path.join(os.pardir, "omission", "resources", "font"))

        self.opendyslexic_bold = pkg_resources.resource_filename(
            __name__,
            os.path.join(
                fontfolder, "open-dyslexic", "OpenDyslexic-Bold.otf"
                )
            )

        self.opendyslexic_regular = pkg_resources.resource_filename(
            __name__,
            os.path.join(
                fontfolder, "open-dyslexic", "OpenDyslexic-Regular.otf"
                )
            )

        self.orbitron = pkg_resources.resource_filename(
            __name__,
            os.path.join(
                fontfolder, "orbitron", "orbitron-medium.otf"
                )
            )

        self.sourcesans_regular = pkg_resources.resource_filename(
            __name__,
            os.path.join(
                fontfolder, "source-sans-pro", "SourceSansPro-Regular.otf"
                )
            )

    def get_datastring(self):
        """
        Get the datastring for the FontLoader.
        """
        datastring = "DYS=" + str(int(self.dyslexic_mode)) + "\n"
        return datastring

    def set_dyslexic_mode(self, mode):
        """
        Set the dyslexic mode.
        """
        self.dyslexic_mode = mode

    def get_dyslexic_mode(self):
        """
        Get the dyslexic mode.
        """
        return self.dyslexic_mode

    def decorative(self):
        """
        Returns the path to the decorative font, usually Orbitron.
        """
        if self.dyslexic_mode:
            fontpath = self.opendyslexic_bold
        else:
            fontpath = self.orbitron
        return fontpath

    def passage(self):
        """
        Returns the path to the passage font, usually Source Sans Pro.
        """
        if self.dyslexic_mode:
            fontpath = self.opendyslexic_regular
        else:
            fontpath = self.sourcesans_regular
        return fontpath
