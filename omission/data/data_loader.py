"""
Data Loader [Omission]
Version: 2.0

Loads scores and settings from files.

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

# Our data layout follows these conventions:
# DEF=T:3:2:3:1:30:3:1
# DEF=S:3:2:3:1:3
# DEF=I:3:2:3:1
# VOL=10
# DYS=1
# SCO=T:3:2:3:1:30:3:1
# :852:Fred
# :1936523:Jason
# :5832:Jarek
# :100:Bob
# SCO=T:5:2:3:1:30:3:1

import os.path

from appdirs import user_data_dir

from omission.common import constants
from omission.data.settings import Settings
from omission.data.scoreboard import Scoreboards


class DataLoader(object):
    """
    Statically load scores and other stored data from our config file.
    """

    directory = user_data_dir(constants.APP_NAME, constants.APP_AUTHOR)
    path = os.path.join(directory, "scores.data")

    def __init__(self):
        pass

    @classmethod
    def read_in(cls):
        try:
            with open(cls.path, 'r') as scorefile:
                rawdata = scorefile.readlines()
        except FileNotFoundError:
            # The file doesn't yet exist, that's fine. Carry on.
            pass

        for d in rawdata:
            if not Settings.parse_datastring(d):
                Scoreboards.parse_datastring(d)

    @classmethod
    def write_out(cls):
        # Create the folders, if necessary
        os.makedirs(cls.directory, 0x777, True)

        # Fetch the datastrings to write out
        data = ''
        data += Settings.datastring
        data += Scoreboards.datastring

        # Write out the data to a file.
        with open(cls.path, 'w') as scorefile:
            scorefile.write(data)
