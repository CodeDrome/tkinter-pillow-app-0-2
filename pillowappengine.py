import os.path

import PIL
from PIL import Image
from PIL import ImageEnhance


class PillowAppEngine(object):

    """
    Implements a wrapper over the core Pillow functionality.
    Provides state and methods for UIs and other client
    software to streamline Pillow usage.
    """

    PILLOW_VERSION = PIL.PILLOW_VERSION

    def __init__(self, on_image_change):

        self.image = None
        self.filepath = None
        self.saved = None
        self.on_image_change = on_image_change

    def open(self, filepath):

        """
        Attempts to create a Pillow Image from
        the filepath. If successful this becomes
        the "image" attribute.
        """

        try:
            self.image = Image.open(filepath)
            self.filepath = filepath
            self.saved = True
            self.on_image_change()
        except Exception as e:
            self.image = None
            self.filepath = None
            raise

    def save(self):

        """
        Attempts to save the image with the
        filename it was opened from.
        """

        try:
            self.image.save(self.filepath)
            self.saved = True
        except Exception as e:
            self.saved = False
            raise

    def save_as(self, filepath):

        """
        Attempts to save the image to the
        specified filepath.
        """

        try:
            self.filepath = filepath
            self.image.save(self.filepath)
            self.saved = True
            self.on_image_change()
        except Exception as e:
            self.saved = False
            raise

    def close(self):

        """
        Sets the image other attributes to None.
        """

        self.image = None
        self.filepath = None
        self.saved = None
        self.on_image_change()

    def get_properties(self):

        """
        Returns a dictionary containing various
        pieces of information on the image.
        """

        if self.image is not None:

            return {"filepath": self.filepath,
                    "filename": os.path.split(self.filepath)[1],
                    "width": self.image.width,
                    "height": self.image.height,
                    "format": self.image.format,
                    "mode": self.image.mode}

        else:

            return None

    def get_properties_text(self):

        """
        Returns the image information from
        get_properties in a text format.
        """

        if self.image is not None:

            properties = self.get_properties()

            format_string = "File Name: {}\nWidth:     {}\nHeight:    {}\nFormat:    {}\nMode:      {}"

            properties_text = format_string.format(properties["filename"],
                                                   properties["width"],
                                                   properties["height"],
                                                   properties["format"],
                                                   properties["mode"])

            return properties_text

        else:

            return "No image"
