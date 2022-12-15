from aobjects import *
from atyping import *
from error import (error_category, error)


class integerstd:

    metadata = ({

        "itoa": nativefn_t(string_t() , 1, [
            ("__integer__", integer_t()), 
        ]), 
    })

    @staticmethod
    def hasmeta(_attribute):
        return _attribute in integerstd.metadata.keys()
    
    @staticmethod
    def getmeta(_attribute):
        assert integerstd.hasmeta(_attribute), "invalid std!"
        return integerstd.metadata[_attribute]
    
    @staticmethod
    def get(_attribute):
        match _attribute:
            case "itoa":
                return integerstd.itoa
            
            case _:
                raise AttributeError("No such attribute \"%s\"" % _attribute)
    @staticmethod
    def itoa(_state, __integer__):
        return astring(str(__integer__.raw))
