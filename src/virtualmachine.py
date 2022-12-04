from aframe import frame
from aobjects import *
from abuiltins.getter import getbuiltin
from mem import *



TOP    = -1
BOTTOM = 00

def push_operand(_cls, _aobject):
    _cls.state.oprnd.generic_push(_aobject)

def popp_operand(_cls):
    return _cls.state.oprnd.popp()



class virtualmachine(object):
    """ Virtual machine for atom.
    """

    def __init__(self, _state):

        #! global state
        self.state = _state


    #! =========== opcode ============

    def iload(self, _bytecode_chunk):
        _int =\
        ainteger(_bytecode_chunk[2])

        atom_object_New(self.state, _int)
    
        #! push to opstack
        push_operand(self, _int)
    
    def fload(self, _bytecode_chunk):
        _flt =\
        afloat(_bytecode_chunk[2])

        atom_object_New(self.state, _flt)
    
        #! push to opstack
        push_operand(self, _flt)

    def sload(self, _bytecode_chunk):
        _str =\
        astring(_bytecode_chunk[2])

        atom_object_New(self.state, _str)
    
        #! push to opstack
        push_operand(self, _str)
    
    def nload(self, _bytecode_chunk):
        _null =\
        ainteger(_bytecode_chunk[2])

        atom_object_New(self.state, _null)
    
        #! push to opstack
        push_operand(self, _null)
    

    def load_funpntr(self, _bytecode_chunk):
        _funpntr =\
        afun(_bytecode_chunk[2])

        atom_object_New(self.state, _funpntr)
    
        #! push to opstack
        push_operand(self, _funpntr)
    
    def load_mod_funpntr(self, _bytecode_chunk):
        _funpntr =\
        anativefun(_bytecode_chunk[2], _bytecode_chunk[3])

        atom_object_New(self.state, _funpntr)
    
        #! push to opstack
        push_operand(self, _funpntr)
    
    def load_global(self, _bytecode_chunk):
        _offset = _bytecode_chunk[3]

        #! retrieve object
        _object =\
        atom_object_Get(self.state, self.state.stack.bott().get(_offset))

        #! push to opstack
        push_operand(self, _object)
    
    def load_local(self, _bytecode_chunk):
        _offset = _bytecode_chunk[3]

        #! retrieve object
        _object =\
        atom_object_Get(self.state, self.state.stack.peek().get(_offset))

        #! push to opstack
        push_operand(self, _object)
    

    def build_array(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        #! temp
        _arr = []

        #! appended inorder
        for _r in range(_popsize):_arr.append(popp_operand(self))

        _new_arr = aarray(*_arr[::-1])

        atom_object_New(self.state, _new_arr)

        #! push to opstack
        push_operand(self, _new_arr)
    
    def array_pushall(self, _bytecode_chunk):
        #! pop extenssion
        _extension = popp_operand(self)

        #! pop array
        _array = popp_operand(self)
        _array.pushall(_extension)

        #! pushback
        push_operand(self, _array)
    
    def array_push(self, _bytecode_chunk):
        #! pop element
        _newelem = popp_operand(self)

        #! pop array
        _array = popp_operand(self)
        _array.push(_newelem)

        #! pushback
        push_operand(self, _array)

    def call_function(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        #! params
        _tmp = []

        #! appended inorder
        for _r in range(_popsize): _tmp.append(popp_operand(self))

        _funpntr =\
        popp_operand(self)


        #! pushback
        for _r in range(_popsize): push_operand(self, _tmp.pop())

        #! push program frame
        self.state.stack.push(frame(self.state.codes[_funpntr.funpntr]))

        for i in self.state.codes[_funpntr.funpntr]:
            print(i)
    
    def call_native(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        #! params
        _param = []

        #! appended inorder
        for _r in range(_popsize): _param.append(popp_operand(self))

        _funpntr =\
        popp_operand(self)

        _fun = getbuiltin(_funpntr.modpntr).get(_funpntr.funpntr)

        _return = _fun(self.state, *_param)

        #! store
        atom_object_New(self.state, _return)

        #! push to opstack
        push_operand(self, _return)
    
    def return_control(self, _bytecode_chunk):
        self.state.stack.popp()
    
    #! ========= pow =========

    def intpow(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(_lhs.raw ** _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def fltpow(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw ** _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)

    #! ========= mul =========

    def intmul(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(_lhs.raw * _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def fltmul(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw * _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ====== quotient =======

    def quotient(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw / _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ====== remainder =======
    
    def intrem(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(_lhs.raw % _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def fltrem(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw % _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ========= add =========
    
    def intadd(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(_lhs.raw + _rhs.raw)
        
        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def fltadd(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw + _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def concat(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        astring(_lhs.raw + _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ========= sub =========
    
    def intsub(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)

        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(_lhs.raw - _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def fltsub(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        afloat(_lhs.raw - _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)

    def store_global(self, _bytecode_chunk):
        _offset = _bytecode_chunk[3]

        #! pop value
        _vvalue =\
        popp_operand(self)

        #! push to value stack
        self.state.stack.bott().set(_offset, _vvalue.offset)
    
    
    def store_local(self, _bytecode_chunk):
        _offset = _bytecode_chunk[3]

        #! pop value
        _vvalue =\
        popp_operand(self)

        #! push to value stack
        self.state.stack.peek().set(_offset, _vvalue.offset)
        
    
    def store_fast(self, _bytecode_chunk):
        _offset = _bytecode_chunk[3]

        #! pop value
        _vvalue =\
        popp_operand(self)

        #! push to value stack
        self.state.stack.peek().set(_offset, _vvalue.offset)
        

    def pop_top(self, _bytecode_chunk):
        popp_operand(self)
    
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
