from aobjects import *
from atyping import *

class std:

    metadata = ({

        "printf": nativefn_t(null_t() , 2, [
            ("_format", string_t()), 
            ("_format_args", array_t(any_t()))
        ]), 

        "print": nativefn_t(null_t() , 1, [
            ("_string", any_t()), 
        ]), 

        "readl" : nativefn_t(string_t(), 1, [
            ("_message", string_t())
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

            case "readl":
                return std.readl
            
            case _:
                raise AttributeError("No such attribute \"%s\"" % _attribute)


    @staticmethod
    def printf(_state, _format, _format_list):
        ...

    @staticmethod
    def print(_state, _format):
        print(_format)
        return anull()

    @staticmethod
    def readl(_state, _message):
        ...
        return astring(input(_message.raw))
