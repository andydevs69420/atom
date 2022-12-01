
from stack import stack
from aframe import frame
from aobjects import aobject



def push_operand(_cls, _aobject):
    _cls.oprnd.generic_push(_aobject)


class virtualmachine(object):
    """ Virtual machine for atom.
    """

    def __init__(self, _state):
        self.state =_state
        self.stack = stack(frame)
        self.oprnd = stack(aobject)

    def run(self):
        ...
