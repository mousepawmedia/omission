"""
Settings [Omission]
Version: 2.0

Contains the static instances of all the loaded game settings.

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

import textwrap
import re

from omission.common.classproperty import classproperty
from omission.data.game_round_settings import GameRoundSettings

class Settings(object):
    """
    Contains static instances of the settings for each mode.
    """

    # The currently loaded settings for each game round.
    timed = GameRoundSettings.default_timed()
    survival = GameRoundSettings.default_survival()
    infinite = GameRoundSettings.default_infinite()

    # The sound volume (0-10)
    vol = 10
    # Whether to use the dyslexia font
    dys = False

    # The regex for settings datastrings
    pattern_datastring_settings_volume = re.compile(r'^VOL=\d+')
    pattern_datastring_settings_dyslexic = re.compile(r'^DYS=[01]')

    @classproperty
    def datastring(cls):
        return textwrap.dedent(f"""\
            DEF={cls.timed.datastring}
            DEF={cls.survival.datastring}
            DEF={cls.infinite.datastring}
            VOL={cls.vol}
            DYS={int(cls.dys)}""")

    @classmethod
    def parse_datastring(cls, datastring: str):
        """
        :param datastring: the datastring to parse
        :return: True if successfully parsed, else False
        """

        if GameRoundSettings.pattern_datastring_settings_timed.match(datastring):
            return cls.timed.parse_datastring(datastring)
        elif GameRoundSettings.pattern_datastring_settings_survial.match(datastring):
            return cls.timed.parse_datastring(datastring)
        elif GameRoundSettings.pattern_datastring_settings_infinite.match(datastring):
            return cls.infinite.parse_datastring(datastring)
        elif cls.pattern_datastring_settings_volume.match(datastring):
            return cls.volume_from_datastring(datastring)
        elif cls.pattern_datastring_settings_dyslexic.match(datastring):
            return cls.dyslexic_from_datastring(datastring)

        return False

    @classmethod
    def volume_from_datastring(cls, datastring: str):
        if datastring[:4] == 'VOL=':
            data = datastring.split('=')
            try:
                cls.vol = int(data[1])
            except (ValueError, IndexError):
                return False
            else:
                return True
        else:
            return False

    @classmethod
    def dyslexic_from_datastring(cls, datastring: str):
        if datastring[:4] == 'DYS=':
            data = datastring.split('=')
            try:
                cls.dys = bool(int(data[1]))
            except (ValueError, IndexError):
                return False
            else:
                return True
        else:
            return False
