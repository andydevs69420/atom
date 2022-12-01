from enum import Enum
from . import type_names


__ALL = __all__ = [
            "operation", 
            "tag_t",
            "any_t" ,
            "integer_t", 
            "float_t", 
            "string_t", 
            "boolean_t", 
            "null_t",
            "array_t",
            "map_t",
            "user_t"]

class operation(Enum):
    INT_OP   = 0x01
    FLOAT_OP = 0x02
    STR_OP   = 0x03
    BOOL_OP  = 0x04
    NULL_OP  = 0x05
    ARRAY_UNPACK = 0x06
    MAP_UNPACK   = 0x07
    BAD_OP   = 0x08


class tag_t(object):
    """ Abstract class tag_t. base class of all tag.
    """

    def __init__(self):
        pass
    
    def repr(self):raise NotImplementedError("Holly shake! not overridden.")
    def isprimitive(self):return False
    def isnonprimitive(self): False
    def isany(self):return False
    def isint(self):return False
    def isfloat(self):return False
    def isstring(self):return False
    def isboolean(self):return False
    def isnull(self):return False
    def isarray(self):return False
    def ismap(self):return False
    def isuserdefined(self):return False

    """ If its not overridden, then the operator is not applicable for its operand(s).
    """
    def bitnot(self):return operation.BAD_OP
    def lognot(self):return operation.BAD_OP
    def pos(self):return operation.BAD_OP
    def neg(self):return operation.BAD_OP
    def unpack(self):return operation.BAD_OP
    def pow(self, _rhs):return operation.BAD_OP
    def mul(self, _rhs):return operation.BAD_OP
    def div(self, _rhs):return operation.BAD_OP
    def mod(self, _rhs):return operation.BAD_OP
    def add(self, _rhs):return operation.BAD_OP
    def sub(self, _rhs):return operation.BAD_OP
    def shift(self, _rhs):return operation.BAD_OP
    def relational(self, _rhs):return operation.BAD_OP
    def equality(self, _rhs):return operation.BAD_OP
    def bitwise(self, _rhs):return operation.BAD_OP



class primitive_t(tag_t):
    """ Represents primitive type.
    """

    def __init__(self):
        super().__init__()

    """ Shared.
    """
    def isprimitive(self):
        return True
    
    def lognot(self):
        return operation.BOOL_OP

class nonprimitive_t(tag_t):
    """ Represents non-primitive type.
    """

    def __init__(self):
        super().__init__()

    """ Shared.
    """
    def isnonprimitive(self):
        return True
    
    def lognot(self):
        return operation.BOOL_OP

class any_t(tag_t):
    """ Any type, usually those type whose undetermined at compile-time.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.ANY
    
    def repr(self):
        return self.name
    
    def isany(self):
        return True

class number_t(primitive_t):
    """ Base tag or int and float.
    """

    def __init__(self):
        super().__init__()

    def pos(self):
        if  self.isint():
            return operation.INT_OP

        elif self.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP
    
    def neg(self):
        if  self.isint():
            return operation.INT_OP

        elif self.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP
    
    #! ============= arithmetic =============

    def pow(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.INT_OP

        elif self.isfloat() or _rhs.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP

    def mul(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.INT_OP

        elif self.isfloat() or _rhs.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP
    
    def div(self, _rhs):
        if  self.isint() or _rhs.isfloat():
            return operation.FLOAT_OP

        #! end
        return operation.BAD_OP
    
    def mod(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.INT_OP

        elif self.isfloat() or _rhs.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP

    def add(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.INT_OP

        elif self.isfloat() or _rhs.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP
    
    def sub(self, _rhs):
        if  self.isint() and _rhs.isint():
            return operation.INT_OP

        elif self.isfloat() or _rhs.isfloat():
            return operation.FLOAT_OP
        
        #! end
        return operation.BAD_OP
    

    #! ========= relational group ==========
    
    def relational(self, _rhs):
        if  _rhs.isprimitive():
            return operation.BOOL_OP

        #! end
        return operation.BAD_OP
    
    

    #! ============= equality =============

    def equality(self, _rhs):
        if  _rhs.isprimitive():
            return operation.BOOL_OP

        #! end
        return operation.BAD_OP


class integer_t(number_t):
    """ Integer compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.INT
    
    def repr(self):
        return self.name

    def isint(self):
        return True
    
    #! ==== integer specific op ====

    def bitnot(self):
        return operation.INT_OP

    def shift(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.INT_OP
        
        #! end
        return operation.BAD_OP
    
    def bitwise(self, _rhs):
        if  _rhs.isint() or _rhs.isboolean():
            return operation.INT_OP
        
        #! end
        return operation.BAD_OP

    
class float_t(number_t):
    """ Float compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.FLOAT
    
    def repr(self):
        return self.name
    
    def isfloat(self):
        return True


class boolean_t(primitive_t):
    """ Boolean compiletime tag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.BOOL
    
    def repr(self):
        return self.name
    
    def isboolean(self):
        return True


class null_t(primitive_t):
    """ Null compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.NULL
    
    def repr(self):
        return self.name
    
    def isnull(self):
        return True


class string_t(nonprimitive_t):
    """ String compiletime flag.
    """

    def __init__(self):
        super().__init__()
        self.name = type_names.STR
    
    def repr(self):
        return self.name
    
    def isstring(self):
        return True

    #! ==== string specific op ====

    def add(self, _rhs):
        if  _rhs.isstring():
            return operation.STR_OP
        
        #! end
        return operation.BAD_OP

class array_t(nonprimitive_t):
    """ Array compiletime tag.
    """

    def __init__(self, _elementtype):
        super().__init__()
        self.name = type_names.ARRAY
        self.elementtype = _elementtype
    
    def repr(self):
        return self.name + "[" + self.elementtype.repr() + "]"
    
    def isarray(self):
        return True

    #! ==== array specific op ====

    def unpack(self):
        return operation.ARRAY_UNPACK

class map_t(nonprimitive_t):
    """ Map compiletime tag.
    """

    def __init__(self, _keytype, _valtype):
        super().__init__()
        self.name = type_names.MAP
        self.keytype = _keytype
        self.valtype = _valtype
        
    def repr(self):
        return self.name + "[" + self.keytype.repr() + ":" + self.valtype.repr() + "]"

    def ismap(self):
        return True
    
    #! ==== map specific op ====
    
    def unpack(self):
        return operation.MAP_UNPACK


class user_t(nonprimitive_t):
    """ User defined types tag.
    """

    def __init__(self, _subtypes):
        super().__init__()
    
    def isuserdefined(self):
        return True
