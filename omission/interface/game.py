"""
Game Interface [Omission]
Version: 2.0

The gameplay interface.

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

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from omission.data import img_loader
from omission.game.contentloader import ContentLoader
from omission.game.gameround import GameRound, GameMode, GameStatus, GameRoundSettings
from omission.interface.useful import to_widget

class Gameplay(QWidget):
    """
    The gameplay interface.
    """

    def __init__(self, root):
        super().__init__()

        self.loader = ContentLoader()
        self.settings = GameRoundSettings()
        self.playing = False
        self.gameround = None

        # Get global soundplayer
        self.soundplayer = root.dataloader.soundplayer

        # Track guesses
        self._guesses = []
        # Indicates whether we're paused for a solution.
        self.solution_pause = False

        # Create the primary layout
        self.layout = QVBoxLayout()

        # Top section: status and score
        toprow = QHBoxLayout()

        topleft = QVBoxLayout()
        self.lblLabelTries = QLabel("Tries Left")
        topleft.addWidget(self.lblLabelTries)
        self.lblTries = QLabel("3")
        topleft.addWidget(self.lblTries)
        toprow.addWidget(to_widget(topleft))

        topcenter = QVBoxLayout()
        self.lblLabelScore = QLabel("Score")
        topcenter.addWidget(self.lblLabelScore)
        self.lblScore = QLabel("00000000")
        topcenter.addWidget(self.lblScore)
        toprow.addWidget(to_widget(topcenter))


        topright = QVBoxLayout()
        self.lblLabelHint = QLabel("Letters Removed")
        topright.addWidget(self.lblLabelHint)
        self.lblHint = QLabel("?")
        topright.addWidget(self.lblHint)
        toprow.addWidget(to_widget(topright))

        # Convert top row to widget and add to window
        self.layout.addWidget(to_widget(toprow))

        # Second section: main game
        centerrow = QHBoxLayout()

        self.lblPassage = QLabel("Example")
        self.lblPassage.setStyleSheet("QLabel {background-color : red; color : blue; }")

        centerrow.addWidget(self.lblPassage)

        self.layout.addWidget(to_widget(centerrow))

        self.setLayout(self.layout)

