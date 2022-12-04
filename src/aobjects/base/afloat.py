

from . import aobject

class afloat(aobject):

    def __init__(self, _rawflt):
        super().__init__()
        self.raw = _rawflt
    
    def __str__(self):
        return "%f" % self.raw

    def __repr__(self):
        return self.__str__()