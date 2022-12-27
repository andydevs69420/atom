

from enum import Enum


class context(Enum):
    GLOBAL   = 0x00
    LOCAL    = 0x01
    FUNCTION = 0x02
    METHOD   = 0x03
    LOOP     = 0x04
    ARRAY    = 0x05 # for array unpack
    MAP      = 0x06 # for map unpack

