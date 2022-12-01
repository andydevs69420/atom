
from sys import argv
from os import path as ospath
from stack import stack
from mem import mem
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
        self.names = stack(str)
        self.files = stack(str)
        self.codes = ({})
        self.stack = stack( frame )
        self.value = stack(aobject) # instead of storing the address of an object, store the actual object
        self.oprnd = stack(aobject)
        
        #! MEM
        self.memory = mem()
        #! GC
        self.gcroot = None

############################
#    STACK    #   VALUE    #
#-------------#------------#
#      x      #     40     #
#      y      #  "hello!"  #
#      z      #    true    #
#-------------#------------#
#      a      #   [1..2]   #
#      b      #     2.2    #
#      c      #    NULL    #
############################