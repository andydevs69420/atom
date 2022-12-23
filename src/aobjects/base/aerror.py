


from . import aobject

class aerror(aobject):

    def __init__(self, _error_category_string, _message):
        super().__init__()
        self.error_cat = _error_category_string
        self.message   = _message
    
    def objecthash(self):
        return self.hash("%s -> %s" % (self.error_cat, self.message))
    
    def __str__(self):
        return "%s -> %s" % (self.error_cat, self.message)

    def __repr__(self):
        return self.__str__()
