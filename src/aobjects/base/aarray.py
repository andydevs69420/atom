
from . import aobject

class aarray(aobject):

    def __init__(self, *_array_of_aobject:list[aobject]):
        super().__init__()
        self.array = list(_array_of_aobject)
    
    def push(self, _aobject):
        self.array.append(_aobject)

    def pushall(self, _array):
        self.array.extend(_array.array)
    
    def __str__(self):
        _fmt = ""
        for _r in range(len(self.array)):
            if  self.array[_r] is self:
                _fmt += "[array]"
            else:
                _fmt += self.array[_r].__repr__()
            
            if  _r < (len(self.array) - 1):
                _fmt += ", "

        #! array
        return "[%s]" % _fmt
    
    def __repr__(self):
        return self.__str__()
