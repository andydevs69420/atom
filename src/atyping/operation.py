from enum import Enum

class operation(Enum):
    INT_OP   = 0x01
    FLOAT_OP = 0x02
    STR_OP   = 0x03
    BOOL_OP  = 0x04
    NULL_OP  = 0x05
    ARRAY_UNPACK = 0x06
    MAP_UNPACK   = 0x07
    BAD_OP   = 0x08
