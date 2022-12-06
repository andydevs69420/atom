
from . import aobject

class aarray(aobject):

    def __init__(self, *_array_of_aobject:list[aobject]):
        super().__init__()
        self.array = list(_array_of_aobject)
    
    def push(self, _aobject):
        self.array.append(_aobject)

    def pushall(self, _array):
        self.array.extend(_array.array)
    
    def subscript(self, _int_index):
        return self.array[_int_index.raw]

    def set_index(self, _int_index, _aobject_value):
        self.array[_int_index.raw] = _aobject_value
    
    def objecthash(self):
        return sum([*[_obj.objecthash() for _obj in self.array]])
    
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
