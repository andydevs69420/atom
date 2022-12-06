


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
            if  _head.nkey.objecthash() == _key.objecthash():
                #! update
                _head.nval  = _val
                return
            
            if  not _head.tail:
                _head.tail = Node(_key, _val)
                return

            _head = _head.tail


class HashMap(object):
    """ HashMap base.
    """

    LOAD_FACTOR = 0.75

    def __init__(self):
        super().__init__()
        self.__htsize = 16
        self.__elsize = 0
        self.__bucket = [None for _r in range(self.__htsize)]

    
    def put(self, _key, _value):    
        _index  = _key.objecthash() % self.__htsize
        
        if  self.__bucket[_index]:
            #! collision
            self.__bucket[_index].append(_key, _value)
           
            #! end
            return

        self.__bucket[_index] = LinkedList(_key, _value)
        self.__elsize += 1

        if  (float(self.__elsize) / self.__htsize) > HashMap.LOAD_FACTOR:
            self.rehash()
    

    def get(self, _key):
        _headt = self.__bucket[_key.objecthash() % self.__htsize]

        while _headt:
            #! check
            if _headt.nkey.objecthash() == _key.objecthash(): return _headt.nval

            #! next
            _headt = _headt.tail
        
        raise KeyError("key \"%s\" not found." % _key)

    def haskey(self, _key):
        _index = _key.objecthash() % self.__htsize

        if  not self.__bucket[_index]:
            return False

        _head = self.__bucket[_index]

        while _head:
            #! check
            if _head.nkey.objecthash() == _key.objecthash(): return True

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
    
    def keys(self):
        _key = []

        for _cell in self.__bucket:
            #! check
            if  _cell: 
                _head = _cell

                while _head:
                    #! re-insert
                    _key.append(_head.nkey)
                    
                    #! next
                    _head = _head.tail
        #! end
        return _key
    
    def values(self):
        _val = []

        for _cell in self.__bucket:
            #! check
            if  _cell: 
                _head = _cell

                while _head:
                    #! re-insert
                    _val.append(_head.nval)
                    
                    #! next
                    _head = _head.tail
        #! end
        return _val

class aobject(HashMap):
    """ Base class of all atom object.
    """

    def __init__(self):
        super().__init__()
        self.offset = None
        self.gcnext = None

    def objecthash(self):
        _hash = 0
        for _k, _v in zip(self.keys(), self.values()):
            _hash  = (((_hash << 5) - _hash) + (_k.objecthash() + _v.objecthash()))
            _hash |= 0

        return _hash
