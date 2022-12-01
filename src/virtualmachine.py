from aframe import frame
from aobjects import *
from mem import *


def push_operand(_cls, _aobject):
    _cls.state.oprnd.generic_push(_aobject)

def popp_operand(_cls):
    return _cls.state.oprnd.popp()



def push_value(_cls, _offset, _vvalue):
    if  (_offset + 1) > len(_cls.state.value):
        #! make slot
        _cls.state.value.generic_push(_vvalue)
    
    else:
        #! set slot
        _cls.state.value[_offset] = _vvalue

def popp_value(_cls):
    return _cls.state.value.popp()


class virtualmachine(object):
    """ Virtual machine for atom.
    """

    def __init__(self, _state):

        #! global state
        self.state = _state


    #! =========== opcode ============

    def iload(self, _bytecode_chunk):
        _int = ainteger(_bytecode_chunk[2])

        atom_object_New(self.state, _int)
    
        #! push to opstack
        push_operand(self, _int)
    

    def store_global(self, _bytecode_chunk):
        _offset = _bytecode_chunk[2]

        #! pop value
        _vvalue = popp_operand(self)

        #! push to value stack
        push_value(self, _offset, _vvalue)

    
    #! =========== visitor ===========
    
    def visit(self, _bytecode_chunk):
        _visitor = getattr(self, _bytecode_chunk[1], self.error)

        #! end
        return _visitor(_bytecode_chunk)
    
    def error(self, _bytecode_chunk):
        raise NotImplementedError("not implemented opcode %s." % _bytecode_chunk[1])

    def run(self):
        if  "program" not in self.state.codes.keys():
            return 0x00
        
        #! push program frame
        self.state.stack.push(frame(self.state.codes["program"]))

        while not self.state.stack.isempty():
            _top = self.state.stack.peek()

            #! visit opcode
            self.visit(_top.instructions[_top.ipointer])

            #! next
            _top.ipointer += 1

            if  _top.ipointer >= len(_top.instructions):
                break

        #! end
        return 0x00
