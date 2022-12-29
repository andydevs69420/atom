import sys
from sys import argv, executable
from os import path as ospath
from stack import stack
from aframe import frame
from mem import mem
from aobjects import aobject

BASE_PATH = ...

if getattr(sys, "frozen", False):
    BASE_PATH = ospath.abspath(ospath.dirname(executable))
else:
    BASE_PATH = ospath.abspath(ospath.dirname(argv[0]))


LIBS_PATH = ospath.abspath(ospath.join(BASE_PATH[: len(ospath.dirname(BASE_PATH))], "lib"))

CODE   = "code"
MEMORY = "memory"

class astate(object):
    """ Shared state for atom.
    """

    def __init__(self):
        self.paths = [
            BASE_PATH,
            LIBS_PATH,
            ospath.join(ospath.curdir, "lib"),
            ospath.join(ospath.curdir, "bin"),
        ]
        self.aargv = ([])
        self.names = ([])
        self.files = ([])
        self.codes = ({})
        self.calls = ({})
        self.stacktrace = ([])

        #! VM
        self.stack = stack( frame   )
        self.oprnd = stack( aobject )
        
        #! MEM
        self.memory = mem()
