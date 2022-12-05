from . import type_names
from . import number_t

class float_t(number_t):
    """ Float compiletime tag.
    """

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
