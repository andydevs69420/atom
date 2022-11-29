

from stack import stack
from readf import read_file
from parser import parser

from symboltable import symboltable
from typechecking import (object_names, typetable, operation)

from error import (error_category, error)

from aopcode import *

def push_ttable(_cls, _type, _intern0=None, _intern1=None):
    _typetb = typetable()
    _typetb.types.append(_type)

    #! internal
    _typetb.internal0 = _intern0
    _typetb.internal1 = _intern1

    #! push type
    _cls.tstack.push(_typetb)


def emit_opcode(_cls, _opcode, *_args):
    ...



class generator(object):
    """ Base code generator for atom.
    """

    def __init__(self):
        self.locals = 0
        self.symtbl = symboltable()
        self.tstack = stack(typetable)

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
        push_ttable(self, object_names.INT)

        #! opcode
        emit_opcode(self, iload, I64)
    

    def ast_float(self, _node):
        #! max is float 64
        F64 = float(_node.get(0))

        #! type
        push_ttable(self, object_names.FLOAT)

        #! opcode
        emit_opcode(self, fload, F64)
    

    def ast_str(self, _node):
        STR = str(_node.get(0))

        #! type
        push_ttable(self, object_names.STR)

        #! opcode
        emit_opcode(self, sload, STR)


    def ast_bool(self, _node):
        BOOL = _node.get(0) == "true"

        #! type
        push_ttable(self, object_names.BOOL)

        #! opcode
        emit_opcode(self, bload, BOOL)


    def ast_null(self, _node):
        #! type
        push_ttable(self, object_names.NULL)

        #! opcode
        emit_opcode(self, constn, None)


    def ast_binary_op(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        _op = _node.get(1)
        self.visit(_node.get(2)) # rhs
        self.visit(_node.get(0)) # lhs

        _lhs = self.tstack.popp()
        _rhs = self.tstack.popp()

        #! default
        _operation = operation.BAD_OP

        if  _op == "^^":
            _operation = _lhs.exponent(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, object_names.INT)

                    emit_opcode(self, intadd)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, object_names.FLOAT)

                    emit_opcode(self, fltadd)

        elif _op == "*":
            _operation = _lhs.multiply(_rhs)

            #! emit float type
            push_ttable(self, object_names.FLOAT)

           #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, object_names.INT)

                    emit_opcode(self, intmul)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, object_names.FLOAT)

                    emit_opcode(self, fltmul)

        elif _op == "/":
            _operation = _lhs.divide(_rhs)

            #! emit float type
            push_ttable(self, object_names.FLOAT)

            #! opcode
            emit_opcode(self, quotient)
            
        
        elif _op == "%":
            _operation = _lhs.modulo(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, object_names.INT)

                    emit_opcode(self, intrem)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, object_names.FLOAT)

                    emit_opcode(self, fltrem)

        elif _op == "+":
            _operation = _lhs.plus(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, object_names.INT)

                    emit_opcode(self, intadd)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, object_names.FLOAT)

                    emit_opcode(self, fltadd)
                
                case _:
                    #! emit str type
                    push_ttable(self, object_names.STR)

                    emit_opcode(self, concat)
        
        elif _op == "-":
            _operation = _lhs.minus(_rhs)

            #! opcode
            match _operation:
                case operation.INT_OP  :
                    #! emit int type
                    push_ttable(self, object_names.INT)

                    emit_opcode(self, intsub)

                case operation.FLOAT_OP:
                    #! emit float type
                    push_ttable(self, object_names.FLOAT)
                    
                    emit_opcode(self, fltsub)
        
        elif _op == "<<" or _op == ">>":
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, object_names.INT)

            #! opcode
            if  _op == "<<":
                emit_opcode(self, lshift)

            else:
                emit_opcode(self, rshift)
        
        elif _op == "<"  or \
             _op == "<=" or \
             _op == ">"  or \
             _op == ">=":
            _operation = _lhs.relational(_rhs)

            #! emit bool type
            push_ttable(self, object_names.BOOL)

            #! opcode
            if  _op == "<":
                emit_opcode(self, comlt )

            elif _op == "<=":
                emit_opcode(self, comlte)
            
            elif _op == ">":
                emit_opcode(self, comgt )

            elif _op == ">=":
                emit_opcode(self, comgte)
        
        elif _op == "!=" or \
             _op == "==":
            _operation = _lhs.equal(_rhs)

            #! emit bool type
            push_ttable(self, object_names.BOOL)

            #! opcode
            if  _lhs.is_integer(_lhs) and \
                _rhs.is_integer(_rhs):
                emit_opcode(self, equal_i)

            elif _lhs.is_float(_lhs) and \
                _rhs.is_float(_rhs):
                emit_opcode(self, equal_f)
            
            elif _lhs.is_string(_lhs) and \
                _rhs.is_string(_rhs):
                emit_opcode(self, equal_s)
            
            elif _lhs.is_bool(_lhs) and \
                _rhs.is_bool(_rhs):
                emit_opcode(self, equal_b)
            
            elif _lhs.is_null(_lhs) and \
                _rhs.is_null(_rhs):
                emit_opcode(self, equal_n)
            
            else:
                emit_opcode(self, addressof)
            

            if  _op == "!=":
                #! negate
                emit_opcode(self, unary_lnot)



        if  _operation == operation.BAD_OP:
            error.raise_tracked(
                error_category.CompileError, "invalid operation %s %s %s." % (_lhs.repr(), _op, _rhs.repr()), _node.locs)



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
        for _each_import in _node.statements[0]:

            #! read file first
            read_file(self.__state, _each_import + ".as")

            print(_each_import)
        
        #! ast

    
    def generate(self):
        return self.visit(self.gparser.parse())

