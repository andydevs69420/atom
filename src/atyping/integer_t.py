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
        return operation.op_integer_t()

    def shift(self, _rhs):
        if  _rhs.isint():
            return operation.op_integer_t()
        
        #! end
        return operation.op_error_t()
    
    def equality(self, _rhs):
        if  _rhs.isint():
            return operation.op_boolean_t()

        return operation.op_error_t()
    
    def bitwise(self, _rhs):
        if  _rhs.isint():
            return operation.op_boolean_t()

        return operation.op_error_t()


class signedbyte_t(integer_t):

    def __init__(self):
        super().__init__()

    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedbyte_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()
    
    def isbyte(self):
        return True
    
class signedshort_t(integer_t):

    def __init__(self):
        super().__init__()
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedshort_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()
    
    def isshort(self):
        return True


class signedint_t(integer_t):

    def __init__(self):
        super().__init__()
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedint_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isbyte() or _rhs.isshort() or _rhs.isint32()

    def isint32(self):
        return True


class signedlong_t(integer_t):

    def __init__(self):
        super().__init__()
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedlong_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()
    
    def islong(self):
        return True


class signedbigint_t(integer_t):

    def __init__(self):
        super().__init__()
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(signedbigint_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance

    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isint()
    
    def isbigint(self):
        return True

