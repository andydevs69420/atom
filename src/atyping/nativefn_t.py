from . import type_names
from . import nonprimitive_t


class nativefn_t(nonprimitive_t):
    """ Array compiletime tag.
    """

    def __init__(self, _returntype, _paramcount, _parameters):
        super().__init__()
        self.name = type_names.NATIVEFN
        self.returntype = _returntype
        self.paramcount = _paramcount
        self.parameters = _parameters
    
    def repr(self):
        _param = ""
        for _p in range(self.paramcount):
            _param += self.parameters[_p][1].repr()

            if  _p < (self.paramcount - 1):
                _param += ", "
        #! end
        return self.name + "[" + self.returntype.repr() + "]" + "(" + _param + ")"
    
    def matches(self, _rhs):
        if  not _rhs.isnativefunction():
            return False
        
        if  self.paramcount != _rhs.paramcount:
            return False
        
        for _x, _y in zip(self.parameters, _rhs.parameters):
            if  not _x[1].matches(_y[1]):
                return False

        return self.returntype.matches(_rhs.returntype)
    
    def isnativefunction(self):
        return True
