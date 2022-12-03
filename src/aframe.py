

class frame(object):
    """ Frame for stack.
    """

    def __init__(self, _instructions):
        super().__init__()
        self.ipointer = 00
        self.instructions = _instructions
        self.value = []


    def set(self, _offset, _value):
        if  len(self.value) - 1 > _offset:
            self.value[_offset] = _value
            return
        #! end
        self.value.append(_value)
    
    def get(self, _offset):
        return self.value[_offset]


