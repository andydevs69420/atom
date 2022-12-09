from . import operation
from . import type_names
from . import number_t
from platform import architecture


SIGNED__8bit_MIN = -(2 ** (8-1))
SIGNED__8bit_MAX =  (2 ** (8-1) - 1)

SIGNED_16bit_MIN = -(2 ** (16-1))
SIGNED_16bit_MAX =  (2 ** (16-1) - 1)


SIGNED_32bit_MIN = -(2 ** (32-1))
SIGNED_32bit_MAX =  (2 ** (32-1) - 1)

SIGNED_64bit_MIN = -(2 ** (64-1))
SIGNED_64bit_MAX =  (2 ** (64-1) - 1)

SIGNED_128bit_MIN = -(2 ** (128-1))
SIGNED_128bit_MAX =  (2 ** (128-1) - 1)


from platform import architecture

class integer_t(number_t):
    """ Integer compiletime tag.
    """

    @staticmethod
    def auto(_int:int):
        _size = operation.op_error_t()

        if  _int >= SIGNED_128bit_MIN and _int <= SIGNED_128bit_MAX:
            _size = signedbigint_t()

        if  _int >= SIGNED_64bit_MIN and _int <= SIGNED_64bit_MAX:
            _size = signedint_t()

        if  _int >= SIGNED_32bit_MIN and _int <= SIGNED_32bit_MAX:
            _size = signedint_t()

        if  _int >= SIGNED_16bit_MIN and _int <= SIGNED_16bit_MAX:
            _size = signedshort_t()

        if  _int >= SIGNED__8bit_MIN and _int <= SIGNED__8bit_MAX:
            _size = signedbyte_t()
        
        #! if it remains "error_t", then interger overflow or underflow.
        return _size

    #! =============================

    def __init__(self):
        super().__init__()
        self.name = type_names.INT
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(integer_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance

    def qualname(self):
        return self.name

    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()

    def isint(self):
        return True
    
    def ismax8(self):return False
    def ismax16(self):return False
    def ismax32(self):return False
    def ismax64(self):return False
    def ismax128(self):return False
    
    #! ==== integer specific op ====

    def bitnot(self):
        return self

    def shift(self, _rhs):
        if  _rhs.isint():
            return self
        
        #! end
        return operation.op_error_t()
    
    def equality(self, _rhs):
        if  _rhs.isint():
            return operation.op_boolean_t()

        return operation.op_error_t()
    
    def bitwise(self, _rhs):
        if  self.isbyte() and _rhs.isbyte():
            return operation.op_signedbyte_t()

        elif self.isbyte() and _rhs.isshort():
            return operation.op_signedshort_t()
        
        elif self.isbyte() and _rhs.isint32():
            return operation.op_signedint_t()

        elif self.isbyte() and _rhs.islong():
            return operation.op_signedlong_t()

        elif self.isbyte() and _rhs.isbigint():
            return operation.op_signedbigint_t()
        #! ============== SHORT =================
        elif self.isshort() and _rhs.isbyte():
            return operation.op_signedshort_t()

        elif self.isshort() and _rhs.isshort():
            return operation.op_signedshort_t()
        
        elif self.isshort() and _rhs.isint32():
            return operation.op_signedint_t()

        elif self.isshort() and _rhs.islong():
            return operation.op_signedlong_t()

        elif self.isshort() and _rhs.isbigint():
            return operation.op_signedbigint_t()
        #! =============== INT ==================
        elif self.isint32() and _rhs.isbyte():
            return operation.op_signedint_t()

        elif self.isint32() and _rhs.isshort():
            return operation.op_signedint_t()
        
        elif self.isint32() and _rhs.isint32():
            return operation.op_signedint_t()

        elif self.isint32() and _rhs.islong():
            return operation.op_signedlong_t()

        elif self.isint32() and _rhs.isbigint():
            return operation.op_signedbigint_t()
        #! ============== LONG ==================
        elif self.islong() or _rhs.islong():
            return operation.op_signedlong_t()
        #! ============= BIGINT =================
        elif self.isbigint() or _rhs.isbigint():
            return operation.op_signedbigint_t()
        
        #! end
        return operation.op_error_t()




class signedbyte_t(integer_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.I8

    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedbyte_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return  self.name
    
    def matches(self, _rhs):
        return _rhs.isbyte()
    
    def isbyte(self):
        return True
    
class signedshort_t(integer_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.I16
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedshort_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return  self.name
    
    def matches(self, _rhs):
        return _rhs.isbyte() or _rhs.isshort()
    
    def isshort(self):
        return True


class signedint_t(integer_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.I32
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedint_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return  self.name
    
    def matches(self, _rhs):
        return _rhs.isbyte() or _rhs.isshort() or _rhs.isint32()

    def isint32(self):
        return True


class signedlong_t(integer_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.I64
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedlong_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isbyte() or _rhs.isshort() or _rhs.isint32() or _rhs.islong()
    
    def islong(self):
        return True


class signedbigint_t(integer_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.I128
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedbigint_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance

    def repr(self):
        return  self.name
    
    def matches(self, _rhs):
        #! or replace with _rhs.isint()
        return _rhs.isbyte() or _rhs.isshort() or _rhs.isint32() or _rhs.islong() or _rhs.isbigint()
    
    def isbigint(self):
        return True

