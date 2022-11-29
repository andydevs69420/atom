

from stack import stack
from readf import read_file
from parser import parser
from symboltable import symboltable
from typing import (type_names, typetable, operation)
from error import (error_category, error)
from aopcode import *


TARGET = ...
MAX_NESTING_LEVEL = 255



def push_ttable(_cls, _type, _intern0=None, _intern1=None):
    _typetb = typetable()
    _typetb.types.append(_type)

    #! internal
    _typetb.internal0 = _intern0
    _typetb.internal1 = _intern1

    #! push type
    _cls.tstack.push(_typetb)


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
        self.symtbl = symboltable()
        self.tstack = stack(typetable)
        self.bcodes = []
        self.nstlvl = 0
        

    #! =========== VISITOR ===========
    
    def visit(self, _node):
        #! make visitor
        _visitor = getattr(self, "ast_" + _node.type.name.lower(), self.error)

        #! end
        return _visitor(_node)
    
    def error(self, _node):
        raise AttributeError("unimplemented node no# %d a.k.a %s!!!" % (_node.type.value, _node.type.name))
    
    #! =========== AST TREE ==========

    def ast_int(self, _node):
        #! max is int 64
        I64 = int(_node.get(0))

        #! type
        push_ttable(self, type_names.INT)

        #! opcode
        emit_opcode(self, iload, I64)
    

    def ast_float(self, _node):
        #! max is float 64
        F64 = float(_node.get(0))

        #! type
        push_ttable(self, type_names.FLOAT)

        #! opcode
        emit_opcode(self, fload, F64)
    

    def ast_str(self, _node):
        STR = str(_node.get(0))

        #! type
        push_ttable(self, type_names.STR)

        #! opcode
        emit_opcode(self, sload, STR)


    def ast_bool(self, _node):
        BOOL = _node.get(0) == "true"

        #! type
        push_ttable(self, type_names.BOOL)

        #! opcode
        emit_opcode(self, bload, BOOL)


    def ast_null(self, _node):
        #! type
        push_ttable(self, type_names.NULL)

        #! opcode
        emit_opcode(self, constn, None)

    
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
            _operation = _rhs.bit_not()

            #! emit int type
            push_ttable(self, type_names.INT)

            #! opcode
            emit_opcode(self, bit_not)
        
        elif _op == "!":
            #! op result
            _operation = _rhs.log_not()

            #! emit int type
            push_ttable(self, type_names.BOOL)

            #! opcode
            emit_opcode(self, log_not)

        elif _op == "+":
            #! op result
            _operation = _rhs.positive()

            match _operation:
                case operation.INT_OP:
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    #! opcode
                    emit_opcode(self, intpos)
                
                case operation.FLOAT_OP:
                    #! emit int type
                    push_ttable(self, type_names.FLOAT)

                    #! opcode
                    emit_opcode(self, fltpos)

        
        elif _op == "-":
            #! op result
            _operation = _rhs.negative()

            #! opcode
            match _operation:
                case operation.INT_OP:
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    #! opcode
                    emit_opcode(self, intneg)
                
                case operation.FLOAT_OP:
                    #! emit int type
                    push_ttable(self, type_names.FLOAT)

                    #! opcode
                    emit_opcode(self, fltneg)

        if  _operation == operation.BAD_OP:
            error.raise_tracked(error_category.CompileError, "invalid operation %s %s." % (_op, _rhs.repr()), _node.site)

        self.nstlvl -= 1
        #! end

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
            _operation = _lhs.exponent(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    emit_opcode(self, intadd)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, type_names.FLOAT)

                    emit_opcode(self, fltadd)

        elif _op == "*":
            #! op result
            _operation = _lhs.multiply(_rhs)

            #! emit float type
            push_ttable(self, type_names.FLOAT)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    emit_opcode(self, intmul)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, type_names.FLOAT)

                    emit_opcode(self, fltmul)

        elif _op == "/":
            #! op result
            _operation = _lhs.divide(_rhs)

            #! emit float type
            push_ttable(self, type_names.FLOAT)

            #! opcode
            emit_opcode(self, quotient)
            
        
        elif _op == "%":
            #! op result
            _operation = _lhs.modulo(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    emit_opcode(self, intrem)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, type_names.FLOAT)

                    emit_opcode(self, fltrem)

        elif _op == "+":
            #! op result
            _operation = _lhs.plus(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    emit_opcode(self, intadd)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, type_names.FLOAT)

                    emit_opcode(self, fltadd)
                
                case _:
                    #! emit str type
                    push_ttable(self, type_names.STR)

                    emit_opcode(self, concat)
        
        elif _op == "-":
            #! op result
            _operation = _lhs.minus(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, type_names.INT)

                    emit_opcode(self, intsub)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, type_names.FLOAT)
                    
                    emit_opcode(self, fltsub)
        
        elif _op == "<<" or _op == ">>":
            #! op result
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, type_names.INT)

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
            push_ttable(self, type_names.BOOL)

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
            _operation = _lhs.equal(_rhs)

            #! emit bool type
            push_ttable(self, type_names.BOOL)

            #! opcode
            if  _lhs.is_integer(_lhs) and\
                _rhs.is_integer(_rhs):
                emit_opcode(self, equal_i)

            elif _lhs.is_float(_lhs) and\
                 _rhs.is_float(_rhs):
                 emit_opcode(self, equal_f)
            
            elif _lhs.is_string(_lhs) and\
                 _rhs.is_string(_rhs):
                 emit_opcode(self, equal_s)
            
            elif _lhs.is_bool(_lhs) and\
                 _rhs.is_bool(_rhs):
                 emit_opcode(self, equal_b)
            
            elif _lhs.is_null(_lhs) and\
                 _rhs.is_null(_rhs):
                 emit_opcode(self, equal_n)
            
            else:
                emit_opcode(self, addressof)
            
            if  _op == "!=":
                #! negate
                emit_opcode(self, log_not)

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
        push_ttable(self, type_names.ANY)

        self.nstlvl -= 1
        #! end

    
    def ast_var_stmnt(self, _node):
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, type_names.NULL)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.var_exist_locally(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            #! opcode
            emit_opcode(self, store_name, self.offset)

            #! register
            self.symtbl.insert_variable(_variable[0], self.offset, _vtype, True, False)

            self.offset += 1
            #! end

    def ast_let_stmnt(self, _node):
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, type_names.NULL)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.var_exist_locally(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            #! opcode
            emit_opcode(self, store_name, self.offset)

            #! register
            self.symtbl.insert_variable(_variable[0], self.offset, _vtype, False, False)

            self.offset += 1
            #! end

    def ast_const_stmnt(self, _node):
        for _variable in _node.get(0):
            
            if  not _variable[1]:
                #! null
                push_ttable(self, type_names.NULL)

            else:
                self.visit(_variable[1])
            
            #! datatype
            _vtype = self.tstack.popp()

            if  self.symtbl.var_exist_locally(_variable[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _variable[0], _node.site)

            #! opcode
            emit_opcode(self, store_name, self.offset)

            #! register
            self.symtbl.insert_variable(_variable[0], self.offset, _vtype, False, True)

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
    """

    def __init__(self, _state):
        super().__init__()

        #! init prop
        self.__state = _state
        self.gparser = parser(self.__state)
    
    def ast_import(self, _node):
        for _each_import in _node.get(0)[::-1]:

            #! read file first
            read_file(self.__state, _each_import + ".as")

            #! parse
            _parse = parser(self.__state)
            
            for _each_node in _parse.raw_parse():
                #! visit each node
                self.visit(_each_node)
        #! end

    
    def generate(self):
        self.visit(self.gparser.parse())

        for x in self.bcodes:
            print(x)
        return self.bcodes

