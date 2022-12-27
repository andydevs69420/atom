

"""
    #TODO: replace values with integers.
"""

#! const
iload  = "iload"
fload  = "fload"

sload  = "sload"
string_get = "string_get"

bload  = "bload"
nload  = "nload"

load_funpntr = "load_funpntr"
load_mod_funpntr = "load_mod_funpntr"
load_typepntr = "load_typepntr"

load_global = "load_global"
load_local  = "load_local"

build_array = "build_array"
array_push = "array_push"
array_pushall = "array_pushall"
array_pop = "array_pop"
array_peek = "array_peek"
array_size = "array_size"
array_get = "array_get"
array_set = "array_set"


build_map = "build_map"
map_put   = "map_put"
map_merge = "map_merge"
map_keys = "map_keys"
map_values = "map_values"
map_get = "map_get"
map_set = "map_set"


build_enum = "build_enum"
get_enum   = "get_enum"


build_module = "build_module"

make_aobject = "make_aobject"
get_attribute = "get_attribute"
set_attribute = "set_attribute"

#! call function|type
call_function = "call_function"
call_native = "call_native"
call_type = "call_type"

#! end function
return_control = "return_control"

#! unary
bit_not = "bit_not"
log_not = "log_not"
intpos  = "intpos"
fltpos  = "fltpos"
intneg  = "intneg"
fltneg  = "fltneg"

#! exponent
intpow = "intpow"
fltpow = "fltpow"

#! multiply
intmul = "intmul"
fltmul = "fltmul"

#! divide
quotient  = "quotient"

intrem = "intrem"
fltrem = "fltrem"

#! plus
intadd = "intadd"
fltadd = "fltadd"
concat = "concat"

#! minus
intsub = "intsub"
fltsub = "fltsub"

#! shift
lshift = "lshift"
rshift = "rshift"

#! compare
comlt  = "comlt"
comlte = "comlte"
comgt  = "comgt"
comgte = "comgte"

#! equal
equal_i = "equal_i"
equal_f = "equal_f"
equal_s = "equal_s"
equal_b = "equal_b"
equal_n = "equal_n"
addressof = "addressof"

#! bitwise logic
bitand = "bitand"
bitxor = "bitxor"
bitor  = "bitor"

#! var setter
store_global = "store_global"
store_local  = "store_local"
store_fast   = "store_fast"



#! object manipulation
dup_top = "dup_top"
rot2 = "rot2"
rot3 = "rot3"

#! stack item removal
pop_top = "pop_top"

#! jumps
pop_jump_if_false = "pop_jump_if_false"
pop_jump_if_true = "pop_jump_if_true"

jump_if_false = "jump_if_false"
jump_if_true = "jump_if_true"
jump_to = "jump_to"


#! try
setup_try = "setup_try"
unsetup_try = "unsetup_try"


assert_error = "assert_error"