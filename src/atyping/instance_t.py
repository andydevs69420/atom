
from . import type_names
from . import nonprimitive_t
from . import operation


class instance_t(nonprimitive_t):
    """ Type compiletime flag.
    """

    def __init__(self, _typeID, _instancename):
        super().__init__()
        self.typeid = _typeID
        self.name   = _instancename
    
    def repr(self):
        return self.name
    
    def matches(self, _rhs):
        if  not _rhs.isinstance():
            return False
        
        return (self.typeid == _rhs.typeid)
    
    def isinstance(self):
        return True
    
    def equality(self, _rhs):
        if  _rhs.istype():
            return operation.op_boolean_t()

        return operation.op_error_t()



