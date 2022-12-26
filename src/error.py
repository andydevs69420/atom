
from enum import Enum
from sys import (stderr, exit)

from colorama import init, Fore

init(False, True)

class error_category(Enum):

    IOError       = 0x00
    FileNotFound  = 0x01
    LexicalError  = 0x02
    ParseError    = 0x03
    SemanticError = 0x04
    CompileError  = 0x05
    RuntimeError  = 0x06

    UtfError = 0x07
    NumberFormatError = 0x08
    StringFormatError = 0x09

class error:

    @staticmethod
    def raise_untracked(_category, _message):
        print("%s[%s] %s%s" % (Fore.RED, _category.name, _message, Fore.RESET), file=stderr)
        exit(0x01)
    
    @staticmethod
    def raise_fromstack(_category, _message, _stack):
        print("%s[%s] %s%s" % (Fore.RED, _category.name, _message, Fore.RESET), file=stderr)
        assert len(_stack) > 0, "empty stack!!!!!"
        for _stck in _stack[::-1]:
            print("%s%s%s" % (Fore.RED, _stck, Fore.RESET), file=stderr)
        exit(0x01)
    
    @staticmethod
    def raise_tracked(_category, _message, _location):
        print("%s[%s] %s \n%s%s" % (Fore.RED, _category.name, _message, _location, Fore.RESET), file=stderr)
        exit(0x01)

    
