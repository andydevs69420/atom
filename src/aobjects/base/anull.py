from . import aobject

class anull(aobject):

    def __init__(self):
        super().__init__()
        self.raw = None
    
    def all(self):
        return self.keys() + self.values()
    
    def __str__(self):
        return "null"
    
    def __repr__(self):
        return self.__str__()



