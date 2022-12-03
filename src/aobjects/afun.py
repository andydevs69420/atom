

from . import aobject

class afun(aobject):

    def __init__(self, _funname):
        super().__init__()
        self.funpntr = _funname
    
    def __str__(self):
        return "<function %s(...)/>" % self.funpntr

    def __get__(self):
        return self.funpntr


