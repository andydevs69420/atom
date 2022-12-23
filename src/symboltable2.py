""" LinkedList of HashTable
"""

from stack import stack

class Node(object):
    """ Base node for LinkedList.
    """

    def __init__(self, _key, _val):
        self.head = None
        self.tail = None
        self.nkey = _key
        self.nval = _val
    

class LinkedList(Node):
    """ LinkedList base.
    """

    def __init__(self, _key, _val):
        super().__init__(_key, _val)
    

    def append(self, _key, _val):
        _head = self
        while _head:
            if  _head.nkey == _key:
                #! update
                _head.nval  = _val
                return
            
            if  not _head.tail:
                _head.tail = Node(_key, _val)
                return

            _head = _head.tail


class HashTable(object):
    """ HashTable base.
    """

    LOAD_FACTOR = 0.75

    def __init__(self):
        self.__htsize = 16
        self.__elsize = 0
        self.__bucket = [None for _r in range(self.__htsize)]

    
    def put(self, _key, _value):
        
        _index = self.hash(_key) % self.__htsize
        
        if  self.__bucket[_index]:
            #! collision
            self.__bucket[_index].append(_key, _value)

            #! end
            return

        self.__bucket[_index] = LinkedList(_key, _value)
        self.__elsize += 1

        if  (float(self.__elsize) / self.__htsize) > HashTable.LOAD_FACTOR:
            self.rehash()
    

    def get(self, _key):
        _headt = self.__bucket[self.hash(_key) % self.__htsize]

        while _headt:
            #! check
            if _headt.nkey == _key: return _headt.nval

            #! next
            _headt = _headt.tail
        
        raise KeyError("key \"%s\" not found." % _key)

    def haskey(self, _key):
        _index = self.hash(_key) % self.__htsize

        if  not self.__bucket[_index]:
            return False

        _head = self.__bucket[_index]

        while _head:
            #! check
            if _head.nkey == _key: return True

            #! next
            _head = _head.tail
        
        return False
    
    def rehash(self):
        _bucket = self.__bucket

        self.__htsize *= 2
        self.__elsize  = 0
        self.__bucket  = [None for _r in range(self.__htsize)]

        for _cell in _bucket:
            if  _cell:
                _head = _cell

                while _head:
                    #! re-insert
                    self.put(_head.nkey, _head.nval)
                    
                    #! next
                    _head = _head.tail
    
    def hash(self, _key):
        if type(_key) == int: return _key

        assert type(_key) == str, "Nah!"

        _hashcode = 69420
        
        for _idx in range(len(_key)):
            _hashcode  = ((_hashcode << 5) - _hashcode) + ord(_key[_idx])
            _hashcode |= 0
        
        return _hashcode
    
    def aslist(self):
        _children = []
        
        for _chain in self.__bucket:
            #! next element
            if  not _chain: continue

            #! 
            _head = _chain
            while _head:
                #! append current
                _children.append((_head.nkey, _head.nval))

                #! next tail
                _head = _head.tail
        
        return _children
    
    def keys(self):
        _keys = []
        
        for _chain in self.__bucket:
            #! next element
            if  not _chain: continue

            #! 
            _head = _chain
            while _head:
                #! append current
                _keys.append(_head.nkey)

                #! next tail
                _head = _head.tail
        
        return _keys


class SymbolTable(HashTable):
    """ SymbolTable base.

        Bottom to up.
    """

    def __init__(self, _parent=None):
        super().__init__()
        self.upperscope = _parent
        self.childnodes = stack(SymbolTable)
    
    #! ======== checker ========
    
    def isglobal(self):
        #! check
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self

        #! end
        return not (not (not _top.upperscope))

    def contains(self, _name):
        """ Check for global name.
        """
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self

        while _top:
            #! check
            if _top.haskey(_name): return True

            #! next
            _top = _top.upperscope

        #! end
        return False

    def haslocal(self, _name):
        """ Check for local name.
        """
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        return _top.haskey(_name)

    #! ======= operation =======
    
    def insert(self, _key, _value):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_key, _value)
    
    def insert_var(self,
        _varname   ,
        _offset    ,
        _datatype  ,
        _isglobal  ,
        _isconstant,
        _site      ,
    ):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_varname, variabletable(_varname, _offset, _datatype, _isglobal, _isconstant, _site))
    
    def insert_fun(self,
        _funcname,
        _offset  ,
        _datatype,
        _retrtype,
        _site    ,
    ):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_funcname, functiontable(_funcname, _offset, _datatype, _retrtype, _site))
    
    def insert_struct(self,
        _structname ,
        _offset     ,
        _datatype   ,
        _site       ,
    ):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_structname, structtable(_structname, _offset, _datatype, _site))

    def insert_enum(self,
        _enumname ,
        _offset   ,
        _datatype ,
        _site     ,
    ):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_enumname, enumtable(_enumname, _offset, _datatype, _site))

    def insert_module(self,
        _modname   ,
        _offset    ,
        _datatype  ,
        _isglobal  ,
        _isconstant,
        _site      ,
    ):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self
        
        #! insert
        _top.put(_modname, moduletable(_modname, _offset, _datatype, _isglobal, _isconstant, _site))

    def lookup(self, _key):
        #! check bottom
        _top = self.childnodes.peek() if not self.childnodes.isempty() else self

        while _top:
            #! check
            if _top.haskey(_key): return _top.get(_key)

            #! next
            _top = _top.upperscope

        #! end
        raise KeyError("key not found \"%s\"." % _key)
    
    #! child scope
    def newscope(self):
        """ Creates new symboltable node.
        """
        self.childnodes.push(SymbolTable(_parent=self if self.childnodes.isempty() else self.childnodes.peek()))
    
    def endscope(self):
        """ Removes scope from hierarchy.
        """
        return\
        self.childnodes.popp()
    
    #! stand alone scope
    def newparentscope(self):
        """ Creates new symboltable node.
        """
        self.childnodes.push(SymbolTable())
    
    def endparentscope(self):
        """ Creates new symboltable node.
        """
        return\
        self.childnodes.popp()



