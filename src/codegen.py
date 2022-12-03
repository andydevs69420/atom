

from stack import stack
from readf import (file_isfile, read_file)
from aparser import parser
from symboltable2 import SymbolTable
from atyping import *
from error import (error_category, error)
from aopcode import *
from aast import ast_type

TARGET = ...
MAX_NESTING_LEVEL = 255



def push_ttable(_cls, _type):
    #! push type
    _cls.tstack.generic_push(_type)


def get_byteoff(_cls):
    return len(_cls.bcodes) * 2

def emit_opcode(_cls, _opcode, *_args):
    _cls.bcodes.append([get_byteoff(_cls), _opcode, *_args])
    return _cls.bcodes[-1]


class generator(object):
    """ Base code generator for atom.
    """

    def __init__(self):
        self.offset = 0
        self.symtbl = SymbolTable()
        self.tstack = stack(tag_t)
        self.bcodes = []
        self.nstlvl = 0
        
        self.currentfunctiontype = None

    #! =========== VISITOR ===========
    
    def visit(self, _node):
        #! make visitor
        _visitor = getattr(self, "ast_" + _node.type.name.lower(), self.error)

        #! end
        return _visitor(_node)
    
    def error(self, _node):
        raise AttributeError("unimplemented node no# %d a.k.a %s!!!" % (_node.type.value, _node.type.name))
    
    #! ========= DATA TYPING ==========

    def ast_any_t(self, _node):
        #! push int type
        push_ttable(self, any_t())

    def ast_int_t(self, _node):
        #! push int type
        push_ttable(self, integer_t())
    
    def ast_float_t(self, _node):
        #! push int type
        push_ttable(self, float_t())
    
    def ast_str_t(self, _node):
        #! push int type
        push_ttable(self, string_t())
    
    def ast_bool_t(self, _node):
        #! push int type
        push_ttable(self, boolean_t())

    def ast_void_t(self, _node):
        #! push int type
        push_ttable(self, null_t())

    def ast_array_t(self, _node):
        #! internal
        self.visit(_node.get(1))

        _internal = self.tstack.popp()

        #! push int type
        push_ttable(self, array_t(_internal))
    
    def ast_fn_t(self, _node):
        #! return
        self.visit(_node.get(1))

        _return = self.tstack.popp()

        #! push int type
        push_ttable(self, fn_t(_return))
    
    def ast_map_t(self, _node):
        #! val type
        self.visit(_node.get(2))

        #! key type
        self.visit(_node.get(1))

        _key = self.tstack.popp()
        _val = self.tstack.popp()

        #! push int type
        push_ttable(self, map_t(_key, _val))

    #! =========== CONST VAL ==========

    def ast_int(self, _node):
        #! max is int 64
        I64 = int(_node.get(0))

        #! type
        push_ttable(self, integer_t())

        #! opcode
        emit_opcode(self, iload, I64)
    

    def ast_float(self, _node):
        #! max is float 64
        F64 = float(_node.get(0))

        #! type
        push_ttable(self, float_t())

        #! opcode
        emit_opcode(self, fload, F64)
    

    def ast_str(self, _node):
        STR = str(_node.get(0))

        #! type
        push_ttable(self, string_t())

        #! opcode
        emit_opcode(self, sload, STR)


    def ast_bool(self, _node):
        BOOL = _node.get(0) == "true"

        #! type
        push_ttable(self, boolean_t())

        #! opcode
        emit_opcode(self, bload, BOOL)


    def ast_null(self, _node):
        #! type
        push_ttable(self, null_t())

        #! opcode
        emit_opcode(self, nload, None)
    
    def ast_ref(self, _node):
        _var = _node.get(0)

        if  not self.symtbl.contains(_var):
            error.raise_tracked(error_category.CompileError, "var \"%s\" is not defined." % _var, _node.site)

        _name = self.symtbl.lookup(_var)

        #! type
        push_ttable(self, _name.get_datatype())

        #! check
        _opcode = load_global if _name.is_global() else load_local

        #! opcode
        emit_opcode(self, _opcode, _var, _name.get_offset())
    

    def ast_array(self, _node):
        _arrtype = None
        _element = _node.get(0)
        _arrsize = 0
        _hasunpack = False

        while _arrsize < len(_element):
            #! element
            _elem = _element[_arrsize]
            _current = ...

            if  _elem.type == ast_type.UNARY_UNPACK:
                #! build array before unpack
                #! opcode
                emit_opcode(self, build_array, _arrsize)

                #! =========================
                _hasunpack = True
                
                #! visit each element
                self.visit(_elem)

                #! virtual current
                _current = self.tstack.peek()

                #! current
                _arrtype = self.tstack.popp() if  not _arrtype else _arrtype

                #! internal
                _arrtype = _arrtype.elementtype
                
            else:
                self.visit(_elem)

                #! virtual current
                _current = self.tstack.peek()

                #! current
                _arrtype = self.tstack.popp() if  not _arrtype else _arrtype
            
                if  _hasunpack:
                    #! opcode
                    emit_opcode(self, array_push)
            
            _arrsize += 1

            if  not _arrtype.matches(_current):
                #! array of any
                push_ttable(self, any_t())

                #! set as array element type
                _arrtype = self.tstack.popp()

        
        if  not _hasunpack:
            #! opcode
            emit_opcode(self, build_array, _arrsize)
        
        if  _arrsize <= 0:
            #! array of any
            push_ttable(self, any_t())

            #! set as array element type
            _arrtype = self.tstack.popp()

        #! array type
        push_ttable(self, array_t(_arrtype))
    

    def ast_call(self, _node):
        """ 
             $0         $1
            object  parameters
        """
        print(_node)
    
    def ast_unary_op(self, _node):
        """
             $0    $1
            _op  _rhs
        """
        self.nstlvl += 1
        if  self.nstlvl >= MAX_NESTING_LEVEL:
            error.raise_tracked(error_category.CompileError, "max nesting level for expression reached.", _node.site)

        _op = _node.get(0)
        self.visit(_node.get(1)) # rhs

        _rhs = self.tstack.popp()

        #! default
        _operation = operation.BAD_OP

        if  _op == "~":
            #! op result
            _operation = _rhs.bitnot()

            #! emit int type
            push_ttable(self, integer_t())

            #! opcode
            emit_opcode(self, bit_not)
        
        elif _op == "!":
            #! op result
            _operation = _rhs.lognot()

            #! emit int type
            push_ttable(self, boolean_t())

            #! opcode
            emit_opcode(self, log_not)

        elif _op == "+":
            #! op result
            _operation = _rhs.pos()

            match _operation:
                case operation.INT_OP:
                    #! emit int type
                    push_ttable(self, integer_t())

                    #! opcode
                    emit_opcode(self, intpos)
                
                case operation.FLOAT_OP:
                    #! emit int type
                    push_ttable(self, float_t())

                    #! opcode
                    emit_opcode(self, fltpos)

        
        elif _op == "-":
            #! op result
            _operation = _rhs.neg()

            #! opcode
            match _operation:
                case operation.INT_OP:
                    #! emit int type
                    push_ttable(self, integer_t())

                    #! opcode
                    emit_opcode(self, intneg)
                
                case operation.FLOAT_OP:
                    #! emit int type
                    push_ttable(self, float_t())

                    #! opcode
                    emit_opcode(self, fltneg)

        if  _operation == operation.BAD_OP:
            error.raise_tracked(error_category.CompileError, "invalid operation %s %s." % (_op, _rhs.repr()), _node.site)

        self.nstlvl -= 1
        #! end
    
    def ast_unary_unpack(self, _node):
        """
             $0    $1
            _op  _rhs
        """
        self.nstlvl += 1
        if  self.nstlvl >= MAX_NESTING_LEVEL:
            error.raise_tracked(error_category.CompileError, "max nesting level for expression reached.", _node.site)

        _op = _node.get(0)
        self.visit(_node.get(1)) # rhs

        _rhs = self.tstack.peek()

        #! default
        _operation = operation.BAD_OP

        if  _op == "*":
            #! op result
            _operation = _rhs.unpack()

            #! opcode
            emit_opcode(self, array_pushall)
        
        if  _operation == operation.BAD_OP:
            error.raise_tracked(error_category.CompileError, "cannot unpack %s." % _rhs.repr(), _node.site)


    def ast_binary_op(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        self.nstlvl += 1
        if  self.nstlvl >= MAX_NESTING_LEVEL:
            error.raise_tracked(error_category.CompileError, "max nesting level for expression reached.", _node.site)

        _op = _node.get(1)
        self.visit(_node.get(2)) # rhs
        self.visit(_node.get(0)) # lhs

        _lhs = self.tstack.popp()
        _rhs = self.tstack.popp()

        #! default
        _operation = operation.BAD_OP

        if  _op == "^^":
            #! op result
            _operation = _lhs.pow(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, integer_t())

                    emit_opcode(self, intpow)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, float_t())

                    emit_opcode(self, fltpow)

        elif _op == "*":
            #! op result
            _operation = _lhs.mul(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, integer_t())

                    emit_opcode(self, intmul)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, float_t())

                    emit_opcode(self, fltmul)

        elif _op == "/":
            #! op result
            _operation = _lhs.div(_rhs)

            #! emit float type
            push_ttable(self, float_t())

            #! opcode
            emit_opcode(self, quotient)
            
        
        elif _op == "%":
            #! op result
            _operation = _lhs.mod(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, integer_t())

                    emit_opcode(self, intrem)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self,float_t())

                    emit_opcode(self, fltrem)

        elif _op == "+":
            #! op result
            _operation = _lhs.add(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, integer_t())

                    emit_opcode(self, intadd)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, float_t())

                    emit_opcode(self, fltadd)
                
                case operation.STR_OP:
                    #! emit str type
                    push_ttable(self, string_t())

                    emit_opcode(self, concat)
        
        elif _op == "-":
            #! op result
            _operation = _lhs.sub(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, integer_t())

                    emit_opcode(self, intsub)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, float_t())
                    
                    emit_opcode(self, fltsub)
        
        elif _op == "<<" or _op == ">>":
            #! op result
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, integer_t())

            #! opcode
            if  _op == "<<":
                emit_opcode(self, lshift)

            else:
                emit_opcode(self, rshift)
        
        elif _op == "<"  or \
             _op == "<=" or \
             _op == ">"  or \
             _op == ">=":
            #! op result
            _operation = _lhs.relational(_rhs)

            #! emit bool type
            push_ttable(self, boolean_t())

            #! opcode
            if  _op == "<":
                emit_opcode(self, comlt )

            elif _op == "<=":
                emit_opcode(self, comlte)
            
            elif _op == ">":
                emit_opcode(self, comgt )

            elif _op == ">=":
                emit_opcode(self, comgte)
        
        elif _op == "!=" or _op == "==":
            #! op result
            _operation = _lhs.equality(_rhs)

            #! emit bool type
            push_ttable(self, boolean_t())

            #! opcode
            if  _lhs.isint() and _rhs.isint():
                emit_opcode(self, equal_i)

            elif _lhs.isfloat() or _rhs.isfloat():
                emit_opcode(self, equal_f)
            
            elif _lhs.isstring() and _rhs.isstring():
                emit_opcode(self, equal_s)
            
            elif _lhs.isboolean() and _rhs.isboolean():
                emit_opcode(self, equal_b)
            
            elif _lhs.isnull() and _rhs.isnull():
                emit_opcode(self, equal_n)
            
            else:
                emit_opcode(self, addressof)
            
            if  _op == "!=":
                #! negate
                emit_opcode(self, log_not)
        
        elif _op == "&" or \
             _op == "^" or \
             _op == "|":
            
            #! op result
            _operation = _lhs.bitwise(_rhs)

            #! emit int type
            push_ttable(self, integer_t())

            #! opcode
            if  _op == "&":
                emit_opcode(self, bitand)

            elif _op == "^":
                emit_opcode(self, bitxor)
            
            elif _op == "|":
                emit_opcode(self, bitor)


        if  _operation == operation.BAD_OP:
            error.raise_tracked(error_category.CompileError, "invalid operation %s %s %s." % (_lhs.repr(), _op, _rhs.repr()), _node.site)

        self.nstlvl -= 1
        #! end

    def ast_shortc_op(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        self.nstlvl += 1
        if  self.nstlvl >= MAX_NESTING_LEVEL:
            error.raise_tracked(error_category.CompileError, "max nesting level for expression reached.", _node.site)

        _target = ...

        #! lhs
        self.visit(_node.get(0))

        #! jump to last control if false
        if  _node.get(1) == "&&":
            _target =\
            emit_opcode(self, jump_if_false, TARGET)
        else:
            _target =\
            emit_opcode(self, jump_if_true, TARGET)

        #! pop lhs
        emit_opcode(self, pop_top)

        #! rhs
        self.visit(_node.get(2))

        #! jump here
        _target[2] = get_byteoff(self)

        #! rhs
        self.tstack.popp() 
        #! lhs
        self.tstack.popp()

        #! emit as any
        push_ttable(self, any_t())

        self.nstlvl -= 1
        #! end

    #! ========== compound statement ==========
    def ast_function(self, _node):
        _old_offset = self.offset
        _old_bcodes = self.bcodes

        self.offset = 0
        self.bcodes = []

        #! =======================
        _parameters = []

        #! new func scope
        self.symtbl.newscope()

        #! visit returntype
        self.visit(_node.get(0))

        #! set current function
        self.currentfunctiontype =\
        self.tstack.popp()

        #! check if function name is already defined.
        if  self.symtbl.contains(_node.get(1)):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(1), _node.site)

        #! compile parameters
        for _each_param in _node.get(2):

            #! visit type
            self.visit(_each_param[1])

            #! param dtype
            _vtype = self.tstack.popp()

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

            #! opcode
            emit_opcode(self, store_fast, _each_param[0], self.offset)

            #! register
            self.symtbl.insert_var(_each_param[0], self.offset, _vtype, True, False)

            self.offset += 1
            #! end

        #! compile body
        for _each_child in _node.get(3):

            #! visit child
            self.visit(_each_child)
        
        #! unset current function
        self.currentfunctiontype =\
        None

        #! end func scope
        self.symtbl.endscope()

        #! register
        self.symtbl.insert_fun(_node.get(1), self.offset, fn_t(self.currentfunctiontype), self.currentfunctiontype, len(_parameters), tuple(_parameters))

        #! store code
        self.state.codes[_node.get(1)] = self.bcodes

        #! restore
        self.offset = _old_offset
        self.bcodes = _old_bcodes


    #! =========== simple statement ===========

    def ast_var_stmnt(self, _node):
        """ Global variable declairation.
        """
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, null_t())

                #! push null
                emit_opcode(self, nload, None)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.contains(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            #! opcode
            emit_opcode(self, store_global, _variable[0], self.offset)

            #! register
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, True, False)

            self.offset += 1
            #! end

    def ast_let_stmnt(self, _node):
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, null_t())

                #! push null
                emit_opcode(self, nload, None)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.haslocal(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            #! opcode
            emit_opcode(self, store_local, _variable[0], self.offset)

            #! register
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, False, False)

            self.offset += 1
            #! end

    def ast_const_stmnt(self, _node):
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, null_t())

                #! push null
                emit_opcode(self, nload, None)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.haslocal(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            _is_global = self.symtbl.isglobal()

            #! check
            _opcode = store_global if _is_global else store_local

            #! opcode
            emit_opcode(self, _opcode, _variable[0], self.offset)

            #! register
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, _is_global, True)

            self.offset += 1
            #! end

    def ast_expr_stmnt(self, _node):
        #! statement
        self.visit(_node.get(0))

        #! opcode
        emit_opcode(self, pop_top)

    def ast_source(self, _node):
        for _each_node in _node.get(0):
            self.visit(_each_node)

class codegen(generator):
    """ Analyzer and byte-code like generator for atom.

        Code block generator.
    """

    def __init__(self, _state):
        super().__init__()
        #! init prop
        self.state   = _state
        self.gparser = parser(self.state)

    #! ========== simple ============
    
    def ast_import(self, _node):
        for _each_import in _node.get(0):

            #! put extra
            _fpath = _each_import + ".as"
            
            #! check file
            if  not file_isfile(self.state, _fpath):
                error.raise_tracked(error_category.CompileError, "file not found or invalid file \"%s\"." % _each_import, _node.site)

            #! read file first
            read_file(self.state, _fpath)

            #! parse
            _parse = parser(self.state)
            
            for _each_node in _parse.raw_parse():
                #! visit each node
                self.visit(_each_node)
        #! end
    
    def generate(self):
        #! compile each child node
        self.visit(self.gparser.parse())

        for x in self.bcodes:
            print(x)

        #! set program code
        self.state.codes["program"] = self.bcodes

        #! end
        return self.bcodes