
class table(object):
    """ Node in symbol table.
    """

    def __init__(self, _parent=None):
        self.head = _parent
        self.tail = None
        self.currentscope = self

        #! ====== per types ======
        self.names = ({})
    
    def earlier(self):
        if  not self.tail:
            return self
        #! end
        return self.tail.earlier()

    def newtail(self):
        if  not self.tail:
            self.tail = table(self)
            return
        
        #! recurse
        self.tail.newtail()
    
    #! ========== CHECKER ==========

    def name_exist_globally(self, _name):
        """ Checks if "_name" exist from current scope until top scope.
            bottom to up searching.

            Returns
            -------
            bool
        """
        _current_scope = self.currentscope

        while _current_scope:
            if  _name in _current_scope.names.keys():
                #! end
                return True
            
            #! next
            _current_scope = _current_scope.head

        #! end
        return False
    
    def name_exist_locally(self, _name):
        """ Checks if "_name" exist in current scope.
            local searching.
        """
        return _name in self.currentscope.names.keys()
    
    #! ========== OPERATION ==========

    def lookup(self, _name):
        """ bottom to up retriving.
        """
        assert self.name_exist_globally(_name), "uncaught name error."

        _current = self.currentscope

        while _current:
            if  _name in _current.names.keys():
                #! end
                return _current.names[_name]
            
            #! next
            _current = _current.head

        #! if reached here. means error
        raise

    def insert_variable(self,
        _varname   ,
        _offset    ,
        _datatype  ,
        _isglobal  ,
        _isconstant,
    ):
        self.currentscope.names[_varname] = variabletable(_varname, _offset, _datatype, _isglobal, _isconstant)

    def insert_function(self,
        _funcname  ,
        _offset    ,
        _datatype  ,
        _retrtype  ,
        _paramcount,
        _parameters,
    ):
        self.currentscope.names[_funcname] = functiontable(_funcname, _offset, _datatype, _retrtype, _paramcount, _parameters)


class symboltable(table):
    """ The symboltble class.
    """
    
    def __init__(self, _parent=None):
        super().__init__(_parent)

    def __new__(_cls):
        if  not hasattr(_cls, "instance"):
            _cls.instance = super(symboltable, _cls).__new__(_cls)
    
        return _cls.instance
    
    def is_global(self):
        return not self.currentscope.head

    def newscope(self):
        self.newtail()

        #! set new current
        self.currentscope = self.earlier()
    
    def endscope(self):
        _current = self.earlier()

        #! ensure other
        if _current == self: return

        #! unlink
        _current.head.tail = None

        #! set new current
        self.currentscope = self.earlier()

        #! end
        return _current


class typetable(object):

    def __init__(self):
        pass
    
    def get_name(self):...

    def get_offset(self):...

    def get_datatype(self):...

    def is_global(self):...

    def is_constant(self):...


class functiontable(typetable):
    """ Function table for atom.
    """

    def __init__(self, _funcname, _offset, _datatype, _retrtype, _paramcount, _parameters):
        super().__init__()
        self.funcname   = _funcname
        self.offset     = _offset
        self.datatype   = _datatype
        self.retrtype   = _retrtype
        self.paramcount = _paramcount
        self.parameters = _parameters
    
    def is_global(self):
        return True
    
    def is_constant(self):
        return True



class variabletable(typetable):
    """ Variable table for atom.
    """

    def __init__(self, _varname, _offset, _datatype, _isglobal, _isconstant):
        super().__init__()
        self.varname    = _varname
        self.offset     = _offset
        self.datatype   = _datatype
        self.isglobal   = _isglobal
        self.isconstant = _isconstant
    
    def get_name(self):
        return self.varname
    
    def get_offset(self):
        return self.offset

    def get_datatype(self):
        return self.datatype
    
    def is_global(self):
        return self.isglobal
    
    def is_constant(self):
        return self.isconstant

#! END