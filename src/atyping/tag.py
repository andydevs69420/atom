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
    def isfunction(self):return False
    def isnativefunction(self):return False
    def ismap(self):return False
    def istype(self):return False
    def iserror(self):return False

    #! ======== operation =======
    """ If its not overridden, then the operator is not applicable for its operand(s).
    """
    def bitnot(self):return operation.op_error_t()
    def lognot(self):return operation.op_error_t()
    def pos(self):return operation.op_error_t()
    def neg(self):return operation.op_error_t()
    def unpack(self):return operation.op_error_t()
    def pow(self, _rhs):return operation.op_error_t()
    def mul(self, _rhs):return operation.op_error_t()
    def div(self, _rhs):return operation.op_error_t()
    def mod(self, _rhs):return operation.op_error_t()
    def add(self, _rhs):return operation.op_error_t()
    def sub(self, _rhs):return operation.op_error_t()
    def shift(self, _rhs):return operation.op_error_t()
    def relational(self, _rhs):return operation.op_error_t()
    def equality(self, _rhs):return operation.op_error_t()
    def bitwise(self, _rhs):return operation.op_error_t()
