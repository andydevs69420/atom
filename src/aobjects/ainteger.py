

from . import aobject

class ainteger(aobject):

    def __init__(self, _rawint):
        super().__init__()
        self.raw = _rawint
    
    def __str__(self):
        return "%d" % self.raw

    def __get__(self):
        return self.raw

