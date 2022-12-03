from . import operation
from . import primitive_t

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

