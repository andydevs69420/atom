
class table(object):
    """ Node in symbol table.
    """

    def __init__(self, _parent=None):
        self.head = _parent
        self.tail = None

        #! ====== per types ======
        self.functions = ({})
        self.variables = ({})
        self.enums     = ({})
        self.types     = ({})
    
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

    def name_exist(self, _name):
        """ bottom to up searching.
        """
        _current_scope = self.earlier()

        while _current_scope:
            if  _current_scope.var_exist(_name) or \
                _current_scope.fun_exist(_name)  or \
                _current_scope.enum_exist(_name) or \
                _current_scope.type_exist(_name):
                return True
            
            _current_scope = _current_scope.head

        return False

    def var_exist(self, _name):
        """ local searching.
        """
        return _name in self.variables.keys()
    
    def fun_exist(self, _name):
        """ local searching.
        """
        return _name in self.functions.keys()
    
    def enum_exist(self, _name):
        """ local searching.
        """
        return _name in self.enums.keys()
    
    def type_exist(self, _name):
        """ local searching.
        """
        return _name in self.types.keys()
    
    #! ========== OPERATION ==========

    def get_name(self, _name):
        """ bottom to up retriving.
        """
        assert self.name_exist(_name), "uncaught name error."

        _current = self.earlier()

        while _current:
            if  _current.name_exist(_name):
                if  _current.var_exist(_name):
                    return _current.get_var(_name)
                
                elif _current.fun_exist(_name):
                    return _current.get_func(_name)

                elif _current.enum_exist(_name):
                    return _current.get_enum(_name)
                
                elif _current.type_exist(_name):
                    return _current.get_enum(_name)
            
            _current = _current.head
        
    def get_var(self, _name):
        """ local retriving.
        """
        assert self.var_exist(_name), "uncaught var error."

        #! end
        return self.variables[_name]
    
    def get_func(self, _name):
        """ local retriving.
        """
        assert self.fun_exist(_name), "uncaught fun error."

        #! end
        return self.functions[_name]
    
    def get_enum(self, _name):
        """ local retriving.
        """
        assert self.enum_exist(_name), "uncaught enum error."

        #! end
        return self.enums[_name]
    
    def get_type(self, _name):
        """ local retriving.
        """
        assert self.type_exist(_name), "uncaught type error."

        #! end
        return self.types[_name]

    def insert_variable(self,
        _varname   ,
        _offset    ,
        _datatype  ,
        _isglobal  ,
        _isconstant,
    ):
        self.variables[_varname] = variabletable(_varname, _offset, _datatype, _isglobal, _isconstant)

    def insert_function(self,
        _funcname  ,
        _offset    ,
        _datatype  ,
        _retrtype  ,
        _paramcount,
        _parameters,
    ):
        self.functions[_funcname] = functiontable(_funcname, _offset, _datatype, _retrtype, _paramcount, _parameters)


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
        return not self.head

    def newscope(self):
        self.newtail()
    
    def endscope(self):
        _current = self.earlier()

        #! ensure other
        if _current == self: return

        #! unlink
        _current.head.tail = None

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