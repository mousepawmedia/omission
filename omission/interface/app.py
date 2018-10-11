"""
User Interface [Omission]
Version: 2.0

The main user interface class.

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

import os, sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QIcon

from omission.data.data_loader import StasisCube
from omission.interface.game import Gameplay


class OmissionApp:
    """
    Application-level class for Omission.
    Stores critical static objects.
    """

    def __init__(self):
        """
        Initializes a new instance of the Omission application.
        """
        self.app = QApplication(sys.argv)

        # Initialize the data storage
        StasisCube(self)

        with open(os.path.join('interface', 'stylesheet.qss'), 'r') as stylesheet_file:
            stylesheet = stylesheet_file.read()
            self.app.setStyleSheet(stylesheet)

        # Initialize the main interface window
        self.window = OmissionWindow()
        self.window.show()
        self.app.exec_()


class OmissionWindow(QMainWindow):
    """
    Application-level class, builds the main window.
    """

    def __init__(self):
        """
        Initialize a new OmissionWindow.
        """
        super().__init__()
        self.title = "Omission"
        self.icon = os.path.join(os.path.dirname(__file__), os.pardir, "resources", "icons", "omission_icon.png")

        # Initialize the window
        self.initUI()

    def initUI(self):
        # Define window title and icon
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))

        # Set minimum window size.
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.show()

        # TODO: TEMP ONLY
        self.start_game()

    def closeEvent(self, event):
        """
        Cleanup tasks when closing application.
        """
        # TODO: Define kill_callback?
        # Save game data
        StasisCube.dataloader.write_out()

    def start_game(self):
        """
        Start a new game.
        """
        print('Start game')
        game = Gameplay()
        self.setCentralWidget(game)

    def keyPressEvent(self, event):
        """
        Handles keyboard events for the entire application.
        """
        # TODO: Relay to active widget
        pass


