

from enum import Enum


class context(Enum):
    GLOBAL   = 0x00
    LOCAL    = 0x01
    FUNCTION = 0x02
    LOOP     = 0x03

