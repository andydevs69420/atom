

class frame(object):
    """ Frame for stack.
    """

    def __init__(self, _instructions):
        super().__init__()
        self.ipointer = 00
        self.localref = []
        self.instructions = _instructions
    
    



