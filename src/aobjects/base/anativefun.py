

from . import aobject

class anativefun(aobject):

    def __init__(self, _modname, _funname):
        super().__init__()
        self.modpntr = _modname
        self.funpntr = _funname
    
    def all(self):
        return self.keys() + self.values()
    
    def objecthash(self):
        return (self.hash(self.modpntr) + self.hash(self.funpntr))
    
    def __str__(self):
        return "<native function %s.%s(...) at atom memory index %s/>" % (self.modpntr, self.funpntr, hex(self.offset.offset))
    
    def __repr__(self):
        return self.__str__()



