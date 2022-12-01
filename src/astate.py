
from sys import argv
from os import path as ospath
from stack import stack
from aframe import frame
from aobjects import aobject

BASE_PATH = ospath.abspath(ospath.dirname(argv[0]))



CODE   = "code"
MEMORY = "memory"

class astate(object):
    """ Shared state for atom.
    """

    def __init__(self):
        self.paths = [
            BASE_PATH, 
            ospath.join(BASE_PATH    , "lib"), 
            ospath.join(ospath.curdir, "lib"),
            ospath.join(ospath.curdir, "bin"),
        ]
        self.names = ([])
        self.files = stack(str)
        self.codes = ({})
        self.stack = stack(frame  )
        self.value = stack(aobject)
        self.oprnd = stack(aobject)
        
        #! GC
        self.gcroot = None