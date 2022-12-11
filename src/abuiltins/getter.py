from .std import std
from .stringstd import stringstd



def getbuiltin(_name):
    match _name:
        case "std":
            return std
        case "stringstd":
            return stringstd

    #! end
    return False