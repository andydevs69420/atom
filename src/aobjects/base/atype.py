

from . import aobject

class atype(aobject):

    def __init__(self, _typename):
        super().__init__()
        self.typepntr = _typename
    
    def objecthash(self):
        return self.hash(self.typepntr)

    def __str__(self):
        return "<type %s(...) at atom memory index %s/>" % (self.typepntr, hex(self.offset.offset))
    
    def __repr__(self):
        return self.__str__()


