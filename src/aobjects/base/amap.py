
from . import aobject



class amap(aobject):

    def __init__(self):
        super().__init__()
    
    def all(self):
        return self.keys() + self.values()
    
    def merge(self, _amap):
        for _k, _v in zip(_amap.keys(), _amap.values()):
            self.put(_k, _v)
    
    def __str__(self):
        _fmt = ""
        _key = self.keys()

        _idx = 0
        for _k, _v in zip(_key, self.values()):

            if  (_k is self) or (_v is self):
                _fmt += "{self}"
            else:
                _fmt += _k.__repr__() + ": " + _v.__repr__()
            
            if  _idx < (len(_key) - 1):
                _fmt += ", "
            
            _idx += 1

        return "{" + _fmt + "}"
    
    def __repr__(self):
        return self.__str__()