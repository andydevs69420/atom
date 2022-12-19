

from . import aobject

class amodule(aobject):

    def __init__(self, _modname):
        super().__init__()
        self.module = _modname
    
    def __str__(self):
        return "<module %s at atom memory index %s/>" % (self.module, hex(self.offset.offset))
    
    def __repr__(self):
        return self.__str__()

