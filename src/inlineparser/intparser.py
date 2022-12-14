

def parseInt(_int__str):
    #! non regex validator
    
    _check = (lambda c: (c >= 0x30 and c <= 0x39))

    for _i in _int__str:
        if not _check(ord(_i)): return False
    
    #! end
    return int(_int__str)


