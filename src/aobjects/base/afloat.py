

from . import aobject

class afloat(aobject):

    def __init__(self, _rawflt):
        super().__init__()
        self.raw = _rawflt
    
    def all(self):
        return self.keys() + self.values()
    
    def objecthash(self):
        return self.hash("%f" % self.raw)
    
    def __str__(self):
        return "%f" % self.raw

    def __repr__(self):
        return self.__str__()