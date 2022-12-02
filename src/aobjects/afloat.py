

from . import aobject

class afloat(aobject):

    def __init__(self, _rawflt):
        super().__init__()
        self.raw = _rawflt
    
    def __str__(self):
        return "%f" % self.raw

    def __get__(self):
        return self.raw

