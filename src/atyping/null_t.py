from . import type_names
from . import primitive_t


class null_t(primitive_t):
    """ Null compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.NULL
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isnull()
    
    def isnull(self):
        return True