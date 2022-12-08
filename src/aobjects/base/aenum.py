from . import aobject


class aenum(aobject):

    def __init__(self, _enumname):
        super().__init__()
        self.enumname = _enumname

    def __str__(self):
        _fmt  = ""
        _fmt += "enum " + self.enumname + "\n{\n"
        
        _keys = self.keys()

        _idx = 0
        for _k, _v in zip(_keys, self.values()):
            _fmt += "    " + _k.__str__() + " = " + _v.__repr__()

            if  _idx < (len(_keys) - 1):
                _fmt += ", "
            
            
            _fmt += "\n"

            _idx += 1

        _fmt += "}"
        return _fmt
    
    def __repr__(self):
        return super().__str__()

