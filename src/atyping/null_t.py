from . import type_names
from . import primitive_t
from . import operation

class null_t(primitive_t):
    """ Null compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.NULL
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(null_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
        
    def qualname(self):
        return self.name

    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isnull()
    
    def isconstant(self):
        return True
    
    def isnull(self):
        return True
    
    #! ===== null specific op =====

    def lognot(self):
        return operation.op_boolean_t()

    def equality(self, _rhs):
        if  _rhs.isnull():
            return operation.op_boolean_t()

        return operation.op_error_t()