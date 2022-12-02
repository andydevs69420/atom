





class sizedstack(object):
    """ Stack with size. for atom virtual machine
    """

    def __init__(self, _size_t):
        self.__spointer = 0
        self.__internal = [None for _r in range(_size_t)]
    
    def push(self, _object):
        self.__internal[self.__spointer] = _object
        self.__spointer += 1

    def popp(self):
        assert (self.__spointer >= 0), "Stack Underflow!!!"
        _top = self.__internal[self.__spointer - 1]
        self.__spointer -= 1
        return _top
    
    def peek(self):
        return self.__internal[self.__spointer - 1]
    
    def isempty(self):
        return self.__spointer <= 0

