





class stack(object):
    """ Stack implementation for atom.
    """

    def __init__(self, _type:type):
        self.__datatype = _type
        self.__internal = []
    
    
    def generic_push(self, _object):
        self.__internal.append(_object)
    
    def push(self, _object):
        assert type(_object) == self.__datatype, "type error, required \"%s\", got \"%s\"." % (self.__datatype.__name__, type(_object).__name__)
        self.__internal.append(_object)
    
    def popp(self):
        assert not self.isempty(), "empty stack!"
        return self.__internal.pop()
    
    def peek(self):
        assert not self.isempty(), "empty stack!"
        return self.__internal[-1]
    
    def bott(self):
        assert not self.isempty(), "empty stack!"
        return self.__internal[0]
    
    def isempty(self):
        return len(self.__internal) <= 0

    def __len__(self):
        return len(self.__internal)

    def __getitem__(self, _index):
        return self.__internal[_index]

