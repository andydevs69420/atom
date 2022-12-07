from . import type_names
from . import primitive_t
from .import operation

class boolean_t(primitive_t):
    """ Boolean compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.BOOL
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(boolean_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isboolean()
    
    def isboolean(self):
        return True
    
    #! ===== boolean specific op =====

    def lognot(self):
        return operation.op_boolean_t()
    
    def equality(self, _rhs):
        if  _rhs.isboolean():
            return operation.op_boolean_t()

        return operation.op_error_t()