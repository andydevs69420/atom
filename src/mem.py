
from agc import agc



class mem(object):
    """ Memory for atom.
    """

    def __init__(self):
        self.new = []
        self.old = []
        self.permanent = []
    



def atom_object_New(_state, _aobject):
    #! mark
    agc.mark_object(_state, _aobject)

    #! append
    _state.memory.new.append(_aobject)

