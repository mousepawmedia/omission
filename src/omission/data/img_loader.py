"""
Image Loader [Omission]
"""

import os.path
import pkg_resources

def load_image(filename):
    """
    Return the path to the image with the given filename.
    """
    imgpath = pkg_resources.resource_filename(
        __name__,
        os.path.join(os.pardir, "resources", "icons", filename))
    return imgpath
