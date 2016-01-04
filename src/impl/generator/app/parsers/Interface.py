"""
Parser interface to use in class modules
"""
__author__ = 'stepaj27'


class ParserInterface(object):
    """
    Implementation of parser interface.
    We need 2 methods to be implemented - get() and parse(files)
    """
    def parse(self, files):
        """
        :return self
        """
        raise NotImplementedError("method parse(filePath) is not implemented")

    def get(self):
        """
        :return Array
        """
        raise NotImplementedError("method get() is not implemented")
