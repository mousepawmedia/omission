"""
Sound Playback Functions [Omission]
"""

import os.path

from kivy.core.audio import SoundLoader

class SoundPlayer(object):
    """
    Play game sounds.
    """
    def __init__(self):
        self.vol = 1
        self.alarm = SoundLoader.load(os.path.join('resources', 'audio', 'alarm.ogg'))
        self.bell = SoundLoader.load(os.path.join('resources', 'audio', 'bell.ogg'))
        self.lowbell = SoundLoader.load(os.path.join('resources', 'audio', 'lowbell.ogg'))
        self.ding = SoundLoader.load(os.path.join('resources', 'audio', 'ding.ogg'))
        self.gameover = SoundLoader.load(os.path.join('resources', 'audio', 'gameover.ogg'))
        self.bonus = list()

        for i in range(1, 9):
            soundpath = os.path.join('resources', 'audio',
                                     'bonus' + str(i) + '.ogg')
            sound = SoundLoader.load(soundpath)
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
            self.alarm.volume = self.vol
            self.alarm.play()

    def play_bell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        if self.bell:
            self.bell.volume = self.vol
            self.bell.play()

    def play_lowbell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        if self.lowbell:
            self.lowbell.volume = self.vol
            self.lowbell.play()

    def play_ding(self):
        """
        Plays the ding (correct) sound effect.
        """
        if self.ding:
            self.ding.volume = self.vol
            self.ding.play()

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
                self.bonus[soundlev].volume = self.vol
                self.bonus[soundlev].play()

    def play_gameover(self):
        """
        Plays the gameover sound effect.
        """
        self.gameover.volume = self.vol
        if self.gameover:
            self.gameover.play()
