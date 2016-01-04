#!/usr/local/bin/python3
"""Animation generator from video / screenshots / screen capture

    @stepaj27

    Usage:
      main.py [ -v -o PATH -s STEP] images <path>
      main.py [ -v -o PATH] video <file>
      main.py [ -v -o PATH] gif <file>
      main.py (-h | --help)

    Arguments:
      <operation>  Math Operation

    Options:
        -o PATH         Output path [default: ./generated]
        -s STEP         Interval between frames in milliseconds when
                        you try to convert video. [default: 100]
        --verbose, -v   More log output. Check this with bigger animations
        -h, --help      Show this screen.

    """

__author__ = 'stepaj27'

from docopt import docopt
import sys
import app



def main():
    """
      Main bootstrap function
    """

    # check if we are running python 3
    if sys.version_info.major != 3:
        print(u"You are not running Python 3.x.x. (/usr/local/bin/python)")
        return

    arguments = docopt(__doc__, version='Animation generator')

    # initialize controller
    app.Controller(arguments).run()


if __name__ == "__main__":
    sys.exit(main())
