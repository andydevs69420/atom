from . import type_names
from . import nonprimitive_t
from . import operation

class string_t(nonprimitive_t):
    """ String compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.STR
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(string_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isstring()
    
    def isstring(self):
        return True

    #! ==== string specific op ====

    def add(self, _rhs):
        if  _rhs.isstring():
            return operation.op_string_t()
        
        #! end
        return operation.op_error_t()