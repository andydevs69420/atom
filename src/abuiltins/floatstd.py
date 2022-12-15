from aobjects import *
from atyping import *
from error import (error_category, error)


class floatstd:

    metadata = ({

        "ftoa": nativefn_t(string_t() , 1, [
            ("__float__", float_t()), 
        ]), 
    })

    @staticmethod
    def hasmeta(_attribute):
        return _attribute in floatstd.metadata.keys()
    
    @staticmethod
    def getmeta(_attribute):
        assert floatstd.hasmeta(_attribute), "invalid std!"
        return floatstd.metadata[_attribute]
    
    @staticmethod
    def get(_attribute):
        match _attribute:
            case "ftoa":
                return floatstd.ftoa
            
            case _:
                raise AttributeError("No such attribute \"%s\"" % _attribute)
    @staticmethod
    def ftoa(_state, __float__):
        return astring(str(__float__.raw))
