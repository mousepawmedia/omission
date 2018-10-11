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

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar

from omission.game.contentloader import ContentLoader
from omission.game.gameround import GameRound, GameMode, GameStatus, GameRoundSettings
from omission.interface.factory import Factory
from omission.data.data_loader import StasisCube

class Gameplay(QWidget):
    """
    The gameplay interface.
    """

    def __init__(self):
        super().__init__()

        self.loader = ContentLoader()
        self.settings = GameRoundSettings()
        self.playing = False
        self.gameround = None

        # Get global soundplayer
        self.soundplayer = StasisCube.dataloader.soundplayer

        # Track guesses
        self._guesses = []
        # Indicates whether we're paused for a solution.
        self.solution_pause = False

        # Create the primary layout
        self.layout = QVBoxLayout()

        # Top section: status and score
        toprow = QHBoxLayout()

        topleft = QVBoxLayout()
        self.lblLabelTries = Factory.label("Tries Left", 12)
        topleft.addWidget(self.lblLabelTries)

        self.lblTries = Factory.label("3", 18)
        topleft.addWidget(self.lblTries)
        toprow.addWidget(Factory.layout_to_widget(topleft))

        topcenter = QVBoxLayout()
        self.lblLabelScore = Factory.label("Score", 12)
        topcenter.addWidget(self.lblLabelScore)

        self.lblScore = Factory.label("00000000", 24)
        topcenter.addWidget(self.lblScore)
        toprow.addWidget(Factory.layout_to_widget(topcenter))

        topright = QVBoxLayout()
        self.lblLabelHint = Factory.label("Letters Removed", 12)
        topright.addWidget(self.lblLabelHint)

        self.lblHint = Factory.label("?", 18)
        topright.addWidget(self.lblHint)

        toprow.addWidget(Factory.layout_to_widget(topright))

        # Convert top row to widget and add to window
        self.layout.addWidget(Factory.layout_to_widget(toprow))

        # Second section: main game
        centerrow = QHBoxLayout()

        self.lblPassage = Factory.label("Lorem ipsum dolar set amet nonummy.", 16, True)
        self.lblPassage.setSizePolicy(Factory.size_policy(2, 1))
        self.lblPassage.setObjectName("passage") # use the correct stylesheet rule
        centerrow.addWidget(self.lblPassage)

        self.lblGuesses = Factory.label("L\nO\nR\nE\nM", 18)
        self.lblGuesses.setMinimumWidth(70)
        centerrow.addWidget(self.lblGuesses)

        self.layout.addWidget(Factory.layout_to_widget(centerrow))

        # Third section: timer/lives
        bottomrow = QHBoxLayout()

        self.lblMode = Factory.icon('clock.png', 30, 30)
        bottomrow.addWidget(self.lblMode)

        self.barTimer = QProgressBar()
        self.barTimer.setTextVisible(False)
        self.barTimer.setValue(50)
        bottomrow.addWidget(self.barTimer)

        self.lblTimer = Factory.label('5:00', 18)
        bottomrow.addWidget(self.lblTimer)

        self.layout.addWidget(Factory.layout_to_widget(bottomrow))

        self.setLayout(self.layout)

