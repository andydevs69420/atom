from . import operation
from . import type_names
from . import number_t

class integer_t(number_t):
    """ Integer compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.INT
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint() or _rhs.isboolean()

    def isint(self):
        return True
    
    #! ==== integer specific op ====

    def bitnot(self):
        return operation.INT_OP

    def shift(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.INT_OP
        
        #! end
        return operation.BAD_OP
    
    def bitwise(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.INT_OP
        
        #! end
        return operation.BAD_OP
