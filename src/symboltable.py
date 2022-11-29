
class table(object):
    """ Node in symbol table.
    """

    def __init__(self, _parent=None):
        self.head = _parent
        self.tail = None

        #! ====== per types ======
        self.functions = ({})
        self.variables = ({})
    
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
    
    #! ========== OPERATION ==========

    def var_exist_locally(self, _name):
        return _name in self.earlier().variables.keys()
    
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
        _datatype  ,
        _retrtype  ,
        _paramcount,
        _parameters,
    ):
        self.functions[_funcname] = functiontable(_funcname, _datatype, _retrtype, _paramcount, _parameters)


class symboltable(table):
    """ The symboltble class.
    """

    def __init__(self):
        super().__init__(None)

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



class functiontable(object):
    """ Function table for atom.
    """

    def __init__(self, _funcname, _datatype, _retrtype, _paramcount, _parameters):
        self.funcname   = _funcname
        self.datatype   = _datatype
        self.retrtype   = _retrtype
        self.paramcount = _paramcount
        self.parameters = _parameters






class variabletable(object):
    """ Variable table for atom.
    """

    def __init__(self, _varname, _offset, _datatype, _isglobal, _isconstant):
        self.varname    = _varname
        self.offset     = _offset
        self.datatype   = _datatype
        self.isglobal   = _isglobal
        self.isconstant = _isconstant

