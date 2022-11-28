
from names import object_names


class typetable(object):
    """ Typing for atom.
    """

    def __init__(self):
        self.types:str           = []
        self.internal0:typetable = None
        self.internal1:typetable = None
    
    def totype(self):
        _supported_types = []

        for _idx in range(len(self.types)):
            _format =  ""
            _format += self.types[_idx]

            if  not self.internal0:
                _supported_types.append(_format)
                continue

            _format += "["
            _format += self.internal0.totype()

            if   self.internal1:
                _format += ":"
                _format += self.internal1.totype()

            _format += "]"

            _supported_types.append(_format)
        
        #! end
        return _supported_types

    def is_instance(self, _other_type):
        ...