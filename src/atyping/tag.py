from . import operation


class tag_t(object):
    """ Abstract class tag_t. base class of all tag.
    """

    def __init__(self):
        pass
    
    def repr(self):raise NotImplementedError("Holly shake! not overridden.")
    def matches(self, _rhs):raise NotImplementedError("Holly shake! not overridden.")

    #! ======= checker =======
    def isprimitive(self):return False
    def isnonprimitive(self): False
    def isany(self):return False
    def isint(self):return False
    def isfloat(self):return False
    def isstring(self):return False
    def isboolean(self):return False
    def isnull(self):return False
    def isarray(self):return False
    def isfunction(self): return False
    def ismap(self):return False
    def isuserdefined(self):return False

    #! ======== operation =======
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


    #! ====== member check ========
    """ Checks if an object hass attribute.
    """
    def hasAttribute(self, _attribute):return False
