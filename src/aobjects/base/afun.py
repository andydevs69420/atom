

from . import aobject

class afun(aobject):

    def __init__(self, _funname):
        super().__init__()
        self.funpntr = _funname
    
    def objecthash(self):
        return self.hash(self.funpntr)

    def __str__(self):
        return "[FUNCTION %s]" % self.funpntr
    
    def __repr__(self):
        return self.__str__()

    def __get__(self):
        return self.funpntr


