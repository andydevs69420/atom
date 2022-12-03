from . import type_names
from . import nonprimitive_t
from . import operation

class array_t(nonprimitive_t):
    """ Array compiletime tag.
    """

    def __init__(self, _elementtype):
        super().__init__()
        self.name = type_names.ARRAY
        self.elementtype = _elementtype
    
    def repr(self):
        return self.name + "[" + self.elementtype.repr() + "]"
    
    def matches(self, _rhs):
        if  not _rhs.isarray():
            return False

        return self.elementtype.matches(_rhs.elementtype)
    
    def isarray(self):
        return True

    #! ==== array specific op ====

    def unpack(self):
        return operation.ARRAY_UNPACK