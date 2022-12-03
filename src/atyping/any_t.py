from . import type_names
from . import tag_t

class any_t(tag_t):
    """ Any type, usually those type whose undetermined at compile-time.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.ANY
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return _rhs.isany()
    
    def isany(self):
        return True

