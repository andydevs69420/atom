from . import operation
from . import primitive_t


def op_pow_div(_lhs, _rhs):
    """ For power and divide.

        Cast operation as float.
    """
    if  _lhs.isint() and _rhs.isint():
        return operation.op_float64_t()
    
    elif _lhs.isint() and _rhs.isfloat32():
        return operation.op_float32_t()
    
    elif _lhs.isint() and _rhs.isfloat64():
        return operation.op_float64_t()
    #! ====== float =====
    elif _lhs.isfloat32() and _rhs.isint():
        return operation.op_float32_t()

    elif _lhs.isfloat32() and _rhs.isfloat32():
        return operation.op_float32_t()
    
    elif _lhs.isfloat32() and _rhs.isfloat64():
        return operation.op_float64_t()
    #! ===== double =====
    elif _lhs.isfloat32() or _rhs.isfloat64():
        return operation.op_float64_t()
    #! end
    return operation.op_error_t()

def op_mul_mod_add_sub(_lhs, _rhs):
    """ FOR mul, mod, add, sub.

        You can simply use "or" because operand types can be interchanged,
        and remove redundant condition.
    """
    #! ============== BYTE ==================
    if  _lhs.isbyte() and _rhs.isbyte():
        return operation.op_signedbyte_t()

    elif _lhs.isbyte() and _rhs.isshort():
        return operation.op_signedshort_t()
    
    elif _lhs.isbyte() and _rhs.isint32():
        return operation.op_signedint_t()

    elif _lhs.isbyte() and _rhs.islong():
        return operation.op_signedlong_t()

    elif _lhs.isbyte() and _rhs.isbigint():
        return operation.op_signedbigint_t()
    #! ============== SHORT =================
    elif _lhs.isshort() and _rhs.isbyte():
        return operation.op_signedshort_t()

    elif _lhs.isshort() and _rhs.isshort():
        return operation.op_signedshort_t()
    
    elif _lhs.isshort() and _rhs.isint32():
        return operation.op_signedint_t()

    elif _lhs.isshort() and _rhs.islong():
        return operation.op_signedlong_t()

    elif _lhs.isshort() and _rhs.isbigint():
        return operation.op_signedbigint_t()
    #! =============== INT ==================
    elif _lhs.isint32() and _rhs.isbyte():
        return operation.op_signedint_t()

    elif _lhs.isint32() and _rhs.isshort():
        return operation.op_signedint_t()
    
    elif _lhs.isint32() and _rhs.isint32():
        return operation.op_signedint_t()

    elif _lhs.isint32() and _rhs.islong():
        return operation.op_signedlong_t()

    elif _lhs.isint32() and _rhs.isbigint():
        return operation.op_signedbigint_t()
    #! ============== LONG ==================
    elif _lhs.islong() or _rhs.islong():
        return operation.op_signedlong_t()
    #! ============= BIGINT =================
    elif _lhs.isbigint() or _rhs.isbigint():
        return operation.op_signedbigint_t()
    #! ========== ATLEAST 1 FLOAT ===========
    elif _lhs.isfloat() or _rhs.isfloat():
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
    


