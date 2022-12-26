

from . import aobject

class ainteger(aobject):

    def __init__(self, _rawint):
        super().__init__()
        self.raw = _rawint

    def all(self):
        return self.keys() + self.values()
    
    def objecthash(self):
        return self.hash(self.raw)
    
    def __str__(self):
        return "%s" % self.raw
    
    def __repr__(self):
        return self.__str__()

