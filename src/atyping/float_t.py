from . import type_names
from . import number_t

class float_t(number_t):
    """ Float compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.FLOAT
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isfloat()
    
    def isfloat(self):
        return True
