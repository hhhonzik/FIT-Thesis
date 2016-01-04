# -*- coding: utf-8 -*-
"""
GIF parser module implementation
"""
from app.parsers.Interface import ParserInterface
from PIL import Image
import tempfile
import scipy.misc as misc



class GifParser(object):
    """
    A class to process JIF Images.
    """
    __implements__ = ParserInterface
    def __init__(self):
        self.images = []

    def parse(self, file):
        """
        :param file: path to a .gif file.
        :return: self
        """
        gifimage = Image.open(file)
        # To iterate through the entire gif
        try:
            while 1:
                temporaryfile = tempfile.NamedTemporaryFile(suffix='_image.png', delete=True)
                gifimage.seek(gifimage.tell()+1)
                gifimage.convert('RGB').save(temporaryfile, 'PNG')
                self.images.append(misc.fromimage(Image.open(temporaryfile)))
                # do something to im
        except EOFError:
            pass # end of sequence
        return self

    def get(self):
        """
        :return: Array of numpy images
        """
        return self.images
