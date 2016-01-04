# -*- coding: utf-8 -*-
"""
Console log messages (with colors)
"""
__author__ = 'stepaj27'

BOLD = '\033[01m'

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
LIGHT_PURPLE = '\033[94m'
PURPLE = '\033[95m'

END = '\033[0m'
import sys

def warn(msg, additional=""):
    """
    :param msg: error message
    :param additional: additional note (not colored)
    :return:
    """
    print(YELLOW + BOLD + msg + END + " " + additional)

def success(msg, additional=""):
    """
    :param msg: error message
    :param additional: additional note (not colored)
    :return:
    """
    print(GREEN + BOLD + msg + END + " " + additional)

def error(msg, additional=""):
    """
    :param msg: error message
    :param additional: additional note (not colored)
    :return:
    """
    print(RED + BOLD + msg + END + " " + additional)
    sys.exit()
