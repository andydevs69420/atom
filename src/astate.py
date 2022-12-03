
from sys import argv
from os import path as ospath
from stack import stack
from sizedstack import sizedstack
from mem import mem
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
        self.files = ([])
        self.codes = ({})

        #! VM
        self.stack = sizedstack(1000)
        self.oprnd = stack( aobject )
        
        #! MEM
        self.memory = mem()
        #! GC
        self.gcroot = None

############################             ###############
#    STACK    #   VALUE    #             #     HEAP    # 
#-------------#------------#             #-------------#
#      x      #     40     # <---------> #  intobj-40  #
#      y      #  "hello!"  #             #      |      #
#      z      #    true    #             #      |      #
#-------------#------------#             #      v      #
#      a      #   [1..2]   #             ###############    
#      b      #     2.2    #
#      c      #    NULL    #
############################