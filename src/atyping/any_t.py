from . import type_names
from . import tag_t

class any_t(tag_t):
    """ Any type, usually those type whose undetermined at compile-time.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.ANY
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(any_t, _cls).__new__(_cls)
        
        #! end
        return _cls.instance
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        return True
    
    def isany(self):
        return True

