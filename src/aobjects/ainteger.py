

from . import aobject

class ainteger(aobject):

    def __init__(self, _rawint):
        super().__init__()
        self.__int = _rawint
    
    def __get__(self):
        return self.__int

