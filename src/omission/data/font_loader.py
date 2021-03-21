"""
Font Loader [Omission]
"""

import os.path
import pkg_resources

class FontLoader(object):
    """
    Loads the correct font based on settings.
    """

    def __init__(self):
        self.dyslexic_mode = False

        fontfolder = os.path.join(os.pardir, "resources", "font")

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
