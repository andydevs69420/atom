from . import operation
from . import primitive_t


def op_pow_div(_lhs, _rhs):
    """ For power and divide.

        Cast operation as float.
    """
    if  _lhs.isint() and _rhs.isint():
        return operation.op_float_t()
    
    elif _lhs.isfloat() and _rhs.isfloat():
        return operation.op_float_t()
    
    #! end
    return operation.op_error_t()

def op_mul_mod_add_sub(_lhs, _rhs):
    if  _lhs.isint() and _rhs.isint():
        return operation.op_integer_t()

    elif _lhs.isfloat() and _rhs.isfloat():
        return operation.op_float_t()

    elif _lhs.isfloat() and _rhs.isint():
        return operation.op_float_t()
    
    elif _lhs.isint() and _rhs.isfloat():
        return operation.op_float_t()
    
    #! end
    return operation.op_error_t()

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
        return op_pow_div(self, _rhs)

    def mul(self, _rhs):
        return op_mul_mod_add_sub(self, _rhs)
    
    def div(self, _rhs):
        return op_pow_div(self, _rhs)
    
    def mod(self, _rhs):
        return op_mul_mod_add_sub(self, _rhs)

    def add(self, _rhs):
        return op_mul_mod_add_sub(self, _rhs)
    
    def sub(self, _rhs):
        return op_mul_mod_add_sub(self, _rhs)
    

    #! ========= relational group ==========
    
    def relational(self, _rhs):
        if  _rhs.isprimitive():
            return operation.op_boolean_t()

        #! end
        return operation.op_error_t()
    


