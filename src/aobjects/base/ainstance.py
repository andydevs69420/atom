

from . import aobject

class ainstance(aobject):

    def __init__(self, _instance):
        super().__init__()
        self.instance = _instance
    
    def __str__(self):
        _fmt = ""
        _key = self.keys()

        _idx = 0
        for _k, _v in zip(_key, self.values()):

            if  (_k is self) or (_v is self):
                _fmt += "{self}"
            else:
                _fmt += _k.__str__() + ": " + _v.__repr__()
            
            if  _idx < (len(_key) - 1):
                _fmt += ", "
            
            _idx += 1

        return "%s(%s)" % (self.instance, _fmt)
    
    def __repr__(self):
        return self.__str__()

