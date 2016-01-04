# -*- coding: utf-8 -*-
"""
Implementation of ImageParser class
"""
from app.parsers.Interface import ParserInterface
import glob
import os
import scipy.misc as misc


class ImageParser(object):
    """A class to process array of images."""
    __implements__ = ParserInterface
    def  __init__(self):
        self.images = []

    def parse(self, path):
        """
        :param path: path to images. It looks for every file in that path.
        :return:
        """
        files = glob.glob(os.path.join(path, '*'))
        if len(files) == 0:
            raise FileNotFoundError('No images in this path: {0}'.format(path))

        self.images = [misc.imread(f) for f in files]
        return self

    def get(self):
        """
        :return: frames of animation as numpy images
        """
        return self.images
