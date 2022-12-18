from aframe import frame
from aobjects import *
from abuiltins.getter import getbuiltin
from mem import *
from error import (error_category, error)
from atyping import integer_t, float_t


TOP    = -1
BOTTOM = 00

def push_operand(_cls, _aobject):
    _cls.state.oprnd.generic_push(_aobject)

def popp_operand(_cls):
    return _cls.state.oprnd.popp()

def peek_operand(_cls):
    return _cls.state.oprnd.peek()

def check_int(_cls, _int):
    if  integer_t.auto(_int).iserror():
        error.raise_fromstack(error_category.RuntimeError, "integer underflowed or overflowed.", _cls.state.stacktrace)
    
    #! end
    return _int

def check_flt(_cls, _flt):
    if  float_t.auto(_flt).iserror():
        error.raise_fromstack(error_category.RuntimeError, "float underflowed or overflowed.", _cls.state.stacktrace)
    
    #! end
    return _flt

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
    
    def bload(self, _bytecode_chunk):
        _str =\
        aboolean(_bytecode_chunk[2])

        atom_object_New(self.state, _str)
    
        #! push to opstack
        push_operand(self, _str)
    
    def nload(self, _bytecode_chunk):
        _null =\
        anull()

        atom_object_New(self.state, _null)
    
        #! push to opstack
        push_operand(self, _null)

    def load_funpntr(self, _bytecode_chunk):
        _funpntr =\
        afun(_bytecode_chunk[2], _bytecode_chunk[3])

        atom_object_New(self.state, _funpntr)
    
        #! push to opstack
        push_operand(self, _funpntr)
    

    def load_mod_funpntr(self, _bytecode_chunk):
        _funpntr =\
        anativefun(_bytecode_chunk[2], _bytecode_chunk[3])

        atom_object_New(self.state, _funpntr)
    
        #! push to opstack
        push_operand(self, _funpntr)
    
    def load_typepntr(self, _bytecode_chunk):
        _typepntr =\
        atype(_bytecode_chunk[2])

        atom_object_New(self.state, _typepntr)
    
        #! push to opstack
        push_operand(self, _typepntr)

    
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
    
    #! ===== array object =====

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
        #! pop extension
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
    
    def array_get(self, _bytecode_chunk):
        #! pop array
        _array = popp_operand(self)

        #! pop element
        _element = popp_operand(self)

        #! FIXME: CATCH array out of bounds

        push_operand(self, _array.subscript(_element))
    
    def array_set(self, _bytecode_chunk):
        #! pop array
        _array = popp_operand(self)

        #! pop element
        _element = popp_operand(self)

        #! new value
        _value = popp_operand(self)

        #! FIXME: CATCH array out of bounds

        #! set index
        _array.set_index(_element, _value)


    #! ====== map object ======

    def build_map(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        _new_map = amap()

        #! alloc
        atom_object_New(self.state, _new_map)

        for _r in range(_popsize):
            _k = popp_operand(self)
            _v = popp_operand(self)
            _new_map.put(_k, _v)
        
        push_operand(self, _new_map)
    
    def map_put(self, _bytecode_chunk):
        #! pop element
        _newelemk = popp_operand(self)
        _newelemv = popp_operand(self)

        #! pop map
        _map = popp_operand(self)
        _map.put(_newelemk, _newelemv)

        #! pushback
        push_operand(self, _map)

    def map_merge(self, _bytecode_chunk):
        #! pop extension
        _extension = popp_operand(self)

        #! pop map
        _map = popp_operand(self)
        _map.merge(_extension)

        #! pushback
        push_operand(self, _map)
    
    def map_get(self, _bytecode_chunk):
        #! pop map
        _map = popp_operand(self)

        #! pop element
        _key = popp_operand(self)

        #! FIXME: CATCH key error

        push_operand(self, _map.get(_key))
    
    def map_set(self, _bytecode_chunk):
        #! pop map
        _map = popp_operand(self)

        _map.put(popp_operand(self), popp_operand(self))
    
    #! = struct / object make =

    def make_aobject(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[3]

        _object = ainstance(_bytecode_chunk[2])

        #! alloc
        atom_object_New(self.state, _object)

        for _r in range(_popsize):
            _k = popp_operand(self)
            _v = popp_operand(self)
            _object.put(_k, _v)

        #! push to operand
        push_operand(self, _object)
    
    def get_attribute(self, _bytecode_chunk):
        #! pop attrib
        _attrib = popp_operand(self)

        #! pop obect
        _object = popp_operand(self)
        
        #! push
        push_operand(self, _object.get(_attrib))
    
    def set_attribute(self, _bytecode_chunk):
        #! pop attrib
        _attrib = popp_operand(self)

        #! pop obect
        _object = popp_operand(self)
        _object.put(_attrib, popp_operand(self))

    #! ===== enum object ======

    def build_enum(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[3]

        _new_enum = aenum(_bytecode_chunk[2])
        
        #! alloc
        atom_object_New(self.state, _new_enum)

        for _r in range(_popsize):
            _k = popp_operand(self)
            _v = popp_operand(self)
            _new_enum.put(_k, _v)

        #! push operand
        push_operand(self, _new_enum)
    
    def get_enum(self, _bytecode_chunk):
        #! pop attrib
        _attrib = popp_operand(self)

        #! pop enum
        _enum = popp_operand(self)
        
        #! push
        push_operand(self, _enum.get(_attrib))
    
    #! ======== call =========
    
    def call_native(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        #! append
        self.state.stacktrace.append(self.state.calls[_bytecode_chunk[3]])

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

        #! pop native stacktrace
        self.state.stacktrace.pop()

    def call_function(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]
        
        #! append
        self.state.stacktrace.append(self.state.calls[_bytecode_chunk[3]])

        #! params
        _tmp = []

        #! appended inorder
        for _r in range(_popsize): _tmp.append(popp_operand(self))

        _funpntr =\
        popp_operand(self)
       
        #! pushback
        for _r in range(_popsize): push_operand(self, _tmp.pop())

        #! push program frame
        self.state.stack.push(frame(self.state.codes[_funpntr.modpntr][_funpntr.funpntr]))

        for _i in self.state.codes[_funpntr.modpntr][_funpntr.funpntr]:
            print(_i)
        
    def call_type(self, _bytecode_chunk):
        _popsize = _bytecode_chunk[2]

        #! params
        _tmp = []

        #! appended inorder
        for _r in range(_popsize): _tmp.append(popp_operand(self))

        _typepntr =\
        popp_operand(self)

        #! pushback
        for _r in range(_popsize): push_operand(self, _tmp.pop())

        #! push program frame
        self.state.stack.push(frame(self.state.codes[_typepntr.typepntr]))

    def return_control(self, _bytecode_chunk):
        self.state.stack.popp()

        if  len(self.state.stacktrace) != 0:
            #! pop user defined
            self.state.stacktrace.pop()
    
    #! ======= unary =========

    def bit_not(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        
        #! check
        _new = ainteger(check_int(self, ~_obj.raw))

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)

    def log_not(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        _new = aboolean(not _obj.raw)

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)
    
    def intpos(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        _new = ainteger(check_int(self, + _obj.raw))

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)

    def intneg(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        _new = ainteger(check_int(self, - _obj.raw))

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)
    
    def fltpos(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        _new = afloat(check_flt(self, + _obj.raw))

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)

    def fltneg(self, _bytecode_chunk):
        _obj =\
        popp_operand(self)

        _new = afloat(check_flt(self, - _obj.raw))

        #! alloc
        atom_object_New(self.state, _new)

        #! push
        push_operand(self, _new)

    #! ========= pow =========

    def intpow(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw ** _rhs.raw))

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
        afloat(check_flt(self, _lhs.raw ** _rhs.raw))

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
        ainteger(check_int(self, _lhs.raw * _rhs.raw))

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
        afloat(check_flt(self, _lhs.raw * _rhs.raw))

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
        afloat(check_flt(self, _lhs.raw / _rhs.raw))

        #! FIXME: zero division error

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
        ainteger(check_int(self, _lhs.raw % _rhs.raw))

        #! FIXME: zero division error

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
        afloat(check_flt(self, _lhs.raw % _rhs.raw))

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
        ainteger(check_int(self, _lhs.raw + _rhs.raw))
        
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
        afloat(check_flt(self, _lhs.raw + _rhs.raw))

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
        ainteger(check_int(self, _lhs.raw - _rhs.raw))

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
        afloat(check_flt(self, _lhs.raw - _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ======== shift ========

    def lshift(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw << _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def rshift(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw >> _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ====== relational ======

    def comlt(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw < _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def comlte(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw <= _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def comgt(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw > _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def comgte(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw >= _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ======= equality =======

    def equal_i(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw == _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def equal_f(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw == _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)

    def equal_s(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw == _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def equal_b(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw == _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def equal_n(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.raw == _rhs.raw)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)

    def addressof(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        aboolean(_lhs.offset.offset == _rhs.offset.offset)

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    #! ======== bitwise =======

    def bitand(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw & _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def bitxor(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw ^ _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)
    
    def bitor(self, _bytecode_chunk):
        _lhs =\
        popp_operand(self)
        
        _rhs =\
        popp_operand(self)

        _new =\
        ainteger(check_int(self, _lhs.raw | _rhs.raw))

        #! store
        atom_object_New(self.state, _new)

        #! push to opstack
        push_operand(self, _new)

    def dup_top(self, _bytecode_chunk):
        #! cuplicate top
        push_operand(self, peek_operand(self))

    def rot1(self, _bytecode_chunk):
        _top = popp_operand(self)
        _bot = popp_operand(self)

        push_operand(self, _top)
        push_operand(self, _bot)
    
    def rot3(self, _bytecode_chunk):
        _1st = popp_operand(self)
        _2nd = popp_operand(self)
        _3rd = popp_operand(self)

        push_operand(self, _3rd)
        push_operand(self, _2nd)
        push_operand(self, _1st)

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
    
    #! ========= jumps ========

    def pop_jump_if_false(self, _bytecode_chunk):
        #! pop first before check
        if  not popp_operand(self).raw:
            self.state.stack.peek().ipointer = (_bytecode_chunk[2] // 2) - 1
        
    def pop_jump_if_true(self, _bytecode_chunk):
        #! pop first before check
        if  popp_operand(self).raw:
            self.state.stack.peek().ipointer = (_bytecode_chunk[2] // 2) - 1
        
    def jump_if_false(self, _bytecode_chunk):
        #! peek first before check
        if  not peek_operand(self).raw:
            self.state.stack.peek().ipointer = (_bytecode_chunk[2] // 2) - 1
    
    def jump_if_true(self, _bytecode_chunk):
        #! peek first before check
        if  peek_operand(self).raw:
            self.state.stack.peek().ipointer = (_bytecode_chunk[2] // 2) - 1
        
    def jump_to(self, _bytecode_chunk):
        self.state.stack.peek().ipointer = (_bytecode_chunk[2] // 2) - 1
    
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

        # try:
        while not self.state.stack.isempty():
            _top = self.state.stack.peek()

            #! visit opcode
            self.visit(_top.instructions[_top.ipointer])

            #! next
            _top.ipointer += 1

        # except:
        #     error.raise_untracked(error_category.RuntimeError, "internal virtualmachine error...")

        #! program ok!!!
        print("Program finished with exit code %s..." % popp_operand(self).__repr__())

        #! debug!!
        assert self.state.oprnd.isempty(), "not all operand is popped out!!"

        #! end
        return 0x00
