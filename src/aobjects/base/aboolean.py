

from . import aobject

class aboolean(aobject):

    def __init__(self, _rawbool):
        super().__init__()
        self.raw = _rawbool
    
    def all(self):
        return self.keys() + self.values()
    
    def objecthash(self):
        return self.hash(int(self.raw))
    
    def __str__(self):
        return "%s" % "true" if self.raw else "false"
    
    def __repr__(self):
        return self.__str__()

