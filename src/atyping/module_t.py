from . import type_names
from . import nonprimitive_t
from . import operation

class module_t(nonprimitive_t):
    """ Module compiletime flag.
    """

    def __init__(self, _modname, _members):
        super().__init__()
        self.name = type_names.MODULE
        self.modname = _modname    
        #! type members
        self.members = _members
    
    def qualname(self):
        return self.name
        
    def repr(self):
        _member = ""
        _members = self.members
        _len = len(_members)
        for _p in range(len(self.members)):
            _member += _members[_p][0]

            if  _p < (_len - 1):
                _member += ", "
        #! end
        return self.name + "[" + self.modname + "]"
    
    def matches(self, _rhs):
        #! module cant be passed as args or return
        return False
    
    def ismodule(self):
        return True
    
    def hasAttribute(self, _attrib):
        for _attr in self.members:
            if  _attr[0] == _attrib:
                return True
        
        return False

    def getAttribute(self, _attrib):
        """ Returns attribute type.
        """
        assert self.hasAttribute(_attrib), "uncaught attribute error %s." % _attrib
        
        for _attr in self.members:
            if  _attr[0] == _attrib:
                return _attr[1]
    
    #! ==== type specific op ====

    def equality(self, _rhs):
        if  _rhs.istype():
            return operation.op_boolean_t()

        return operation.op_error_t()
