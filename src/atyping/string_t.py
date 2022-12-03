from . import type_names
from . import nonprimitive_t
from . import operation

class string_t(nonprimitive_t):
    """ String compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.STR
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isstring()
    
    def isstring(self):
        return True

    #! ==== string specific op ====

    def add(self, _rhs):
        if  _rhs.isstring():
            return operation.STR_OP
        
        #! end
        return operation.BAD_OP