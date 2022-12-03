from . import nonprimitive_t

class type_t(nonprimitive_t):
    """ User defined types tag.
    """

    def __init__(self, _subtypes):
        super().__init__()
    
    def isuserdefined(self):
        return True
