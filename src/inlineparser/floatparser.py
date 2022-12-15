
def floatParse(_float__string):
    """ Valid float ("digit" '.' "digit")

        Invalid float ('.' "digit") | ("digit" '.')
    """
    _score  = 0
    #! digit check
    _check0 = (lambda c: (c >= 0x30 and c <= 0x39))
    
    _idx = 0

    _iseol = (lambda _idx: (_idx >= len(_float__string)))


    if  not _iseol(_idx):
        while not _iseol(_idx) and _check0(ord(_float__string[_idx])): 
            _score += 1
            _idx   += 1

    _has_dot = False

    if  not _iseol(_idx):
        if  _float__string[_idx] == ".":
            _has_dot = True
            _score += 1
            _idx   += 1

    if  not _iseol(_idx):
        while not _iseol(_idx) and _check0(ord(_float__string[_idx])): 
            _score += 1
            _idx   += 1
            _has_dot = False

    #! end
    return float(_float__string) if (_score == len(_float__string) and not _has_dot) else False

