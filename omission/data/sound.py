"""
Sound Playback Functions [Omission]
"""

import os.path

from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent


class SoundPlayer(object):
    """
    Play game sounds.
    """
    def __init__(self):
        self.player = QMediaPlayer()

        soundfolder = os.path.abspath(os.path.join(os.pardir, "omission", "resources", "audio"))
        print(soundfolder)

        self.vol = 1

        self.alarm = QMediaContent(QUrl.fromLocalFile(os.path.join(soundfolder, 'alarm.ogg')))

        self.bell = QMediaContent(QUrl.fromLocalFile(os.path.join(soundfolder, 'bell.ogg')))

        self.lowbell = QMediaContent(QUrl.fromLocalFile(os.path.join(soundfolder, 'lowbell.ogg')))

        self.ding = QMediaContent(QUrl.fromLocalFile(os.path.join(soundfolder, 'ding.ogg')))

        self.gameover = QMediaContent(QUrl.fromLocalFile(os.path.join(soundfolder, 'gameover.ogg')))

        self.bonus = list()

        for i in range(1, 9):
            soundpath = os.path.join(soundfolder, 'bonus' + str(i) + '.ogg')
            sound = QMediaContent(QUrl.fromLocalFile(soundpath))
            self.bonus.append(sound)

    def get_datastring(self):
        """
        Get the datastring for the sound.
        """
        # VOL=10
        return "VOL=" + str(int(self.vol*10)) + "\n"

    def get_volume(self):
        """
        Get the volume (0-10)
        """
        return int(self.vol * 10)

    def set_volume(self, vol):
        """
        Set the volume (0-10)
        """
        # Enforce valid volume range.
        if vol < 0:
            vol = 0
        elif vol > 10:
            vol = 10

        self.vol = vol/10

    def play_alarm(self):
        """
        Plays the alarm sound effect.
        """
        if self.alarm:
            self.player.setMedia(self.alarm)
            self.player.setVolume(self.vol)
            self.player.play()

    def play_bell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        if self.bell:
            self.player.setMedia(self.bell)
            self.player.setVolume(self.vol)
            self.player.play()

    def play_lowbell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        if self.lowbell:
            self.player.setMedia(self.lowbell)
            self.player.setVolume(self.vol)
            self.player.play()

    def play_ding(self):
        """
        Plays the ding (correct) sound effect.
        """
        if self.ding:
            self.player.setMedia(self.ding)
            self.player.setVolume(self.vol)
            self.player.play()

    def play_bonus(self, level):
        """
        Plays the bonus sound effect.
        """
        if level > 0:
            if level <= 8:
                soundlev = level - 1
            else:
                soundlev = 7

            if self.bonus[soundlev]:
                self.player.setMedia(self.bonus[soundlev])
                self.player.setVolume(self.vol)
                self.player.play()

    def play_gameover(self):
        """
        Plays the gameover sound effect.
        """
        if self.gameover:
            self.player.setMedia(self.gameover)
            self.player.setVolume(self.vol)
            self.player.play()
