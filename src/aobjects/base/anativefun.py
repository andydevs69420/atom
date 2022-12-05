

from . import aobject

class anativefun(aobject):

    def __init__(self, _modname, _funname):
        super().__init__()
        self.modpntr = _modname
        self.funpntr = _funname
    
    def hash(self, _key):
        return self.hash(self.modpntr) + self.hash(self.funpntr)
    
    def __str__(self):
        return "[NATIVE FUNCTION %s.__%s]" % (self.modpntr, self.funpntr)
    
    def __repr__(self):
        return self.__str__()

    def __get__(self):
        return self.funpntr


