
from enum import Enum
from sys import (stderr, exit)

class error_category(Enum):

    IOError      = 0x00
    LexicalError = 0x01
    ParseError   = 0x02

class error:

    @staticmethod
    def raise_untracked(_category, _message):
        print("[%s] %s" % (_category.name, _message), file=stderr)
        exit(0x01)
    
    @staticmethod
    def raise_tracked(_category, _message, _location):
        print("[%s] %s \n%s" % (_category.name, _message, _location), file=stderr)
        exit(0x01)