from .std import std



def getbuiltin(_name):
    match _name:
        case "std":
            return std

    #! end
    return False