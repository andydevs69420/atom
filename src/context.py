

from enum import Enum


class context(Enum):
    GLOBAL   = 0x00
    LOCAL    = 0x01
    FUNCTION = 0x02
    LOOP     = 0x03
    ARRAY    = 0x04 # for array unpack
    MAP      = 0x05 # for map unpack

