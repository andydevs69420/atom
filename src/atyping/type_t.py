from . import type_names
from . import nonprimitive_t
from . import operation


class type_t(nonprimitive_t):
    """ Type compiletime flag.
    """

    def __init__(self, _typeID, _typename, _returntype, _paramcount, _parameters):
        super().__init__()
        self.name = type_names.TYPE
        self.typenumber = _typeID
        self.typename   = _typename
        self.returntype = _returntype
        self.paramcount = _paramcount
        #! type members becomes parameters
        self.parameters = _parameters
        #! methods
        self.methods = []
    
    def clear(self):
        self.methods = []
    
    def dump(self):
        print(self.methods)
        print(self.parameters)
    
    def qualname(self):
        return self.name
        
    def repr(self):
        _param = ""
        for _p in range(self.paramcount):
            _param += self.parameters[_p][1].repr()

            if  _p < (self.paramcount - 1):
                _param += ", "
        #! end
        return self.name + "[" + self.returntype.repr() + "]" + "(" + _param + ")"
    
    def matches(self, _rhs):
        if  not _rhs.istype():
            return False
        
        if  self.paramcount != _rhs.paramcount:
            return False
        
        if  self.typeid != _rhs.typeid:
            return False
        
        for _x, _y in zip(self.parameters, _rhs.parameters):
            if  not _x[1].matches(_y[1]):
                return False

        return self.returntype.matches(_rhs.returntype)
    
    def istype(self):
        return True
    
    def hasAttribute(self, _attrib):
        for _attr in self.parameters:
            if  _attr[0] == _attrib:
                return True
        
        return False

    def getAttribute(self, _attrib):
        """ Returns attribute type.
        """
        assert self.hasAttribute(_attrib), "uncaught attribute error %s." % _attrib
        
        for _attr in self.parameters:
            if  _attr[0] == _attrib:
                return _attr[1]
    
    def insert_method(self, _method):
        self.methods.append(_method)

    def hasMethod(self, _method):
        for _meth in self.methods:
            if  _meth[0] == _method:
                return True
        
        return False

    def getMethod(self, _method):
        """ Returns method type.
        """
        assert self.hasMethod(_method), "uncaught attribute error %s." % _method
        
        for _meth in self.methods:
            if  _meth[0] == _method:
                return _meth[1]
    
    #! ==== type specific op ====

    def equality(self, _rhs):
        if  _rhs.istype():
            return operation.op_boolean_t()

        return operation.op_error_t()
