""" LinkedList of HashTable
"""


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

    def __init__(self):
        self.head = None
        self.tail = None
        #! ===============
        self.__htsize = 16
        self.__elsize = 0
        self.__bucket = [None for _r in range(self.__htsize)]

    
    def put(self, _key, _value):
        assert _key and _value, "invalid data!!!"
        
        _index = self.hash(_key) % self.__htsize
        
        if  self.__bucket[_index]:
            #! collision
            self.__bucket[_index].append(_key, _value)

            #! end
            return

        self.__bucket[_index] = LinkedList(_key, _value)
        self.__elsize += 1

        if  (float(self.__elsize) / self.__htsize) > 0.75:
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



class SymbolTable(HashTable):
    """ SymbolTable base.

        Bottom to up.
    """

    def __init__(self):
        super().__init__()

    def insert_variable(self, _key, _value):
        self.getlast().put(_key, _value)
    
    def lookup_global(self, _key):
        _last = self.getlast()

        while _last:
            if _last.haskey(_key): return _last.get(_key)

            _last = _last.head
        
        return False
    
    def lookup_local(self, _key):
        if  self.getlast().haskey(_key):
            return False

        return self.getlast().haskey(_key)
    
    def newscope(self):
        self.newtail()
    
    def endscope(self):
        _end = self.getlast()
        _end.head.tail = None


if  __name__ == "__main__":
    _st = SymbolTable()
    _st.insert_variable("Andy", 2)
    _st.insert_variable("Marielle", 10)
    _st.insert_variable("Orpheus", "OPAW")
    print(_st.lookup_global("Andy"))
    print(_st.lookup_global("Marielle"))
    

    _st.newscope()

    _st.insert_variable("Orpheus", 2000)
    print(_st.lookup_global("Andy"))
    print(_st.lookup_global("Marielle"))
    print(_st.lookup_global("Orpheus"))
    _st.insert_variable("amanda", 2)

    _st.endscope()

    if  not _st.lookup_local("amanda"):
        print("Error amanda not found!")

    print(_st.lookup_global("Orpheus"))