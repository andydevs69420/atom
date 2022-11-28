
from sys import argv
from os import path as ospath

from stack import stack

BASE_PATH = ospath.abspath(ospath.dirname(argv[0]))


class state(object):
    """ Shared state for atom.
    """

    def __init__(self):
        self.paths = [
            BASE_PATH, 
            ospath.join(BASE_PATH    , "lib"), 
            ospath.join(ospath.curdir, "lib"),
            ospath.join(ospath.curdir, "bin")
        ]
        self.names = []
        self.files = stack(str)
