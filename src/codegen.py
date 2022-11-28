

from stack import stack
from readf import read_file
from parser import parser

from symboltable import symboltable
from typechecking import (object_names, typetable)


from aopcode import *

def push_ttable(_cls, _type, _intern0=None, _intern1=None):
    _type = typetable()
    _type.types.append(_type)

    #! internal
    _type.internal0 = _intern0
    _type.internal1 = _intern1

    #! push type
    _cls.tstack.push(_type)


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
        _op = _node.get(1)
        self.visit(_node.get(2)) # rhs
        self.visit(_node.get(0)) # lhs

        _lhs = self.tstack.popp()
        _rhs = self.tstack.popp()

        if  _op == "+":

            #! opcode
            emit_opcode(self, intadd)


    def ast_expr_stmnt(self, _node):
        #! statement
        self.visit(_node.get(0))

        

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
