"""
Interface Factory Functions [Omission]
Version: 2.0

Functions to create common interface objects.

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
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy

from omission.data.data_loader import StasisCube
from omission.data.img_loader import load_image


class Factory:
    """
    A static class containing QWidget factory functions.
    """

    @staticmethod
    def size_policy(vertical_stretch: int = 0, horizontal_stretch: int = 0):
        policy = QSizePolicy()

        if vertical_stretch < 0:
            policy.setVerticalPolicy(QSizePolicy.Minimum)
        elif vertical_stretch > 0:
            policy.setVerticalStretch(vertical_stretch)
            policy.setVerticalPolicy(QSizePolicy.MinimumExpanding)

        if horizontal_stretch < 0:
            policy.setHorizontalPolicy(QSizePolicy.Minimum)
        elif horizontal_stretch > 0:
            policy.setHorizontalStretch(horizontal_stretch)
            policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)

        return policy


    @staticmethod
    def layout_to_widget(layout: QWidget):
        """
        Generates a widget from the provided QLayout object.
        :param layout: the QLayout to convert to a widget
        :return: the QWidget generated from the QLayout
        """
        widget = QWidget()
        widget.setLayout(layout)
        return widget


    @staticmethod
    def label(text: str, size: int, passage: bool = False):
        """
        Generate a QLabel with the given text and size.
        :param text: the label text
        :param size: the point height of the font
        :return: the generated QLabel object
        """
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        if passage:
            lbl.setFont(StasisCube.dataloader.fontloader.passage(size))
        else:
            lbl.setFont(StasisCube.dataloader.fontloader.decorative(size))

        return lbl


    @staticmethod
    def icon(filename: str, width: int, height: int):
        """
        Generate a QLabel with the given icon and size.
        :param filename: the filename for the icon (from resources/icons)
        :param width: the width of the icon
        :param height: the height of the icon
        :return: the generated QLabel object
        """
        lbl = QLabel()
        pixmap = QPixmap(load_image(filename))
        pixmap = pixmap.scaled(width, height)
        lbl.setPixmap(pixmap)
        return lbl
