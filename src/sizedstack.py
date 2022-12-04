





class sizedstack(object):
    """ Stack with size. for atom virtual machine
    """

    def __init__(self, _size_t):
        self.__spointer = 0
        self.__internal = []
    
    def push(self, _object):
        self.__internal.append(_object)
       

    def popp(self):
        return self.__internal.pop()
    
    def peek(self):
        return self.__internal[-1]
    
    def bott(self):
        return self.__internal[0]

    def isempty(self):
        return len(self.__internal) <= 0
    
