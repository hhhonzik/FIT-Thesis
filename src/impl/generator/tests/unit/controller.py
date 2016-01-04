import unittest

import app

class ControllerTestCase(unittest.TestCase):

    def test_verbose_arg(self):
        controller = app.Controller({
            '--verbose': True,
            'images': True,
            'video': False,
            'gif': False,
            '-o': './generated',
            '<path>': './tests/resources/images'
        })
        self.assertEqual(controller.talk, True)

    def test_parser(self):
        controller = app.Controller({
            '--verbose': False,
            'images': True,
            'video': False,
            'gif': False,
            '-o': './generated',
            '<path>': './tests/resources/images'
        })
        self.assertEqual(controller.input, './tests/resources/images')
        self.assertEqual(controller.parser.__class__.__name__, 'ImageParser')
