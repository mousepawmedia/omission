"""
Sound Playback Functions [Omission]
"""

from kivy.core.audio import SoundLoader

class SoundPlayer(object):
    """
    Play game sounds.
    """
    def __init__(self):
        self.vol = 1

    def get_datastring(self):
        """
        Get the datastring for the sound.
        """
        return "VOL=" + str(int(self.vol*10))

    def set_volume(self, vol):
        """
        Set the volume (0-10)
        """
        self.vol = vol/10

    def play_alarm(self):
        """
        Plays the alarm sound effect.
        """
        sound = SoundLoader.load('resources/audio/alarm.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()

    def play_bell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        sound = SoundLoader.load('resources/audio/bell.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()

    def play_lowbell(self):
        """
        Plays the low bell (wrong) sound effect.
        """
        sound = SoundLoader.load('resources/audio/lowbell.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()

    def play_ding(self):
        """
        Plays the ding (right) sound effect.
        """
        sound = SoundLoader.load('resources/audio/ding.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()

    def play_bonus(self, level):
        """
        Plays the bonus sound effect.
        """
        if level > 0 and level <= 8:
            soundlev = level
        elif level > 9:
            soundlev = 8
        sound = SoundLoader.load('resources/audio/bonus' + soundlev + '.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()

    def play_gameover(self):
        """
        Plays the gameover sound effect.
        """
        sound = SoundLoader.load('resources/audio/gameover.ogg')
        sound.volume = self.vol
        if sound:
            sound.play()
