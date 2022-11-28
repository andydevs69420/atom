
from enum import Enum
from . import object_names


class operation(Enum):
    INT_OP   = 0x01
    FLOAT_OP = 0x02
    STR_OP   = 0x03
    BAD_OP   = 0x04


class typetable(object):
    """ Typing for atom.
    """

    def __init__(self):
        self.types:str           = []
        self.internal0:typetable = None
        self.internal1:typetable = None
    
    def repr(self):
        return self.totype()[0]

    def totype(self):
        """ Generates supported type.

            Example
            -------
            struct X, Y {
                ...
                ...
            };

            let x_instances = [X(..., ...), Y(..., ...)];

            Genearates
            ----------
            [array[X], array[Y]]
        """
        _supported_types = []

        for _idx in range(len(self.types)):
            _format =  ""
            _format += self.types[_idx]

            if  not self.internal0:
                _supported_types.append(_format)
                continue

            _format += "["
            _format += self.internal0.totype()

            if   self.internal1:
                _format += ":"
                _format += self.internal1.totype()

            _format += "]"

            _supported_types.append(_format)
        
        #! end
        return _supported_types
    
    #! ========= SINGULAR =========

    @staticmethod
    def is_number(_type):
        #! short
        return  typetable.is_float(_type) or \
                typetable.is_integer(_type)
    
    @staticmethod
    def is_integer(_type):
        return bool(object_names.INT in \
            _type.totype())
          
    @staticmethod
    def is_float(_type):
        return bool(object_names.FLOAT in \
            _type.totype())
    
    @staticmethod
    def is_string(_type):
        return bool(object_names.STR in \
            _type.totype())
    
    @staticmethod
    def is_bool(_type):
        return bool(object_names.BOOL in \
            _type.totype())
    
    @staticmethod
    def is_null(_type):
        return bool(object_names.NULL in \
            _type.totype())

    #! ========= PLURAL =========

    @staticmethod
    def are_numbers(_left, _right):
        return  typetable.is_number(_left ) and \
                typetable.is_number(_right)
    
    @staticmethod
    def are_integers(_left, _right):
        return  typetable.is_integer(_left ) and \
                typetable.is_integer(_right)
    
    @staticmethod
    def are_floats(_left, _right):
        return  typetable.is_float(_left ) and \
                typetable.is_float(_right)
    
    @staticmethod
    def are_strings(_left, _right):
        return  typetable.is_number(_left ) and \
                typetable.is_number(_right)
    
    @staticmethod
    def are_booleans(_left, _right):
        return  typetable.is_bool(_left ) and \
                typetable.is_bool(_right)


    #! ======== PER TYPE OPS =====

    def exponent(self, _right):
        """ Only numbers can be raised.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            #! cast as int op
            if typetable.are_integers(self, _right): return operation.INT_OP
            
            #! cast as float op
            return operation.FLOAT_OP

        #! end
        return operation.BAD_OP

    def multiply(self, _right):
        """ Only numbers can be multiplied.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            #! cast as int op
            if typetable.are_integers(self, _right): return operation.INT_OP
            
            #! cast as float op
            return operation.FLOAT_OP

        #! end
        return operation.BAD_OP
    
    def divide(self, _right):
        """ Only numbers can be divided.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            #! cast as float op
            return operation.FLOAT_OP

        #! end
        return operation.BAD_OP

    def plus(self, _right):
        """ Only numbers(float, int) and string can be added.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            #! cast as int op
            if typetable.are_integers(self, _right): return operation.INT_OP
            
            #! cast as float op
            return operation.FLOAT_OP

        elif typetable.are_strings(self, _right):
            #! string concat
            return operation.STR_OP
        
        #! end
        return operation.BAD_OP
    

    def minus(self, _right):
        """ Only numbers can be subtracted.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            #! cast as int op
            if typetable.are_integers(self, _right): return operation.INT_OP
            
            #! cast as float op
            return operation.FLOAT_OP

        #! end
        return operation.BAD_OP