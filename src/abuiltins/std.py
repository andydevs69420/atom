from aobjects import *
from atyping import *
from error import (error_category, error)

from colorama import init, Fore

init(False, True)

class std:

    metadata = ({

        "printf": nativefn_t(null_t() , 2, [
            ("_format", string_t()), 
            ("_format_args", array_t(any_t()))
        ]), 

        "print": nativefn_t(null_t() , 1, [
            ("_string", any_t()), 
        ]), 

        "scan": nativefn_t(string_t(), 1, [
            ("_message", string_t())
        ]),

        "readFile": nativefn_t(string_t(), 1, [
            ("_path", string_t())
        ]),

        "writeFile": nativefn_t(null_t(), 3, [
            ("_path"  , string_t()),
            ("_data"  , string_t()),
            ("_append", boolean_t())
        ])
    })

    @staticmethod
    def hasmeta(_attribute):
        return _attribute in std.metadata.keys()
    
    @staticmethod
    def getmeta(_attribute):
        assert std.hasmeta(_attribute), "invalid std!"
        return std.metadata[_attribute]
    
    @staticmethod
    def get(_attribute):
        match _attribute:
            case "printf":
                return std.printf
            
            case "print":
                return std.print

            case "scan":
                return std.scan
            
            case "readFile":
                return std.readFile
            
            case "writeFile":
                return std.writeFile
            
            case _:
                raise AttributeError("No such attribute \"%s\"" % _attribute)


    @staticmethod
    def printf(_state, _format, _format_list):
        _fmt = ""
        _tofmt = _format.raw

        _idx = 0
        _slots = 0

        _bracket_stack = []

        while _idx < len(_tofmt):

            _char = _tofmt[_idx]
            
            if  _char == "{":
                _bracket_stack.append(_char)
                _slots += 1

                if _slots > len(_format_list.array): break

                _fmt += _format_list.array[_slots - 1].__str__()
               
            elif _char == "}":
                if  len(_bracket_stack) > 0:
                    _bracket_stack.pop()

                    _idx += 1
                    #! next
                    continue

                #! regular char
                _fmt += _char

            else:
                _fmt += _char
            
            _idx += 1
        
        if  _slots != len(_format_list.array):
            error.raise_fromstack(error_category.StringFormatError, "Not all slots has been formatted, required %d, got %d." % (_slots, len(_format_list.array)), _state.stacktrace)
        
        print("%s%s%s" % (Fore.YELLOW, _fmt, Fore.RESET))
        return anull()


    @staticmethod
    def print(_state, _format):
        print("%s%s%s" % (Fore.YELLOW, _format, Fore.RESET))
        return anull()

    @staticmethod
    def scan(_state, _message):
        _input = ""
        try:
            _input = input(_message.raw)
        except:
            print()
            error.raise_fromstack(error_category.IOError, "keyboard interrupted...", _state.stacktrace)

        return astring(_input)
    
    @staticmethod
    def readFile(_state, _path):
        _input = ""
        try:
            _fobj  = open(_path.raw, "r")
            _input = _fobj.read()
            _fobj.close()
        except:
            print()
            error.raise_fromstack(error_category.FileNotFound, "File not found \"%s\"(No such file or dir)." % _path.raw, _state.stacktrace)

        return astring(_input)
    

    @staticmethod
    def writeFile(_state, _path, _data, _append):
        try:    
            _mode = "a+" if _append.raw else "w"
            _fobj = open(_path.raw, _mode)
            _fobj.write(_data.raw)
            _fobj.close()
        except:
            print()
            error.raise_fromstack(error_category.IOError, "Can't write/make changes to file \"%s\"." % _path.raw, _state.stacktrace)

        return anull()

