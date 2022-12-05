from . import type_names
from . import nonprimitive_t
from . import operation

class map_t(nonprimitive_t):
    """ Map compiletime tag.
    """

    def __init__(self, _keytype, _valtype):
        super().__init__()
        self.name = type_names.MAP
        self.keytype = _keytype
        self.valtype = _valtype
    
    def qualname(self):
        return self.name
        
    def repr(self):
        return self.name + "[" + self.keytype.repr() + ":" + self.valtype.repr() + "]"
    
    def matches(self, _rhs):
        if  not _rhs.ismap():
            return False
        
        return self.keytype.matches(_rhs.keytype) and self.valtype.matches(_rhs.valtype)

    def ismap(self):
        return True
    
    #! ==== map specific op ====
    
    def unpack(self):
        return self