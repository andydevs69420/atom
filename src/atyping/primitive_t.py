from . import tag_t
from . import operation

class primitive_t(tag_t):
    """ Represents primitive type.
    """

    def __init__(self):
        super().__init__()

    """ Shared.
    """
    def isprimitive(self):
        return True
    
    def lognot(self):
        return operation.BOOL_OP