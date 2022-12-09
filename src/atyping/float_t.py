from . import type_names
from . import number_t
from . operation import operation

F32_MIN = -3.4028235e+38
F32_MAX =  3.4028235e+38

F64_MIN = -1.7976931348623157e+308 
F64_MAX =  1.7976931348623157e+308


class float_t(number_t):
    """ Float compiletime tag.
    """

    def auto(_float):
        _size = operation.op_error_t()

        if  _float >= F64_MIN and _float <= F64_MAX:
            _size = float64_t()
        
        if  _float >= F32_MIN and _float <= F32_MAX:
            _size = float32_t()

        return _size

    #! ================
    def __init__(self):
        super().__init__()
        self.name = type_names.FLOAT
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(float_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance

    def qualname(self):
        return self.name

    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isfloat()
    
    def isfloat(self):
        return True

    #! ======= float specific op =======

    def equality(self, _rhs):
        if  _rhs.isfloat():
            return operation.op_boolean_t()

        return operation.op_error_t()


class float32_t(float_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.F32

    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(float32_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return super().repr()
    
    def matches(self, _rhs):
        return _rhs.isfloat32()

    def isfloat32(self):
        return True


class float64_t(float_t):

    def __init__(self):
        super().__init__()
        self.name = type_names.F64

    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(float64_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return super().repr()
    
    def matches(self, _rhs):
        return _rhs.isfloat32() or _rhs.isfloat64()

    def isfloat64(self):
        return True
