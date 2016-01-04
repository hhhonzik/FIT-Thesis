# -*- coding: utf-8 -*-
"""
Implementation of Video parser.

Requirements: ffmpeg (to install please see https://www.ffmpeg.org)
              av (to install please use Pip: pip install av)
"""
from app.parsers.Interface import ParserInterface

import av
import scipy.misc as misc
from app.utils.console import warn

class VideoParser():
    """A class to process Video file."""
    __implements__ = ParserInterface
    def __init__(self, delay):
        self.images = []
        self.delay = delay

    def parse(self, file):
        """
        :param file: path to a video file.
        :return: self
        """
        container = av.open(file)
        step = int(self.delay) # every 100 frames of video
        warn("Video delay: ", str(step))
        currentframe = 0
        for packet in container.demux():
            for frame in packet.decode():
                currentframe += 1
                if currentframe >= step:
                    self.images.append(misc.fromimage(frame.to_image()))
                    currentframe = 0
        return self

    def get(self):
        """
        :return: frames of animation as numpy images
        """
        return self.images
