from .std import std
from .stringstd import stringstd
from .integerstd import integerstd
from .floatstd import floatstd



def getbuiltin(_name):
    match _name:
        case "std":
            return std

        case "stringstd":
            return stringstd
        
        case "integerstd":
            return integerstd
        
        case "floatstd":
            return floatstd

    #! end
    return False