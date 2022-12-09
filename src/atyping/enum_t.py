


from . import type_names
from . import nonprimitive_t
from . import operation

class enum_t(nonprimitive_t):
    """ Enum compiletime tag.
    """

    def __init__(self, _membertype, _members):
        super().__init__()
        self.name = type_names.ENUM
        self.membertype = _membertype
        self.members    = _members

    def qualname(self):
        return self.name

    def repr(self):
        return self.name + "[" + self.membertype.repr() + "]"
    
    def matches(self, _rhs):
        if  not _rhs.isenum():
            return False

        return self.membertype.matches(_rhs.membertype)
    
    def isenum(self):
        return True
    
    def hasAttribute(self, _member):
        for _attr in self.members:
            if  _attr[0] == _member:
                return True
        
        return False

    def getAttribute(self, _member):
        """ Returns member type.
        """
        assert self.hasAttribute(_member), "uncaught member error %s." % _member
        
        for _attr in self.members:
            if  _attr[0] == _member:
                return _attr[1]
    
    #! ====== enum specifc op ======

    def equality(self, _rhs):
        if  _rhs.isenum():
            return operation.op_boolean_t()

        return operation.op_error_t()
    

