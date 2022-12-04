from . import tag_t
from . import operation

class nonprimitive_t(tag_t):
    """ Represents non-primitive type.
    """

    def __init__(self):
        super().__init__()

    """ Shared.
    """
    def isnonprimitive(self):
        return True
    
    def lognot(self):
        return operation.op_boolean_t()

