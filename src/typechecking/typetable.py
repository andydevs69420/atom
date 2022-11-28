
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
        return typetable.is_float(_type) or typetable.is_integer(_type)
    
    @staticmethod
    def is_integer(_type):
        for _each_type in _type.totype():
            if  _each_type == object_names.INT:
                return True
        #! end
        return False
    
    @staticmethod
    def is_float(_type):
        for _each_type in _type.totype():
            if  _each_type == object_names.FLOAT:
                return True
        #! end
        return False
    
    @staticmethod
    def is_string(_type):
        for _each_type in _type.totype():
            if  _each_type == object_names.STR:
                return True
        #! end
        return False

    #! ========= PLURAL =========

    @staticmethod
    def are_numbers(_left, _right):
        return typetable.is_number(_left) and typetable.is_number(_right)
    
    @staticmethod
    def are_strings(_left, _right):
        return typetable.is_number(_left) and typetable.is_number(_right)


    #! ======== PER TYPE OPS =====

    def plus(self, _right):
        """ Only numbers(float, int) and string can be added.

            Returns
            -------
            operation 
        """
        if  typetable.are_numbers(self, _right):
            return 

        elif typetable.are_strings(self, _right):
            return operation.STR_OP
        
        #! end
        return operation.BAD_OP
