


class frame(object):
    """ Frame for stack.
    """

    def __init__(self, _instructions):
        super().__init__()
        self.ipointer = 00
        self.instructions = _instructions
        self.value = []


    def set(self, _offset, _value):
        #! end
        if  _offset < len(self.value):
            self.value[_offset] = _value
            return
        #! append
        self.value.append(_value)
    
    def get(self, _offset):
        return self.value[_offset]


