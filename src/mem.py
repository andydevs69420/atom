import gc
from agc import agc
from aobjects import aobject


class offset(object):
    """ Object offset for atom. to easily update forwarding address
    """

    def __init__(self, _offset):
        self.offset = _offset


class agc:
    #! run garbage collection every 500 allocation
    ALLOCATION_LIMIT = 500

    CURRENT_ALLOCATION = 0

    @staticmethod
    def markobject(_state, _object):
        #! make root if empty
        _searchqueue = [_object]

        while len(_searchqueue) > 0:

            _reachableN = _searchqueue.pop()

            #! if not marked
            if  _reachableN.markbit == 0:
                _reachableN.markbit = 1

                #! extend searchqueue using object(s) from "_reachableN"
                _searchqueue.extend(_reachableN.all())
        
        #! end mark
    
    @staticmethod
    def markopstack(_state):
        for _each_object in _state.oprnd:
            agc.markobject(_state, _each_object)
    
    @staticmethod
    def markcallstack(_state):
        for _each_frame in _state.stack:
            for _each_forwarding_address in _each_frame.value:
                agc.markobject(_state, atom_object_Get(_state, _each_forwarding_address))

    @staticmethod
    def sweep(_state):
        #! iterate entire memory and delete unmarked object
        for _idx in range(len(_state.memory.memory)):
            _each_object = _state.memory.memory[_idx]

            if  not _each_object: continue

            #! check markbit
            if  _each_object.markbit == 0:
                #! unreachable
                _state.memory.memory[_idx] = None
            
            #! reset markbit
            _each_object.markbit = 0

    @staticmethod
    def compact(_state):
        _freecell:list[int] = []

        #! last cell
        _lastknowncell = 0

        for _idx in range(len(_state.memory.memory)):
            
            if  _state.memory.memory[_idx] == None:
                #! free cell
                _freecell.insert(0, _idx)

                #! next
                continue

            #! data??
            if  len(_freecell) > 0:
                #! move object
                _lastknowncell = _newlocation = _freecell.pop()

                #! copy
                _state.memory.memory[_newlocation] = _state.memory.memory[_idx]

                #! update offset|address
                _state.memory.memory[_newlocation].offset.offset = _newlocation
                _state.memory.memory[_newlocation]

                #! nullify
                _state.memory.memory[_idx] = None

                #! add current address to free cell
                _freecell.insert(0, _idx)
        
        del _state.memory.memory[_lastknowncell:]
        print("MEMVIEW:", _state.memory.memory)

    @staticmethod
    def collect(_state):
        #! mark everything in operand stack
        agc.markopstack(_state)

        #! mark every local for each frame
        agc.markcallstack(_state)

        #! remove unreachable objects
        agc.sweep(_state)

        #! move object(s) to free cell and update forwarding address
        agc.compact(_state)

        #! invoke python gc
        gc.collect()

        #! end collect|continue thread


class mem(object):
    """ Memory for atom (single memory produces slow|unefficient code).
    """

    def __init__(self):
        self.memory = []
    

def atom_object_New(_state, _aobject):
    #! mark
    agc.markobject(_state, _aobject)

    _aobject.offset = offset(len(_state.memory.memory))

    #! collect if limit reached
    if  agc.CURRENT_ALLOCATION >= agc.ALLOCATION_LIMIT:
        agc.collect(_state)

        #! reset count
        agc.CURRENT_ALLOCATION = 0

    #! increment alloc count
    agc.CURRENT_ALLOCATION += 1
    
    #! append
    _state.memory.memory.append(_aobject)


def atom_object_Get(_state, _offset):
    return _state.memory.memory[_offset.offset]


