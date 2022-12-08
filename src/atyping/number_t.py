from . import operation
from . import primitive_t

class number_t(primitive_t):
    """ Base tag or int and float.
    """

    def __init__(self):
        super().__init__()

    def pos(self):
        if  self.isint():
            return operation.op_integer_t()

        elif self.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()
    
    def neg(self):
        if  self.isint():
            return operation.op_integer_t()

        elif self.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()

    #! ============= arithmetic =============

    def pow(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.op_integer_t()

        elif self.isfloat() or _rhs.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()

    def mul(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.op_integer_t()

        elif self.isfloat() or _rhs.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()
    
    def div(self, _rhs):
        if  self.isint() or _rhs.isfloat():
            return operation.op_float_t()

        #! end
        return operation.op_error_t()
    
    def mod(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.op_integer_t()

        elif self.isfloat() or _rhs.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()

    def add(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.op_integer_t()

        elif self.isfloat() or _rhs.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()
    
    def sub(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.op_integer_t()

        elif self.isfloat() or _rhs.isfloat():
            return operation.op_float_t()
        
        #! end
        return operation.op_error_t()
    

    #! ========= relational group ==========
    
    def relational(self, _rhs):
        if  _rhs.isprimitive():
            return operation.op_boolean_t()

        #! end
        return operation.op_error_t()
    