class typetable(object):

    def __init__(self):pass
    
    def get_name(self):...

    def get_offset(self):...

    def get_datatype(self):...

    def is_global(self):...

    def is_constant(self):...


class functiontable(typetable):
    """ Function table for atom.
    """

    def __init__(self, _funcname, _offset, _datatype, _retrtype, _site):
        super().__init__()
        self.funcname   = _funcname
        self.offset     = _offset
        self.datatype   = _datatype
        self.retrtype   = _retrtype
        self.site       = _site
    
    def get_name(self):
        return self.funcname
    
    def get_offset(self):
        return self.offset
    
    def get_returntype(self):
        return self.retrtype
    
    def get_datatype(self):
        return self.datatype
    
    def is_global(self):
        return True
    
    def is_constant(self):
        return True
    
    def get_site(self):
        return self.site


class structtable(typetable):
    """ struct table for atom.
    """

    def __init__(self, _structname, _offset, _datatype, _site):
        super().__init__()
        self.structname = _structname
        self.offset     = _offset
        self.datatype   = _datatype
        self.site       = _site
    
    def get_name(self):
        return self.varname
    
    def get_offset(self):
        return self.offset

    def get_datatype(self):
        return self.datatype
    
    def is_global(self):
        return True
    
    def is_constant(self):
        return True
    
    def get_site(self):
        return self.site

class enumtable(typetable):
    """ enum table for atom.
    """

    def __init__(self, _enumname, _offset, _datatype, _site):
        super().__init__()
        self.structname = _enumname
        self.offset     = _offset
        self.datatype   = _datatype
        self.site       = _site
    
    def get_name(self):
        return self.structname
    
    def get_offset(self):
        return self.offset

    def get_datatype(self):
        return self.datatype
    
    def is_global(self):
        return True
    
    def is_constant(self):
        return True
    
    def get_site(self):
        return self.site

class variabletable(typetable):
    """ Variable table for atom.
    """

    def __init__(self, _varname, _offset, _datatype, _isglobal, _isconstant, _site):
        super().__init__()
        self.varname    = _varname
        self.offset     = _offset
        self.datatype   = _datatype
        self.isglobal   = _isglobal
        self.isconstant = _isconstant
        self.site       = _site
    
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
    
    def get_site(self):
        return self.site

class moduletable(typetable):
    """ Module table for atom.
    """

    def __init__(self, _modname, _offset, _datatype, _isglobal, _isconstant, _site):
        super().__init__()
        self.modname    = _modname
        self.offset     = _offset
        self.datatype   = _datatype
        self.isglobal   = _isglobal
        self.isconstant = _isconstant
        self.site       = _site
    
    def get_name(self):
        return self.modname
    
    def get_offset(self):
        return self.offset

    def get_datatype(self):
        return self.datatype
    
    def is_global(self):
        return self.isglobal
    
    def is_constant(self):
        return self.isconstant
    
    def get_site(self):
        return self.site

#! END



if  __name__ == "__main__":
    _st = SymbolTable()
    _st.insert("Marielle", 10000000)
    _st.insert("Andy", 23)
    print(_st.lookup("Andy"))
    _st.insert("Andy2", 20000)

    _st.newscope() #1

    _st.insert("Andy2", 200)
    print(_st.lookup("Andy2"))

    _st.newscope()      #2
    _st.insert("Marielle", 100)
    print(_st.lookup("Marielle"))
    _st.endscope()      #2

    print(_st.lookup("Marielle"))

    _st.endscope() #1

    print(_st.lookup("Andy2"))




