from enum import Enum
from builtins import repr

class token_type(Enum):
    IDENTIFIER = 0x01
    INTEGER    = 0x02
    FLOAT      = 0x03
    STRING     = 0x04
    SYMBOL     = 0x05
    EOF        = 0x06


class atoken(object):
    """ Token for atom.
    """

    def __init__(self, _ttype, _line_offset, _colm_offset):
        self.ttype = _ttype
        self.value = None
        self.ln_of = _line_offset
        self.cm_of = _colm_offset

    def __str__(self):
        return "Token(type: %s, value: %s);" % (self.ttype.name, repr(self.value))
    
    @staticmethod
    def make_location_from_offsets(_file, _code, _line_start, _line_end, _colm_start, _colm_end):
        
        ...