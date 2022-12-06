from . import type_names
from . import nonprimitive_t
from . import operation

class error_t(nonprimitive_t):
    """ Error compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.ERROR
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.iserror()
    
    def iserror(self):
        return True