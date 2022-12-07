from . import operation
from . import type_names
from . import number_t

class integer_t(number_t):
    """ Integer compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.INT
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(integer_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()

    def isint(self):
        return True
    
    #! ==== integer specific op ====

    def bitnot(self):
        return operation.op_integer_t()

    def shift(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.op_integer_t()
        
        #! end
        return operation.op_error_t()
    
    def equality(self, _rhs):
        if  _rhs.isint():
            return operation.op_boolean_t()

        return operation.op_error_t()
    
    def bitwise(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.op_integer_t()
        
        #! end
        return operation.op_error_t()
