# -*- coding: utf-8 -*-
"""

Definition of main controller class which binds together the whole application.

"""
__author__ = 'stepaj27'
import app.parsers as parsers

from app.generator import Generator as generator
from app.export import Export as export

# import scipy.misc as misc

class Controller(object):
    """
    Definition of Controller class
    """
    def __init__(self, args):
        """
        :param args: docopt parsed args.
        :return: self
        """
        if args['images']:
            self.parser = parsers.ImageParser()
            self.input = args['<path>']
        if args['gif']:
            self.parser = parsers.GifParser()
            self.input = args['<file>']
        if args['video']:
            self.parser = parsers.VideoParser(args['-s'])
            self.input = args['<file>']

        self.talk = args['--verbose'] == True

        self.exporter = export(args['-o'])

    def run(self):
        """
        Run the whole generator process
        :return: null
        """
        images = self.parser.parse(self.input).get()
        # [misc.imsave("./out/{0}.png".format(i), images[i]) for i in range(len(images))];
        instance = generator(images)
        instance.talk = self.talk
        instance.generate(self.exporter)
