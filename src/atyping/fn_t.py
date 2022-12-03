from . import type_names
from . import nonprimitive_t


class fn_t(nonprimitive_t):
    """ Array compiletime tag.
    """

    def __init__(self, _returntype):
        super().__init__()
        self.name = type_names.FN
        self.returntype = _returntype
    
    def repr(self):
        return self.name + "[" + self.returntype.repr() + "]"
    
    def matches(self, _rhs):
        if  not _rhs.isfunction():
            return False

        return self.returntype.matches(_rhs.returntype)
    
    def isfunction(self):
        return True
