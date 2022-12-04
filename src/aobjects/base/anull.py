from . import aobject

class anull(aobject):

    def __init__(self):
        super().__init__()
    
    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(anull, _cls).__new__(_cls)
    
        return _cls.instance
    
    def __str__(self):
        return "null"
    
    def __repr__(self):
        return self.__str__()



