

from . import aobject

class astring(aobject):

    def __init__(self, _rawstr):
        super().__init__()
        self.raw = _rawstr
    
    def __str__(self):
        return "%s" % self.raw
    
    def __repr__(self):
        return "\"%s\"" % self.__str__()


