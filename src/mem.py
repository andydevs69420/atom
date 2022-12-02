
from agc import agc
from aobjects import aobject


class offset(object):
    """ Object offset for atom. to easily update forwarding address
    """

    def __init__(self, _offset):
        self.offset = _offset



class agc:

    @staticmethod
    def markroot(_state):
        if  not _state.gcroot:
            return
        
        _state.gcroot.markbit = 1

    @staticmethod
    def markobject(_state, _object):
        #! make root if empty
        if  _state.gcroot == None:
            _object.markbit = 1
            _state .gcroot  = _object
            
            #! end
            return

        _object.markbit = 1
        _object.gcnext  = _state.gcroot
        _state .gcroot  = _object
    
    @staticmethod
    def markvalue(_state):
        _state.gcroot = 2
    
    @staticmethod
    def markopstack(_state):
        _state.gcroot = 2



class mem(object):
    """ Memory for atom.
    """

    def __init__(self):
        self.memory = []
    



def atom_object_New(_state, _aobject):
    #! mark
    agc.markobject(_state, _aobject)

    _aobject.offset = offset(len(_state.memory.memory))

    #! append
    _state.memory.memory.append(_aobject)


def atom_object_Get(_state, _offset):
    return _state.memory.memory[_offset.offset]


