""" Static analyzer and compiler for atom.
"""

from os import path
from stack import stack
from readf import (file_isfile, read_file)
from aparser import parser
from symboltable2 import SymbolTable
from atyping import *
from error import (error_category, error)
from aopcode import *
from aast import ast_type
from abuiltins.getter import getbuiltin

TARGET = ...

def push_ttable(_cls, _type):
    #! push type
    _cls.tstack.generic_push(_type)

def get_byteoff(_cls):
    return len(_cls.bcodes) * 2

def emit_opcode(_cls, _opcode, *_args):
    _cls.bcodes.append([get_byteoff(_cls), _opcode, *_args])
    return _cls.bcodes[-1]

class constantevaluator(object):
    """ Removes the obvious part of the bytecode.

        ex:
            let x = 2 + 2;

        produce:
            0   iload  4
            2   store_local x 0
    """

    def visit_evaluator(self, _node):
        #! make visitor
        _visitor = getattr(self, "eval_" + _node.type.name.lower(), self.visit_evaluator_error)

        #! end
        return _visitor(_node)
    
    def visit_evaluator_error(self, _node):
        return ...

    def eval_int(self, _node):
        #! parse
        _integer = int(_node.get(0))

        #! get size
        _intsize = integer_t.auto(_integer)

        if  _intsize.iserror():
            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

        #! make auto int
        return (_intsize, _integer)
    
    def eval_float(self, _node):
        #! parse
        _float = float(_node.get(0))

        #! get size
        _fsize = float_t.auto(_float)

        if  _fsize.iserror():
            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

        #! make auto int
        return (_fsize, _float)

    def eval_str(self, _node):
        return (string_t() , str(_node.get(0)))

    def eval_bool(self, _node):
        return (boolean_t(), bool(_node.get(0) == "true"))

    def eval_null(self, _node):
        return (null_t(), None)
    
    def eval_unary_op(self, _node):
        """ 
             $0   $1 
            _op  _rhs
        """
        _op = _node.get(0)
        #! eval rhs
        _rhs =\
        self.visit_evaluator(_node.get(1))

        if _rhs == ...: return ...

        _result = ...

        if  _op == "~":
            _result = _rhs[0].bitnot()

            if  not _result.iserror():
                _data = ~ _rhs[1]

                if  _result.isint():
                    #! get size
                    if  integer_t.auto(_data).iserror():
                        error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                return (_result, _data)

        if  _op == "!":
            _result = _rhs[0].lognot()

            if  not _result.iserror():
                return (_result, not _rhs[1])
        
        if  _op == "+":
            _result = _rhs[0].pos()

            if  not _result.iserror():
                return (_result, + _rhs[1])
        
        if  _op == "-":
            _result = _rhs[0].neg()

            if  not _result.iserror():
                return (_result, - _rhs[1])

        #! end
        error.raise_tracked(error_category.CompileError, "invalid operation %s %s." % (_op, _rhs[0].repr()), _node.site)

    def eval_binary_op(self, _node):
        """ 
             $0   $1    $2
            _lhs  _op  _rhs
        """
        _op = _node.get(1)
        #! eval rhs
        _rhs =\
        self.visit_evaluator(_node.get(2))

        #! eval lhs
        _lhs =\
        self.visit_evaluator(_node.get(0))

        if _lhs == ... or _rhs == ...: return ...

        _result = ...

        try:

            if  _op == "^^":
                _result = _lhs[0].pow(_rhs[0])

                if  not _result.iserror():
                    _data = _lhs[1] ** _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    else:
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)

            if  _op == "*":
                _result = _lhs[0].mul(_rhs[0])

                if  not _result.iserror():
                    _data = _lhs[1] * _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    else:
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)

            if  _op == "/":
                _result = _lhs[0].div(_rhs[0])
                
                if  not _result.iserror():
                    if  _rhs[1] == 0:
                        error.raise_tracked(error_category.CompileError, "zero division error.", _node.site)

                    _data = _lhs[1] / _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    else:
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "%":
                _result = _lhs[0].mod(_rhs[0])
                
                if  not _result.iserror():
                    if  _rhs[1] == 0:
                        error.raise_tracked(error_category.CompileError, "zero division error.", _node.site)

                    _data = _lhs[1] % _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    else:
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "+":
                _result = _lhs[0].add(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] + _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    elif _result.isfloat():
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "-":
                _result = _lhs[0].sub(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] - _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)
                    else:
                        #! get size
                        if  float_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "<<":
                _result = _lhs[0].shift(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] << _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == ">>":
                _result = _lhs[0].shift(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] >> _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "<":
                _result = _lhs[0].relational(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] < _rhs[1])
            
            if  _op == "<=":
                _result = _lhs[0].relational(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] <= _rhs[1])
            
            if  _op == ">":
                _result = _lhs[0].relational(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] > _rhs[1])
            
            if  _op == ">=":
                _result = _lhs[0].relational(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] >= _rhs[1])
            
            if  _op == "==":
                _result = _lhs[0].equality(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] == _rhs[1])
            
            if  _op == "!=":
                _result = _lhs[0].equality(_rhs[0])
                
                if  not _result.iserror():
                    return (_result, _lhs[1] != _rhs[1])
            
            if  _op == "&":
                _result = _lhs[0].bitwise(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] & _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "^":
                _result = _lhs[0].bitwise(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] ^ _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                    return (_result, _data)
            
            if  _op == "|":
                _result = _lhs[0].bitwise(_rhs[0])
                
                if  not _result.iserror():
                    _data = _lhs[1] | _rhs[1]

                    if  _result.isint():
                        #! get size
                        if  integer_t.auto(_data).iserror():
                            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

                    return (_result, _data)

        except OverflowError:
            error.raise_tracked(error_category.CompileError, "expression (%s %s %s) causes overflow." % (_lhs[1], _op, _rhs[1]), _node.site)

        except ArithmeticError:
            error.raise_tracked(error_category.CompileError, "expression (%s %s %s) causes arithmetic error." % (_lhs[1], _op, _rhs[1]), _node.site)

        #! end
        error.raise_tracked(error_category.CompileError, "invalid operation %s %s %s." % (_lhs[0].repr(), _op, _rhs[0].repr()), _node.site)

    def eval_shortc_op(self, _node):
        """ 
             $0   $1    $2
            _lhs  _op  _rhs
        """
        _op = _node.get(1)
        #! eval rhs
        _rhs =\
        self.visit_evaluator(_node.get(2))

        #! eval lhs
        _lhs =\
        self.visit_evaluator(_node.get(0))

        if _lhs == ... or _rhs == ...: return ...

        if  _op == "&&":

            if  _lhs[1]:
                return (_rhs[0], _rhs[1])

            else:
                return (_lhs[0], _lhs[1])
        
        if  _op == "||":

            if  _lhs[1]:
                return (_lhs[0], _lhs[1])

            else:
                return (_rhs[0], _rhs[1])
        
        #! end
        error.raise_tracked(error_category.CompileError, "invalid operation %s %s %s." % (_lhs[0].repr(), _op, _rhs[0].repr()), _node.site)
    
    def try_eval_una_op(self, _node):
        return self.visit_evaluator(_node)

    def try_eval_bin_op(self, _node):
        return self.visit_evaluator(_node)
    
    def try_eval_short_op(self, _node):
        return self.visit_evaluator(_node)


class source_to_interface(constantevaluator):

    def __init__(self):
        super().__init__()
        
        #! virtual offset
        self.virtoffset = 0
        self.virtualstructnumber = 0
    
    def visit_int(self, _node):
        #! make visitor
        _visitor = getattr(self, "int_" + _node.type.name.lower(), self.error_int)

        #! end
        return _visitor(_node)
    
    def error_int(self, _node):
        raise AttributeError("unimplemented node no# %d a.k.a %s!!!" % (_node.type.value, _node.type.name))

    def int_any_t(self, _node):
        #! push int type
        return any_t()

    def int_int_t(self, _node):
        #! push int type
        _tname = _node.get(0)

        return integer_t()
    
    def int_float_t(self, _node):
        #! push float type
        return float_t()
    
    def int_str_t(self, _node):
        #! push str type
        return string_t()
    
    def int_bool_t(self, _node):
        #! push bool type
        return boolean_t()

    def int_void_t(self, _node):
        #! push void type
        return null_t()

    def int_array_t(self, _node):
        #! internal
        _internal =\
        self.visit_int(_node.get(1))

        #! push array type
        return array_t(_internal)

    
    def int_fn_t(self, _node):
        #! return
        _return =\
        self.visit_int(_node.get(1))

        _plength = len(_node.get(2))

        _params = []

        for _idx in range(_plength):
            #! visit
            _params.append((f"param{_idx}", self.visit_int(_node.get(2)[_idx])))

        #! push int type
        return fn_t(_return, _plength, _params)

    
    def int_map_t(self, _node):
        #! key type
        _key =\
        self.visit(_node.get(1))

        #! val type
        _val =\
        self.visit(_node.get(2))

        #! push int type
        return map_t(_key, _val)
    
    def int_type_t(self, _node):
        """ User defined type.
        """
        #! check
        if  not self.symtbl.contains(_node.get(0)):
            error.raise_tracked(error_category.CompileError, "type %s is not defined." % _node.get(0), _node.site)

        _info = self.symtbl.lookup(_node.get(0))
        
        #! datatype
        _dtype = _info.get_datatype()

        #! emit type
        return _dtype.returntype
    

    def int_struct(self, _node):
        """    
               $0      $1
            subtypes  body
        """
        #! print("DEBUG: interface -> struct")
        _old_offset = self.virtoffset

        for _each_subtype in _node.get(0):

            #! check if function|struct name is already defined.
            if  self.symtbl.contains(_each_subtype):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_subtype, _node.site)
         
            self.virtoffset = 0

            #! make scope
            self.symtbl.newscope()

            _members = []

            if  len(_node.get(1)) <= 0:
                error.raise_tracked(error_category.CompileError, "struct \"%s\" has empty body." %  _each_subtype, _node.site)

            for _each_member in _node.get(1):

                #! visit type
                _dtype =\
                self.visit_int(_each_member[1])

                #! check if parameter is already defined.
                if  self.symtbl.haslocal(_each_member[0]):
                    error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_member[0], _node.site)

                #! insert
                _members.append((_each_member[0], _dtype))

                #! register
                self.symtbl.insert_var(_each_member[0], self.virtoffset, _dtype, False, False, _node.site)

                self.virtoffset += 1
                #! end

            #! leave scope
            self.symtbl.endscope()

            #! restore
            self.virtoffset = _old_offset
            
            #! struct becomes a function
            _type = type_t(self.virtualstructnumber, _each_subtype, instance_t(self.virtualstructnumber, _each_subtype), len(_members), tuple(_members))

            #! register
            self.symtbl.insert_struct(_each_subtype, self.virtoffset, _type, _node.site)

            #! end
            self.virtoffset += 1
            _old_offset  = self.virtoffset

        #! increment every struct dec
        self.virtualstructnumber += 1
    
    def int_implements(self, _node):
        """
              $0   $1
            _name _body
        """
        #! print("DEBUG: interface -> implements")
        _name = _node.get(0)

        self.symtbl.newscope()
        self.names.append(_name)

        #! check if type exist
        if  not self.symtbl.contains(_name):
            error.raise_tracked(error_category.CompileError, "type %s is not defined." % _name, _node.site)
        
        _typeinfo = self.symtbl.lookup(_node.get(0))

        if  not _typeinfo.get_datatype().istype():
            error.raise_tracked(error_category.CompileError, "name %s is not a type." % _name, _node.site)
        
        #! make interface
        for _each_method in _node.get(1):
            assert _each_method.type == ast_type.METHOD, "not a method!!!"
            self.visit_int(_each_method)
        
        #! save
        for _each_symbol in self.symtbl.current().aslist():
            _name = _each_symbol[0].split(".")[1]
            _typeinfo.get_datatype().insert_method((_each_symbol[0].split(".")[1], _each_symbol[1].get_datatype()))

        self.names.pop()
        _symbols =\
        self.symtbl.endscope()

        #! unpack content globally
        for _each_symbol in _symbols.aslist():
            self.symtbl.insert_fun(_each_symbol[0], _each_symbol[1].get_offset(), _each_symbol[1].get_datatype(), _each_symbol[1].get_returntype(), _each_symbol[1].get_site())
    

    def int_method(self, _node):
        """    
               $0        $1     $2        $3     $4
            returntype  name  _self  parameters  body
        """
        #! print("DEBUG: interface -> method")
        _old_offset = self.virtoffset

        self.virtoffset = 0

        #! =======================
        _parameters = []

        #! set current function
        _returntype =\
        self.visit_int(_node.get(0))

        #! check if function name is already defined.
        if  self.symtbl.haslocal(_node.get(1)):
            error.raise_tracked(error_category.CompileError, "method \"%s\" was already defined." %  _node.get(1), _node.site)

        #! new func scope
        self.symtbl.newscope()

        _typeinfo = self.symtbl.lookup(self.names[-1])

        #! mark as instance
        _selftype = instance_t(_typeinfo.get_datatype().typenumber, _typeinfo.get_datatype().typename)

        #! as param
        _parameters.append((_node.get(2), _selftype))

        #! register
        self.symtbl.insert_var(_node.get(2), self.virtoffset, _selftype, False, False, _node.site)

        self.virtoffset += 1
        
        #! compile parameters
        for _each_param in _node.get(3):

            #! param dtype
            _vtype =\
            self.visit_int(_each_param[1])

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

            #! register
            self.symtbl.insert_var(_each_param[0], self.virtoffset, _vtype, False, False, _node.site)

            self.virtoffset += 1
            #! end

        #! end func scope
        self.symtbl.endscope()

        #! restore
        self.virtoffset = _old_offset

        #! final: Type.function
        _finalname = self.names[-1] + "." + _node.get(1)

        #! register
        self.symtbl.insert_fun(_finalname, self.virtoffset, method_t(_returntype, len(_parameters), _parameters), _returntype, _node.site)

        #! end
        self.virtoffset += 1

    def int_function(self, _node):
        """    
               $0        $1       $2       $3
            returntype  name  parameters  body
        """
        #! print("DEBUG: interface -> function")
        _old_offset = self.virtoffset

        self.virtoffset = 0

        #! =======================
        _parameters = []

        #! set current function
        _returntype =\
        self.visit_int(_node.get(0))

        #! new func scope
        self.symtbl.newscope()

        #! check if function name is already defined.
        if  self.symtbl.contains(_node.get(1)):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(1), _node.site)

        #! compile parameters
        for _each_param in _node.get(2):

            #! param dtype
            _vtype =\
            self.visit_int(_each_param[1])

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

            #! register
            self.symtbl.insert_var(_each_param[0], self.virtoffset, _vtype, False, False, _node.site)

            self.virtoffset += 1
            #! end

        #! end func scope
        self.symtbl.endscope()

        #! restore
        self.virtoffset = _old_offset

        #! register
        self.symtbl.insert_fun(_node.get(1), self.virtoffset, fn_t(_returntype, len(_parameters), _parameters), _returntype, _node.site)

        #! end
        self.virtoffset += 1
    
    def int_function_wrapper(self, _node):
        """    
                $0        $1          $2          $3     $4
            returntype  wraptype  wrapper_name  params  return
        """
        #! print("DEBUG: interface -> function wrapper")
        _old_offset = self.virtoffset

        self.virtoffset = 0

        #! =======================
        _parameters = []

        #! new func scope
        self.symtbl.newscope()

        #! visit return type
        _returntype =\
        self.visit_int(_node.get(0))

        _param0 = _node.get(1)

        #! parameter 1 datatype
        _ptype0 =\
        self.visit_int(_param0[1])
        
        _name = _node.get(2)

        #! check if function name is already defined.
        if  self.symtbl.contains(_name):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _name, _node.site)
        
        #! make param list
        _parameters.append((_param0[0], _ptype0))

        #! register
        self.symtbl.insert_var(_param0[0], self.virtoffset, _ptype0, False, False, _node.site)

        self.virtoffset += 1

        #! compile parameters
        for _each_param in _node.get(3):

            #! param dtype
            _vtype =\
            self.visit_int(_each_param[1])

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

            #! register
            self.symtbl.insert_var(_each_param[0], self.virtoffset, _vtype, False, False, _node.site)

            self.virtoffset += 1
            #! end

        #! end func scope
        self.symtbl.endscope()

        #! restore
        self.virtoffset = _old_offset

        #! register
        self.symtbl.insert_fun(_name, self.virtoffset, fn_t(_returntype, len(_parameters), _parameters), _returntype, _node.site)

        #! end
        self.virtoffset += 1
    
    def int_native_function(self, _node):
        """    
            $0        $1          $2       $3     $4
            mod   returntype  func_name  params  body
        """
        #! print("DEBUG: interface -> native function")
        _parameters = []

        #! new func scope
        self.symtbl.newscope()

        #! visit returntype
        _returntype =\
        self.visit_int(_node.get(1))

        #! check if function name is already defined.
        if  self.symtbl.contains(_node.get(2)):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(2), _node.site)

        #! compile parameters
        for _each_param in _node.get(3):

            #! visit type
            self.visit(_each_param[1])

            #! param dtype
            _vtype = self.tstack.popp()

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

        #! end func scope
        self.symtbl.endscope()

        #! datatype
        _datatype = nativefn_t(_returntype, len(_parameters), _parameters)

        #! register
        self.symtbl.insert_fun(_node.get(2), self.virtoffset, _datatype, _returntype, _node.site)


        #! end
        self.virtoffset += 1


class generator(source_to_interface):
    """ Base code generator for atom.
    """

    def __init__(self):
        super().__init__()
        self.offset = 0
        self.imptbl = SymbolTable() #! import table
        self.symtbl = SymbolTable() #! symbol table
        self.tstack = stack(tag_t)
        self.bcodes = []

        #! struct
        self.currentstructnumber   = 0
        #! function
        self.currentfunctiontype   = None
        self.functionhasreturntype = False
        #! loops
        self.loops  = []
        self.breaks = []

        #! function call
        self.callid = 0

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
        _tname = _node.get(0)

        push_ttable(self, integer_t())
    
    def ast_float_t(self, _node):
        #! push float type
        push_ttable(self, float_t())
    
    def ast_str_t(self, _node):
        #! push str type
        push_ttable(self, string_t())
    
    def ast_bool_t(self, _node):
        #! push bool type
        push_ttable(self, boolean_t())

    def ast_void_t(self, _node):
        #! push void type
        push_ttable(self, null_t())

    def ast_array_t(self, _node):
        #! internal
        self.visit(_node.get(1))

        _internal = self.tstack.popp()

        #! push array type
        push_ttable(self, array_t(_internal))

    
    def ast_fn_t(self, _node):
        #! return
        self.visit(_node.get(1))

        _return = self.tstack.popp()

        _plength = len(_node.get(2))

        _params = []

        for _idx in range(_plength):
            #! visit
            self.visit(_node.get(2)[_idx])

            _params.append((f"param{_idx}", self.tstack.popp()))

        #! push int type
        push_ttable(self, fn_t(_return, _plength, _params))

    
    def ast_map_t(self, _node):
        #! val type
        self.visit(_node.get(2))

        #! key type
        self.visit(_node.get(1))

        _key = self.tstack.popp()
        _val = self.tstack.popp()

        #! push int type
        push_ttable(self, map_t(_key, _val))
    
    def ast_type_t(self, _node):
        """ User defined type.
        """
        #! check
        if  not self.symtbl.contains(_node.get(0)):
            error.raise_tracked(error_category.CompileError, "type %s is not defined." % _node.get(0), _node.site)

        _info = self.symtbl.lookup(_node.get(0))
        
        #! datatype
        _dtype = _info.get_datatype()

        #! emit type
        push_ttable(self, _dtype.returntype)

    #! =========== CONST VAL ==========

    def ast_int(self, _node):
        #! max is int 128
        I128 = int(_node.get(0))

        #! get size
        _sze = integer_t.auto(I128)

        if  _sze.iserror():
            error.raise_tracked(error_category.CompileError, "integer underflowed or overflowed.", _node.site)

        #! type
        push_ttable(self, _sze)

        #! opcode
        emit_opcode(self, iload, I128)
    

    def ast_float(self, _node):
        #! max is float 64
        F64 = float(_node.get(0))

        #! get size
        _sze = float_t.auto(F64)

        if  _sze.iserror():
            error.raise_tracked(error_category.CompileError, "float underflowed or overflowed.", _node.site)

        #! type
        push_ttable(self, _sze)

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
    
    def exact_size(self, _type, _current):
        if  _current.isarray():
            _current = _current.elementtype
      
        if  _current.matches(_type):
            #!
            
            if  _current.isbigint():
                _type = _current
            if  _current.islong():
                _type = _current
            if  _current.isint32():
                _type = _current
            if  _current.isshort():
                _type = _current
            if  _current.isbyte():
                _type = _current
            
        return _type

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
                if  not _hasunpack:
                    emit_opcode(self, build_array, _arrsize)

                #! =========================
                _hasunpack = True
                
                #! unpack element
                self.visit(_elem)

                #! virtual current
                _current = self.tstack.popp()

                #! current
                _arrtype = _current.elementtype if not _arrtype else _arrtype

                
            else:
                self.visit(_elem)

                #! virtual current
                _current = self.tstack.popp()

                #! current
                _arrtype = _current if not _arrtype else _arrtype
            
                if  _hasunpack:
                    #! opcode
                    emit_opcode(self, array_push)
            
            _arrsize += 1
     
            if  _current.isarray():
                if  not _current.elementtype.matches(_arrtype):
                    #! array of any
                    push_ttable(self, any_t())

                    #! set as array element type
                    _arrtype = self.tstack.popp()

            else:
                if  not _current.matches(_arrtype):
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
    
    def ast_map(self, _node):
        _keytype = None
        _valtype = None
        _element = _node.get(0)[::-1]
        _mapsize = 0
        _hasunpack = False

        while _mapsize < len(_element):
            #! element
            _elem = _element[_mapsize]
            _currentk = ...
            _currentv = ...

            if  _elem[0].type == ast_type.UNARY_UNPACK:
                #! build array before unpack
                #! opcode
                if  not _hasunpack:
                    emit_opcode(self, build_map, _mapsize)

                #! =========================
                _hasunpack = True
                
                #! unpack element
                self.visit(_elem[0])

                #! virtual current key
                _currentk = self.tstack.peek().keytype
                #! virtual current val
                _currentv = self.tstack.popp().valtype

                #! current key
                _keytype = _currentk if not _keytype else _keytype

                #! current val
                _valtype = _currentv if not _valtype else _valtype

                
            else:
                #! visit val
                self.visit(_elem[1])

                #! visit key
                self.visit(_elem[0])

                #! virtual current key
                _currentk = self.tstack.popp()

                #! virtual current val
                _currentv = self.tstack.popp()

                #! current key
                _keytype = _currentk if not _keytype else _keytype

                #! current val
                _valtype = _currentv if not _valtype else _valtype
            
                if  _hasunpack:
                    #! opcode
                    emit_opcode(self, map_put)
            
            _mapsize += 1

            if  not _keytype.matches(_currentk):
                #! array of any
                push_ttable(self, any_t())

                #! set as array element type
                _keytype = self.tstack.popp()
            
            if  not _valtype.matches(_currentv):
                #! array of any
                push_ttable(self, any_t())

                #! set as array element type
                _valtype = self.tstack.popp()

    
        if  not _hasunpack:
            #! opcode
            emit_opcode(self, build_map, _mapsize)
        
        if  _mapsize <= 0:
            #! val of any
            push_ttable(self, any_t())

            #! key of any
            push_ttable(self, any_t())

            #! set as map element key type
            _keytype = self.tstack.popp()

            #! set as map element val type
            _valtype = self.tstack.popp()

        #! array type
        push_ttable(self, map_t(_keytype, _valtype))

    def ast_attribute(self, _node):
        """ 
             $0         $1
            object  attribute
        """
        #! visit object
        self.visit(_node.get(0))

        #! type
        _dtype = self.tstack.popp()

        if  _dtype.isenum():

            if  not _dtype.hasAttribute(_node.get(1)):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _node.get(1)), _node.site)

            _attribtype = _dtype.getAttribute(_node.get(1))

            #! emit attribute type
            push_ttable(self, _attribtype)

            #! push attribute as string
            emit_opcode(self, sload, _node.get(1))

            #! get
            emit_opcode(self, get_enum)
            
        elif _dtype.isinstance():

            if  not self.symtbl.contains(_dtype.qualname()):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _node.get(1)), _node.site)

            #! structtable
            _info = self.symtbl.lookup(_dtype.qualname())

            _type = _info.get_datatype()

            if  not _type.istype():
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _node.get(1)), _node.site)
            
            if  not (_type.hasAttribute(_node.get(1)) or _type.hasMethod(_node.get(1))):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _node.get(1)), _node.site)

            _attrib_or_method_type = _type.getAttribute(_node.get(1)) if _type.hasAttribute(_node.get(1)) else _type.getMethod(_node.get(1))

            if  _attrib_or_method_type.ismethod():
                #! emit attribute type
                push_ttable(self, _attrib_or_method_type)

                #! pop object
                emit_opcode(self, pop_top)

                #! emit as string
                emit_opcode(self, sload, "<method %s.%s/>" % (_dtype.qualname(), _node.get(1)))

            else:
                #! emit attribute type
                push_ttable(self, _attrib_or_method_type)

                #! push attribute as string
                emit_opcode(self, sload, _node.get(1))

                #! get
                emit_opcode(self, get_attribute)
        
        elif _dtype.ismodule():
            #! check
            if  not _dtype.hasAttribute(_node.get(1)):
                error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _node.get(1)), _node.site)

            _attribtype = _dtype.getAttribute(_node.get(1))

            #! emit attribute type
            push_ttable(self, _attribtype)

            #! push attribute as string
            emit_opcode(self, sload, _node.get(1))

            #! just use get attribute because module is an object
            emit_opcode(self, get_attribute)
        
        elif _dtype.isarray():
            #! pop array
            emit_opcode(self, pop_top)

            #! emit attribute type as str
            push_ttable(self, string_t())

            _vattrib = _node.get(1)

            if  _vattrib == "push":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod array.push/>")
            
            elif _vattrib == "pop":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod array.pop/>")
            
            elif _vattrib == "peek":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod array.peek/>")

            elif _vattrib == "size":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod array.size/>")
            
            else:
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _vattrib), _node.site)
        
        elif _dtype.ismap():
            #! pop array
            emit_opcode(self, pop_top)

            #! emit attribute type as str
            push_ttable(self, string_t())

            _vattrib = _node.get(1)

            if  _vattrib == "keys":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod map.keys/>")
            
            elif _vattrib == "values":
                #! emit as string
                emit_opcode(self, sload, "<abstractmethod map.values/>")
            
            else:
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _vattrib), _node.site)

        else:
            error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _node.get(1)), _node.site)
    
    def ast_element(self, _node):
        """ 
             $0       $1
            object  element
        """
        #! compile element
        self.visit(_node.get(1))

        _element_type = self.tstack.popp()

        #! compile object
        self.visit(_node.get(0))

        _objtype = self.tstack.popp()

        #! check if subscriptable
        if  _objtype.isarray():
            #! verify index
            if  not _element_type.isint():
                error.raise_tracked(error_category.CompileError, "array index should be int, got %s." % _element_type.repr(), _node.site)

            #! push array element type
            push_ttable(self, _objtype.elementtype)

            #! opcode
            emit_opcode(self, array_get)
        
        elif _objtype.ismap():
            #! verify element key
            if  not _objtype.keytype.matches(_element_type):
                error.raise_tracked(error_category.CompileError, "%s key should be %s, got %s." % (_objtype.repr(), _objtype.keytype.repr(), _element_type.repr()), _node.site)

            #! push map value type
            push_ttable(self, _objtype.valtype)

            #! opcode
            emit_opcode(self, map_get)
        
        elif _objtype.isstring():
            #! verify index
            if  not _element_type.isint():
                error.raise_tracked(error_category.CompileError, "string index should be int, got %s." % _element_type.repr(), _node.site)

            #! push map value type
            push_ttable(self, string_t())

            #! opcode
            emit_opcode(self, string_get)

        else:
            error.raise_tracked(error_category.CompileError, "%s is not subscriptable." % _objtype.repr(), _node.site)


    def ast_call_wrapper(self, _node):
        """ 
             $0      $1      $2
            object  name  parameters
        """
        #! make call
        self.state.calls[self.callid] = _node.site
        self.callid += 1
        
        #! wrap name
        _name = _node.get(1)
        
        #! compile object
        self.visit(_node.get(0))

        #! type 
        _dtype = self.tstack.popp()
        
        #! check wrapper
        if  not self.symtbl.contains(_name):
            error.raise_tracked(error_category.CompileError, "wrapper function \"%s\" for type %s is not defined." % (_name, _dtype.repr()), _node.site)

        _info = self.symtbl.lookup(_name)

        #! datatype
        _functype = _info.get_datatype()

        #! check if callable|wrapper
        if  not _functype.isfunction():
            error.raise_tracked(error_category.CompileError, "%s is not a user defined function eg: wrapper, fun." % _functype.repr(), _node.site)

        #! check parameter count
        if  _functype.paramcount != (len(_node.get(2)) + 1):
            error.raise_tracked(error_category.CompileError, "%s requires %d argument, got %d." % (_name, _functype.paramcount - 1, len(_node.get(2))), _node.site)
        
        #! emit return type
        push_ttable(self, _functype.returntype)

        #! load function
        emit_opcode(self, load_global, _name, _info.get_offset())

        #! rotate param
        emit_opcode(self, rot2)

        _index = 0

        _recieve_param = _node.get(2)
        _rquired_param = _functype.parameters[1:]

        if  not _functype.parameters[0][1].matches(_dtype):
            error.raise_tracked(error_category.CompileError, "can't wrap %s with \"%s\". required %s, got %s." % (_dtype.repr(), _name, _functype.parameters[0][1].repr(), _dtype.repr()), _node.site)

        #! check every arguments
        for _each_param in _recieve_param[::-1]:

            #! visit param
            self.visit(_each_param)

            _typeN = self.tstack.popp()

            #! match type
            if  not _rquired_param[_index][1].matches(_typeN):
                error.raise_tracked(error_category.CompileError, "parameter \"%s\" expects argument datatype %s, got %s." % (_rquired_param[_index][0], _rquired_param[_index][1].repr(), _typeN.repr()), _node.site)

            _index += 1

            #! rotate until last
            emit_opcode(self, rot2)
        
        #! emit
        emit_opcode(self, call_function, len(_node.get(2)) + 1, self.callid - 1)
        

    def ast_call(self, _node):
        """ 
             $0         $1
            object  parameters
        """
        #! make call
        self.state.calls[self.callid] = _node.site
        self.callid += 1

        if  _node.get(0).type == ast_type.ATTRIBUTE:
            #! redirect
            return self.call_method(_node)

        #! visit object
        self.visit(_node.get(0))

        #! datatype
        _functype = self.tstack.popp()

        #! check if callable
        if  not (_functype.isfunction() or _functype.isnativefunction() or _functype.istype() or _functype.ismethod()):
            error.raise_tracked(error_category.CompileError, "%s is not a callable type." % _functype.repr(), _node.site)

        #! check parameter count
        if  _functype.paramcount != len(_node.get(1)):
            error.raise_tracked(error_category.CompileError, "%s requires %d argument, got %d." % (_functype.repr(), _functype.paramcount, len(_node.get(1))), _node.site)

        #! emit return type
        push_ttable(self, _functype.returntype)

        _index = 0

        #! check every arguments
        for _each_param in _node.get(1)[::-1]:

            #! visit param
            self.visit(_each_param)

            _typeN = self.tstack.popp()

            #! match type
            if  not _functype.parameters[::-1][_index][1].matches(_typeN):
                error.raise_tracked(error_category.CompileError, "parameter \"%s\" expects argument datatype %s, got %s." % (_functype.parameters[::-1][_index][0], _functype.parameters[::-1][_index][1].repr(), _typeN.repr()), _node.site)

            _index += 1
        
        #! opcode
        if  _functype.isnativefunction():
            #! emit
            emit_opcode(self, call_native, len(_node.get(1)), self.callid - 1)

        elif _functype.isfunction():
            #! emit
            emit_opcode(self, call_function, len(_node.get(1)), self.callid - 1)

        else:
            #! emit
            emit_opcode(self, call_type, len(_node.get(1)), self.callid - 1)

    def call_method(self, _node):
        #! 
        _attrib_node = _node.get(0)

        #! compile object
        self.visit(_attrib_node.get(0))

        _dtype =\
        self.tstack.popp()

        _attrib_name = _attrib_node.get(1)

        if  _dtype.isenum():

            if  not _dtype.hasAttribute(_node.get(1)):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _attrib_name), _node.site)

            _attribtype = _dtype.getAttribute(_attrib_name)

            #! emit attribute type
            push_ttable(self, _attribtype)

            #! push attribute as string
            emit_opcode(self, sload, _attrib_name)

            #! get
            emit_opcode(self, get_enum)

            #! add call
            self.call_part(_node)
            
        elif _dtype.isinstance():

            if  not self.symtbl.contains(_dtype.qualname()):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _attrib_name), _node.site)

            #! structtable
            _info = self.symtbl.lookup(_dtype.qualname())

            _type = _info.get_datatype()

            if  not _type.istype():
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _attrib_name), _node.site)

            if  not _type.hasMethod(_attrib_name):
                error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _attrib_name), _node.site)

            _attrib_or_method_type = _type.getAttribute(_attrib_name) if _type.hasAttribute(_attrib_name) else _type.getMethod(_attrib_name)

            if  _attrib_or_method_type.ismethod():
                #! emit attribute type
                push_ttable(self, _attrib_or_method_type)

                _method = _dtype.qualname() + "." + _attrib_name

                _info = self.symtbl.lookup(_method)

                emit_opcode(self, load_global, _method, _info.get_offset())

                #! add call
                self.call_method_part(_node)

            else:
                #! emit attribute type
                push_ttable(self, _attrib_or_method_type)

                #! push attribute as string
                emit_opcode(self, sload, _attrib_name)

                #! get
                emit_opcode(self, get_attribute)

                #! add call
                self.call_part(_node)
        
        elif _dtype.ismodule():
            #! check
            if  not _dtype.hasAttribute(_attrib_node.get(1)):
                error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _attrib_name), _node.site)

            _attribtype = _dtype.getAttribute(_attrib_name)

            #! emit attribute type
            push_ttable(self, _attribtype)

            #! push attribute as string
            emit_opcode(self, sload, _attrib_name)

            #! just use get attribute because module is an object
            emit_opcode(self, get_attribute)

            #! add call
            self.call_part(_node)
        
        elif _dtype.isarray():
            if  _attrib_name == "push":
                #! check parameter count
                if  len(_node.get(1)) != 1:
                    error.raise_tracked(error_category.CompileError, "push requires 1 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit null
                push_ttable(self, null_t())

                #! compile call args
                self.call_abstract_args(_node, [("_element", _dtype.elementtype)])

                #! add call
                emit_opcode(self, array_push)
            
            elif _attrib_name == "pop":
                #! check parameter count
                if  len(_node.get(1)) != 0:
                    error.raise_tracked(error_category.CompileError, "pop requires 0 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit elementtype
                push_ttable(self, _dtype.elementtype)

                #! emit array pop
                emit_opcode(self, array_pop)
            
            elif _attrib_name == "peek":
                #! check parameter count
                if  len(_node.get(1)) != 0:
                    error.raise_tracked(error_category.CompileError, "peek requires 0 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit elementtype
                push_ttable(self, _dtype.elementtype)

                #! emit array peek
                emit_opcode(self, array_peek)
            
            elif _attrib_name == "size":
                #! check parameter count
                if  len(_node.get(1)) != 0:
                    error.raise_tracked(error_category.CompileError, "size requires 0 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit elementtype
                push_ttable(self, integer_t())

                #! emit array size
                emit_opcode(self, array_size)
            
            else:
                error.raise_tracked(error_category.CompileError, "%s has no method %s." % (_dtype.repr(), _attrib_name), _node.site)
        
        elif _dtype.ismap():
            if  _attrib_name == "keys":
                #! check parameter count
                if  len(_node.get(1)) != 0:
                    error.raise_tracked(error_category.CompileError, "keys requires 0 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit elementtype
                push_ttable(self, array_t(_dtype.keytype))

                #! emit map keys
                emit_opcode(self, map_keys)
            
            elif _attrib_name == "values":
                #! check parameter count
                if  len(_node.get(1)) != 0:
                    error.raise_tracked(error_category.CompileError, "values requires 0 argument, got %d." % len(_node.get(1)), _node.site)
                
                #! emit elementtype
                push_ttable(self, array_t(_dtype.valtype))

                #! emit map values
                emit_opcode(self, map_values)
            
            else:
                error.raise_tracked(error_category.CompileError, "%s has no method %s." % (_dtype.repr(), _attrib_name), _node.site)

        else:
            error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _attrib_name), _node.site)

    def call_abstract_args(self, _node, _paramstype=[]):
        _index = 0

        #! check every arguments
        for _each_param in _node.get(1)[::-1]:

            #! visit param
            self.visit(_each_param)

            _typeN = self.tstack.popp()

            #! match type
            if  not _paramstype[::-1][_index][1].matches(_typeN):
                error.raise_tracked(error_category.CompileError, "parameter \"%s\" expects argument datatype %s, got %s." % (_paramstype[::-1][_index][0], _paramstype[::-1][_index][1].repr(), _typeN.repr()), _node.site)

            _index += 1
    
    def call_method_part(self, _node):
        #! datatype
        _functype = self.tstack.popp()

        #! check if callable
        if  not _functype.ismethod():
            error.raise_tracked(error_category.CompileError, "%s is not a method type." % _functype.repr(), _node.site)

        #! check parameter count
        if  _functype.paramcount != (len(_node.get(1)) + 1):
            error.raise_tracked(error_category.CompileError, "%s requires %d argument, got %d." % (_functype.repr(), _functype.paramcount, len(_node.get(1))), _node.site)

        #! emit return type
        push_ttable(self, _functype.returntype)

        _index = 0

        #! rotate until last
        emit_opcode(self, rot2)

        #! check every arguments
        for _each_param in _node.get(1)[::-1]:

            #! visit param
            self.visit(_each_param)

            _typeN = self.tstack.popp()

            #! match type
            if  not _functype.parameters[::-1][_index][1].matches(_typeN):
                error.raise_tracked(error_category.CompileError, "parameter \"%s\" expects argument datatype %s, got %s." % (_functype.parameters[::-1][_index][0], _functype.parameters[::-1][_index][1].repr(), _typeN.repr()), _node.site)

            _index += 1

            #! rotate until last
            emit_opcode(self, rot2)
        
        #! opcode
        emit_opcode(self, call_function, len(_node.get(1)) + 1, self.callid - 1)

    def call_part(self, _node):
        #! datatype
        _functype = self.tstack.popp()

        #! check if callable
        if  not (_functype.isfunction() or _functype.isnativefunction() or _functype.istype()):
            error.raise_tracked(error_category.CompileError, "%s is not a callable type." % _functype.repr(), _node.site)

        #! check parameter count
        if  _functype.paramcount != len(_node.get(1)):
            error.raise_tracked(error_category.CompileError, "%s requires %d argument, got %d." % (_functype.repr(), _functype.paramcount, len(_node.get(1))), _node.site)

        #! emit return type
        push_ttable(self, _functype.returntype)

        _index = 0

        #! check every arguments
        for _each_param in _node.get(1)[::-1]:

            #! visit param
            self.visit(_each_param)

            _typeN = self.tstack.popp()

            #! match type
            if  not _functype.parameters[::-1][_index][1].matches(_typeN):
                error.raise_tracked(error_category.CompileError, "parameter \"%s\" expects argument datatype %s, got %s." % (_functype.parameters[::-1][_index][0], _functype.parameters[::-1][_index][1].repr(), _typeN.repr()), _node.site)

            _index += 1
        
        #! opcode
        if  _functype.isnativefunction():
            #! emit
            emit_opcode(self, call_native, len(_node.get(1)), self.callid - 1)

        elif _functype.isfunction():
            #! emit
            emit_opcode(self, call_function, len(_node.get(1)), self.callid - 1)

        else:
            #! emit
            emit_opcode(self, call_type, len(_node.get(1)), self.callid - 1)

    def ast_ternary(self, _node):
        if  _node.get(0).type == ast_type.SHORTC_OP:
            if  _node.get(0).get(1) == "&&":
                self.ternary_logic_and(_node)

            else:
                self.ternary_logic_or(_node)

        else:
            self.ternary_using_normal_condition(_node)
    
    def ternary_logic_and(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical and(&&). both operands
        #! must evaluate to true.
        #! if any operand produces false, 
        #! then the condition is false.
        #! so jump to false value without evaluating lhs.
        _if_false__jump_to_false_val =\
        emit_opcode(self, pop_jump_if_false, TARGET)
    
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        _jump_to_false =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile true
        self.visit(_node.get(1))

        _truetype =\
        self.tstack.popp()

        #! jump to end
        _to_end =\
        emit_opcode(self, jump_to, TARGET)

        #! jump if true
        _if_false__jump_to_false_val[2] = get_byteoff(self)

        #! jump to false value
        _jump_to_false[2] = get_byteoff(self)

        #! compile false
        self.visit(_node.get(2))

        _falsetype =\
        self.tstack.popp()

        #! jumpto end ternary
        _to_end[2] = get_byteoff(self)

        if  _truetype.matches(_falsetype):
            push_ttable(self, _truetype)
        
        else:
            push_ttable(self, any_t())
    
    def ternary_logic_or(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical or(||), atleast 1 operand
        #! produces true to make the condition satisfiable.
        #! IF rhs produces true. do not evaluate lhs.
        _if_true__jump_to_true_val =\
        emit_opcode(self, pop_jump_if_true, TARGET)
    
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        _jump_to_false =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! jump if true
        _if_true__jump_to_true_val[2] = get_byteoff(self)

        #! compile true
        self.visit(_node.get(1))

        _truetype =\
        self.tstack.popp()

        #! jump to end
        _to_end =\
        emit_opcode(self, jump_to, TARGET)

        #! jump to false value
        _jump_to_false[2] = get_byteoff(self)

        #! compile false
        self.visit(_node.get(2))

        _falsetype =\
        self.tstack.popp()

        #! jumpto end ternary
        _to_end[2] = get_byteoff(self)

        if  _truetype.matches(_falsetype):
            push_ttable(self, _truetype)
        
        else:
            push_ttable(self, any_t())
    
    def ternary_using_normal_condition(self, _node):
        #! compile condition
        self.visit(_node.get(0))

        _condtype = self.tstack.popp()

        #! check
        if  not _condtype.isboolean():
            error.raise_tracked(error_category.CompileError, "ternary condition must be a boolean type, got %s." % _condtype.repr(), _node.get(0).site)

        #! opcode
        _jump =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile true
        self.visit(_node.get(1))

        _truetype =\
        self.tstack.popp()

        #! jump to end
        _to_end =\
        emit_opcode(self, jump_to, TARGET)

        _jump[2] = get_byteoff(self)

        #! compile false
        self.visit(_node.get(2))

        _falsetype =\
        self.tstack.popp()

        #! jumpto end ternary
        _to_end[2] = get_byteoff(self)

        if  _truetype.matches(_falsetype):
            push_ttable(self, _truetype)
        
        else:
            push_ttable(self, any_t())
    
    def ast_unary_op(self, _node):
        """
             $0   $1
            _op  _rhs
        """
        _eval =\
        self.try_eval_una_op(_node)

        if  _eval != ...:
            if  _eval[0].isint():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, iload, _eval[1])
            
            elif _eval[0].isfloat():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, fload, _eval[1])
            
            elif _eval[0].isstring():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, sload, _eval[1])

            elif _eval[0].isboolean():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, bload, _eval[1])

            else:
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, nload, _eval[1])
            
            return

        #! === NOT EVALUATED ===

        _op = _node.get(0)
        self.visit(_node.get(1)) # rhs

        _rhs = self.tstack.popp()

        #! default
        _operation = operation.op_error_t()

        if  _op == "~":
            #! op result
            _operation = _rhs.bitnot()

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, bit_not)
        
        elif _op == "!":
            #! op result
            _operation = _rhs.lognot()

            #! emit int type
            push_ttable(self, _operation)
        
            #! opcode
            emit_opcode(self, log_not)

        elif _op == "+":
            #! op result
            _operation = _rhs.pos()

            #! emit int|float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intpos)
            
            elif _operation.isfloat():
                emit_opcode(self, fltpos)

        
        elif _op == "-":
            #! op result
            _operation = _rhs.neg()

            #! emit int|float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intneg)
            
            elif _operation.isfloat():
                emit_opcode(self, fltneg)

        else:
            raise

        if  _operation.iserror():
            error.raise_tracked(error_category.CompileError, "sinvalid operation %s %s." % (_op, _rhs.repr()), _node.site)

    
    def ast_unary_typeof(self, _node):
        """
             $0    $1
            _op  _rhs
        """
        #! visit rhs
        self.visit(_node.get(1))
        
        #! datatypoe
        _dtype = self.tstack.popp()

        #! push str
        push_ttable(self, string_t())

        #! opcode
        emit_opcode(self, pop_top)

        #! push type as string
        emit_opcode(self, sload, _dtype.qualname())

    def ast_unary_unpack(self, _node):
        """
             $0    $1
            _op  _rhs
        """
        _op = _node.get(0)
        self.visit(_node.get(1)) # rhs

        _rhs = self.tstack.peek()

        #! default
        _operation = operation.op_error_t()

        if  _op == "*":
            #! op result
            _operation = _rhs.unpack()

            #! opcode
            emit_opcode(self, array_pushall)
        
        elif _op == "**":
            #! op result
            _operation = _rhs.unpack()

            #! opcode
            emit_opcode(self, map_merge)
        else:
            raise
        
        if  _operation.iserror():
            error.raise_tracked(error_category.CompileError, "cannot unpack %s." % _rhs.repr(), _node.site)


    def ast_binary_op(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        _eval =\
        self.try_eval_bin_op(_node)

        if  _eval != ...:
            if  _eval[0].isint():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, iload, _eval[1])
            
            elif _eval[0].isfloat():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, fload, _eval[1])
            
            elif _eval[0].isstring():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, sload, _eval[1])

            elif _eval[0].isboolean():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, bload, _eval[1])

            else:
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, nload, _eval[1])
            
            return

        #! === NOT EVALUATED ===

        _op = _node.get(1)
        
        #! visit rhs
        self.visit(_node.get(2))
        
        #! visit lhs
        self.visit(_node.get(0))

        _lhs = self.tstack.popp()
        _rhs = self.tstack.popp()

        #! default
        _operation = operation.op_error_t()

        if  _op == "^^":
            #! op result
            _operation = _lhs.pow(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intpow)

            elif _operation.isfloat():
                emit_opcode(self, fltpow)

        elif _op == "*":
            #! op result
            _operation = _lhs.mul(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intmul)

            elif _operation.isfloat():
                emit_opcode(self, fltmul)

        elif _op == "/":
            #! op result
            _operation = _lhs.div(_rhs)

            #! emit float type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, quotient)
            
        
        elif _op == "%":
            #! op result
            _operation = _lhs.mod(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intrem)

            elif _operation.isfloat():
                emit_opcode(self, fltrem)

        elif _op == "+":
            #! op result
            _operation = _lhs.add(_rhs)

            #! emit int|float|str type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intadd)

            elif _operation.isfloat():
                emit_opcode(self, fltadd)
            
            elif _operation.isstring():
                emit_opcode(self, concat)
            
            elif _operation.isarray():
                #! rotate array
                emit_opcode(self, rot2)

                #! push or extend opcode
                if  not _rhs.isarray():
                    emit_opcode(self, array_push)

                else:
                    emit_opcode(self, array_pushall)
            
            elif _operation.ismap():
                #! rotate array
                emit_opcode(self, rot2)

                emit_opcode(self, map_merge)
        
        elif _op == "-":
            #! op result
            _operation = _lhs.sub(_rhs)

            #! emit float type
            push_ttable(self, _operation)

            #! opcode
            if  _operation.isint():
                emit_opcode(self, intsub)

            elif _operation.isfloat():
                emit_opcode(self, fltsub)
        
        elif _op == "<<" or _op == ">>":
            #! op result
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, _operation)

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
            push_ttable(self, _operation)

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
            push_ttable(self, _operation)

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
            push_ttable(self, _operation)

            #! opcode
            if   _op == "&":
                emit_opcode(self, bitand)

            elif _op == "^":
                emit_opcode(self, bitxor)
            
            elif _op == "|":
                emit_opcode(self, bitor)

        else:
            raise

        if  _operation.iserror():
            error.raise_tracked(error_category.CompileError, "invalid operation %s %s %s." % (_lhs.repr(), _op, _rhs.repr()), _node.site)

    def ast_shortc_op(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        _eval =\
        self.try_eval_short_op(_node)
        
        if  _eval != ...:
            if  _eval[0].isint():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, iload, _eval[1])
            
            elif _eval[0].isfloat():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, fload, _eval[1])
            
            elif _eval[0].isstring():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, sload, _eval[1])

            elif _eval[0].isboolean():
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, bload, _eval[1])

            else:
                push_ttable(self, _eval[0])

                #! opcode
                emit_opcode(self, nload, _eval[1])
            
            return

        #! === NOT EVALUATED ===

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
        _rhs =\
        self.tstack.popp() 
        #! lhs
        _lhs =\
        self.tstack.popp()

        #! emit as any
        push_ttable(self, _lhs if _lhs.matches(_rhs) else any_t())

    def ast_simple_ass(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        #! right
        self.visit(_node.get(2))

        #! just use peek here, because assignment is an expression
        _rhstype = self.tstack.peek()

        _lhs = _node.get(0)

        if  _lhs.type == ast_type.REF:

            #! check if exist
            if  not self.symtbl.contains(_lhs.get(0)):
                error.raise_tracked(error_category.CompileError, "%s is not defined." % _lhs.get(0), _node.site)
            
            _info = self.symtbl.lookup(_lhs.get(0))

            if  _info.is_constant():
                error.raise_tracked(error_category.CompileError, "assignment of constant variable \"%s\"." % _lhs.get(0), _node.site)
            
            #! update datatype
            _info.datatype = _rhstype
        
            #! duplicate value
            emit_opcode(self, dup_top)

            #! opcode
            emit_opcode(self, store_global if _info.is_global() else store_local, _info.get_name(), _info.get_offset())
        
        elif _lhs.type == ast_type.ELEMENT:
            #! lhs[??] = rhs

            #! duplicate value
            emit_opcode(self, dup_top)

            #! compile element
            self.visit(_lhs.get(1))

            _element_type = self.tstack.popp()

            #! compile object
            self.visit(_lhs.get(0))

            _objtype = self.tstack.popp()

            #! check if subscriptable
            if  _objtype.isarray():
                #! verify index
                if  not _element_type.isint():
                    error.raise_tracked(error_category.CompileError, "array index should be int, got %s." % _element_type.repr(), _node.site)

                #! check if element type matches
                if  not _objtype.elementtype.matches(_rhstype):
                    error.raise_tracked(error_category.CompileError, "element type mismatch. expected %s, got %s." % (_objtype.elementtype.repr(), _rhstype.repr()), _node.site)

                #! opcode
                emit_opcode(self, array_set)
            
            elif _objtype.ismap():
                #! verify element key
                if  not _objtype.keytype.matches(_element_type):
                    error.raise_tracked(error_category.CompileError, "%s key should be %s, got %s." % (_objtype.repr(), _objtype.keytype.repr(), _element_type.repr()), _node.site)

                #! check if element type matches
                if  not _objtype.valtype.matches(_rhstype):
                    error.raise_tracked(error_category.CompileError, "value type mismatch for %s. expected %s, got %s." % (_objtype.repr(), _objtype.valtype.repr(), _rhstype.repr()), _node.site)

                #! opcode
                emit_opcode(self, map_set)
            
            elif _objtype.isstring():
                #! verify index
                if  not _element_type.isint():
                    error.raise_tracked(error_category.CompileError, "string index should be int, got %s." % _element_type.repr(), _node.site)
                
                #! 
                error.raise_tracked(error_category.CompileError, "string element can't be re-assigned.", _node.site)

            else:
                error.raise_tracked(error_category.CompileError, "%s is not subscriptable." % _objtype.repr(), _node.site)

        elif _lhs.type == ast_type.ATTRIBUTE:
            #! lhs.attrib

            #! duplicate value
            emit_opcode(self, dup_top)

            #! visit object
            self.visit(_lhs.get(0))

            #! type
            _dtype = self.tstack.popp()

            if  _dtype.isinstance():

                if  not self.symtbl.contains(_dtype.repr()):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)

                #! structtable
                _info = self.symtbl.lookup(_dtype.repr())

                _type = _info.get_datatype()

                if  not _type.istype():
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)
                
                if  not (_type.hasAttribute(_lhs.get(1)) or _type.hasMethod(_lhs.get(1))):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)

                _attrib_or_method_type = _type.getAttribute(_lhs.get(1)) if _type.hasAttribute(_lhs.get(1)) else _type.getMethod(_lhs.get(1))

                if  _attrib_or_method_type.ismethod():
                    #! for error
                    error.raise_tracked(error_category.CompileError, "%s method \"%s\" can't be re-assigned." % (_dtype.repr(), _lhs.get(1)), _node.site)

                else:
                    if  not _attrib_or_method_type.matches(_rhstype):
                        error.raise_tracked(error_category.CompileError, "%s.%s requires %s, got %s." % (_dtype.repr(), _lhs.get(1), _attrib_or_method_type.repr(), _rhstype.repr()), _node.site)

                    #! push attribute as string
                    emit_opcode(self, sload, _lhs.get(1))

                    #! set
                    emit_opcode(self, set_attribute)
            

            elif _dtype.ismodule():
                #! check
                if  not _dtype.hasAttribute(_lhs.get(1)):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _lhs.get(1)), _node.site)

                #! end
                error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _lhs.get(1)), _node.site)

            elif _dtype.isarray():
                #! pop array
                emit_opcode(self, pop_top)

                #! emit attribute type as str
                push_ttable(self, string_t())

                _vattrib = _node.get(0).get(1)

                if  _vattrib in ("push", "pop", "peek", "size"):
                    #! emit error
                    error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _vattrib), _node.site)
                
                else:
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _vattrib), _node.site)
            
            elif _dtype.ismap():
                #! pop array
                emit_opcode(self, pop_top)

                #! emit attribute type as str
                push_ttable(self, string_t())

                _vattrib = _node.get(0).get(1)

                if  _vattrib in ("keys", "values"):
                    #! emit error
                    error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _vattrib), _node.site)
                
                else:
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _vattrib), _node.site)

            else:
                error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _lhs.get(1)), _node.site)

#! TODO: simplify simple_assignment and augmented assignment.!!!!!!

    def ast_augment_ass(self, _node):
        """
             $0    $1   $2
            _lhs  _op  _rhs
        """
        _op = _node.get(1)

        #! right
        self.visit(_node.get(2))

        #! left
        self.visit(_node.get(0))

        _lhs = self.tstack.popp()
        _rhs = self.tstack.popp()

        #! default
        _operation = operation.op_error_t()

        if  _op == "^^=":
            _operation = _lhs.pow(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            if  _operation.isint():
                #! opcode
                emit_opcode(self, intpow)

            elif _operation.isfloat():
                #! opcode
                emit_opcode(self, fltpow)
        
        elif _op == "*=":
            _operation = _lhs.mul(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            if  _operation.isint():
                #! opcode
                emit_opcode(self, intmul)

            elif _operation.isfloat():
                #! opcode
                emit_opcode(self, fltmul)
        
        elif _op == "/=":
            _operation = _lhs.div(_rhs)

            emit_opcode(self, quotient)
        
        elif _op == "%=":
            _operation = _lhs.mod(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            if  _operation.isint():
                #! opcode
                emit_opcode(self, intrem)

            elif _operation.isfloat():
                #! opcode
                emit_opcode(self, fltrem)
        
        elif _op == "+=":
            _operation = _lhs.add(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            if  _operation.isint():
                #! opcode
                emit_opcode(self, intadd)

            elif _operation.isfloat():
                #! opcode
                emit_opcode(self, fltadd)
            
            elif _operation.isstring():
                #! opcode
                emit_opcode(self, concat)

            elif _operation.isarray():
                #! rotate array
                emit_opcode(self, rot2)

                #! push or extend opcode
                if  not _rhs.isarray():
                    emit_opcode(self, array_push)

                else:
                    emit_opcode(self, array_pushall)
            
            elif _operation.ismap():
                #! rotate array
                emit_opcode(self, rot2)

                emit_opcode(self, map_merge)
        
        elif _op == "-=":
            _operation = _lhs.sub(_rhs)

            #! emit int|float type
            push_ttable(self, _operation)

            if  _operation.isint():
                #! opcode
                emit_opcode(self, intsub)

            elif _operation.isfloat():
                #! opcode
                emit_opcode(self, fltsub)
        
        elif _op == "<<=":
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, lshift)

        elif _op == ">>=":
            _operation = _lhs.shift(_rhs)

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, rshift)
        
        elif _op == "&":
            _operation = _lhs.bitwise(_rhs)

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, bitand)
        
        elif _op == "^":
            _operation = _lhs.bitwise(_rhs)

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, bitxor)
        
        elif _op == "|":
            _operation = _lhs.bitwise(_rhs)

            #! emit int type
            push_ttable(self, _operation)

            #! opcode
            emit_opcode(self, bitor)
        
        if  _operation.iserror():
            error.raise_tracked(error_category.CompileError, "invalid operation %s %s %s." % (_lhs.repr(), _op, _rhs.repr()), _node.site)

        _lhs = _node.get(0)
        _rhs = self.tstack.peek()

        if  _lhs.type == ast_type.REF:

            #! check if exist
            if  not self.symtbl.contains(_lhs.get(0)):
                error.raise_tracked(error_category.CompileError, "%s is not defined." % _lhs.get(0), _node.site)
            
            _info = self.symtbl.lookup(_lhs.get(0))

            if  _info.is_constant():
                error.raise_tracked(error_category.CompileError, "assignment of constant variable \"%s\"." % _lhs.get(0), _node.site)
            
            #! update datatype
            _info.datatype = _rhs
        
            #! duplicate value
            emit_opcode(self, dup_top)

            #! opcode
            emit_opcode(self, store_global if _info.is_global() else store_local, _info.get_name(), _info.get_offset())
        
        elif _lhs.type == ast_type.ELEMENT:
            #! lhs[??] = rhs

            #! duplicate value
            emit_opcode(self, dup_top)

            #! compile element
            self.visit(_lhs.get(1))

            _element_type = self.tstack.popp()

            #! compile object
            self.visit(_lhs.get(0))

            _objtype = self.tstack.popp()

            #! check if subscriptable
            if  _objtype.isarray():
                #! verify index
                if  not _element_type.isint():
                    error.raise_tracked(error_category.CompileError, "array index should be int, got %s." % _element_type.repr(), _node.site)

                #! check if element type matches
                if  not _objtype.elementtype.matches(_rhs):
                    error.raise_tracked(error_category.CompileError, "element type mismatch. expected %s, got %s." % (_objtype.elementtype.repr(), _rhs.repr()), _node.site)

                #! opcode
                emit_opcode(self, array_set)
            
            elif _objtype.ismap():
                #! verify element key
                if  not _objtype.keytype.matches(_element_type):
                    error.raise_tracked(error_category.CompileError, "%s key should be %s, got %s." % (_objtype.repr(), _objtype.keytype.repr(), _element_type.repr()), _node.site)

                #! check if element type matches
                if  not _objtype.valtype.matches(_rhs):
                    error.raise_tracked(error_category.CompileError, "value type mismatch for %s. expected %s, got %s." % (_objtype.repr(), _objtype.valtype.repr(), _rhs.repr()), _node.site)

                #! opcode
                emit_opcode(self, map_set)
            
            elif _objtype.isstring():
                #! verify index
                if  not _element_type.isint():
                    error.raise_tracked(error_category.CompileError, "string index should be int, got %s." % _element_type.repr(), _node.site)
                
                #! 
                error.raise_tracked(error_category.CompileError, "string element can't be re-assigned.", _node.site)

            else:
                error.raise_tracked(error_category.CompileError, "%s is not subscriptable." % _objtype.repr(), _node.site)

        elif _lhs.type == ast_type.ATTRIBUTE:
            #! lhs.attrib

            #! duplicate value
            emit_opcode(self, dup_top)

            #! visit object
            self.visit(_lhs.get(0))

            #! type
            _dtype = self.tstack.popp()

            if  _dtype.isinstance():

                if  not self.symtbl.contains(_dtype.repr()):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)

                #! structtable
                _info = self.symtbl.lookup(_dtype.repr())

                _type = _info.get_datatype()

                if  not _type.istype():
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)
                
                if  not _type.hasAttribute(_lhs.get(1)):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute %s." % (_dtype.repr(), _lhs.get(1)), _node.site)
                
                _attrib_or_method_type = _type.getAttribute(_lhs.get(1)) if _type.hasAttribute(_lhs.get(1)) else _type.getMethod(_lhs.get(1))

                if  _attrib_or_method_type.ismethod():
                    #! for error
                    error.raise_tracked(error_category.CompileError, "%s method \"%s\" can't be re-assigned." % (_dtype.repr(), _lhs.get(1)), _node.site)

                else:
                    if  not _attrib_or_method_type.matches(_rhs):
                        error.raise_tracked(error_category.CompileError, "%s.%s requires %s, got %s." % (_dtype.repr(), _lhs.get(1), _attrib_or_method_type.repr(), _rhs.repr()), _node.site)

                    #! push attribute as string
                    emit_opcode(self, sload, _lhs.get(1))

                    #! set
                    emit_opcode(self, set_attribute)

            elif _dtype.ismodule():
                #! check
                if  not _dtype.hasAttribute(_lhs.get(1)):
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _lhs.get(1)), _node.site)

                #! end
                error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _lhs.get(1)), _node.site)

            elif _dtype.isarray():
                #! pop array
                emit_opcode(self, pop_top)

                #! emit attribute type as str
                push_ttable(self, string_t())

                _vattrib = _node.get(0).get(1)

                if  _vattrib in ("push", "pop", "peek", "size"):
                    #! emit error
                    error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _vattrib), _node.site)
                
                else:
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _vattrib), _node.site)
            
            elif _dtype.ismap():
                #! pop array
                emit_opcode(self, pop_top)

                #! emit attribute type as str
                push_ttable(self, string_t())

                _vattrib = _node.get(0).get(1)

                if  _vattrib in ("keys", "values"):
                    #! emit error
                    error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _vattrib), _node.site)
                
                else:
                    error.raise_tracked(error_category.CompileError, "%s has no attribute \"%s\"." % (_dtype.repr(), _vattrib), _node.site)
            
            else:
                error.raise_tracked(error_category.CompileError, "%s attribute \"%s\" can't be re-assigned." % (_dtype.repr(), _lhs.get(1)), _node.site)

    #! ========== compound statement ==========

    def ast_struct(self, _node):
        """    
               $0      $1
            subtypes  body
        """
        _old_offset = self.offset
        _old_bcodes = self.bcodes

        for _each_subtype in _node.get(0):

            #! check if function|struct name is already defined.
            # if  self.symtbl.contains(_each_subtype):
            #     error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_subtype, _node.site)
         
            self.offset = 0
            self.bcodes = []

            #! make scope
            self.symtbl.newscope()

            _members = []

            if  len(_node.get(1)) <= 0:
                error.raise_tracked(error_category.CompileError, "struct \"%s\" has empty body." %  _each_subtype, _node.site)

            for _each_member in _node.get(1):

                #! visit type
                self.visit(_each_member[1])

                _dtype = self.tstack.popp()

                #! check if parameter is already defined.
                if  self.symtbl.haslocal(_each_member[0]):
                    error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_member[0], _node.site)

                #! insert
                _members.append((_each_member[0], _dtype))

                #! opcode
                emit_opcode(self, store_fast, _each_member[0], self.offset)

                #! register
                self.symtbl.insert_var(_each_member[0], self.offset, _dtype, False, False, _node.site)

                self.offset += 1
                #! end

            for _each_member in _node.get(1)[::-1]:
                
                _info = self.symtbl.lookup(_each_member[0])

                #! val
                emit_opcode(self, load_local, _each_member[0], _info.get_offset())

                #! key
                emit_opcode(self, sload, _each_member[0])
        
            #! make aobject
            emit_opcode(self, make_aobject, _each_subtype, len(_members))

            #! add return
            emit_opcode(self, return_control)

            #! leave scope
            self.symtbl.endscope()

            #! store code
            self.state.codes[self.names[-1]][_each_subtype] = self.bcodes

            #! restore
            self.offset = _old_offset
            self.bcodes = _old_bcodes
            
            #! struct becomes a function
            #! _type = type_t(self.currentstructnumber, _each_subtype, instance_t(self.currentstructnumber, _each_subtype), len(_members), tuple(_members))

            #! register
            # TODO: watchout!!
            #! self.symtbl.insert_struct(_each_subtype, self.offset, _type, _node.site)

            #! val opcode
            emit_opcode(self, load_typepntr, self.names[-1], _each_subtype)

            #! var opcode
            emit_opcode(self, store_global, _each_subtype, self.offset)

            #! end
            self.offset += 1
            _old_offset  = self.offset

        #! increment every struct dec
        self.currentstructnumber += 1
    
    def ast_implements(self, _node):
        """
              $0   $1
            _name _body
        """
        _name = _node.get(0)

        self.symtbl.newscope()
        self.names.append(_name)

        #! check if type exist
        if  not self.symtbl.contains(_name):
            error.raise_tracked(error_category.CompileError, "type %s is not defined." % _name, _node.site)
        
        _typeinfo = self.symtbl.lookup(_node.get(0))

        if  not _typeinfo.get_datatype().istype():
            error.raise_tracked(error_category.CompileError, "name %s is not a type." % _name, _node.site)
        
        #! compile
        for _each_method in _node.get(1):
            self.visit(_each_method)

        self.names.pop()
        _symbols =\
        self.symtbl.endscope()

        #! unpack content globally
        for _each_symbol in _symbols.aslist():
            self.symtbl.insert_fun(_each_symbol[0], _each_symbol[1].get_offset(), _each_symbol[1].get_datatype(), _each_symbol[1].get_returntype(), _each_symbol[1].get_site())

    def ast_method(self, _node):
        """    
               $0        $1    $2      $3        $4
            returntype  name  self  parameters  body
        """
        _old_offset = self.offset
        _old_bcodes = self.bcodes

        self.offset = 0
        self.bcodes = []

        #! =======================
        _parameters = []

        #! visit returntype
        self.visit(_node.get(0))

        #! set current function
        self.currentfunctiontype =\
        self.tstack.popp()

        #! new func scope
        self.symtbl.newscope()

        #! check if function name is already defined.
        # if  self.symtbl.contains(_node.get(1)):
        #     error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(1), _node.site)

        _typeinfo = self.symtbl.lookup(self.names[-1])

        #! mark as instance
        _selftype = instance_t(_typeinfo.get_datatype().typenumber, _typeinfo.get_datatype().typename)

        #! as param
        _parameters.append((_node.get(2), _selftype))

        #! emit 
        emit_opcode(self, store_fast, _node.get(2), self.offset)

        #! register
        self.symtbl.insert_var(_node.get(2), self.offset, _selftype, False, False, _node.site)

        self.offset += 1

        #! compile parameters
        for _each_param in _node.get(3):

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
            self.symtbl.insert_var(_each_param[0], self.offset, _vtype, False, False, _node.site)

            self.offset += 1
            #! end

        #! compile body
        for _each_child in _node.get(4):

            #! check
            if  _each_child.type == ast_type.RETURN_STMNT:
                self.functionhasreturntype = True
           
            #! visit child
            self.visit(_each_child)
        
        if  not self.functionhasreturntype and not self.currentfunctiontype.matches(null_t()):
            error.raise_tracked(error_category.CompileError, "function \"%s\" has no visible return." %  _node.get(1), _node.site)

        if  self.currentfunctiontype.matches(null_t()):
            #! emit virtual null
            emit_opcode(self, nload, None)

            #! add return
            emit_opcode(self, return_control)

        #! end func scope
        self.symtbl.endscope()

        #! store code
        self.state.codes[self.names[-2]][_node.get(1)] = self.bcodes

        #! restore
        self.offset = _old_offset
        self.bcodes = _old_bcodes

        #! final: Type.function
        _finalname = self.names[-1] + "." + _node.get(1)

        #! register
        self.symtbl.insert_fun(_finalname, self.offset, method_t(self.currentfunctiontype, len(_parameters), _parameters), self.currentfunctiontype, _node.site)

        #! unset current function
        self.currentfunctiontype =\
        None
        
        #! val opcode
        emit_opcode(self, load_funpntr, self.names[-2], _node.get(1))

        #! var opcode
        emit_opcode(self, store_global, _node.get(1), self.offset)

        #! end
        self.offset += 1

    def ast_function(self, _node):
        """    
               $0        $1       $2       $3
            returntype  name  parameters  body
        """
        _old_offset = self.offset
        _old_bcodes = self.bcodes

        self.offset = 0
        self.bcodes = []

        #! =======================
        _parameters = []

        #! visit returntype
        self.visit(_node.get(0))

        #! set current function
        self.currentfunctiontype =\
        self.tstack.popp()

        #! new func scope
        self.symtbl.newscope()

        #! check if function name is already defined.
        # if  self.symtbl.contains(_node.get(1)):
        #     error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(1), _node.site)

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
            self.symtbl.insert_var(_each_param[0], self.offset, _vtype, False, False, _node.site)

            self.offset += 1
            #! end

        #! compile body
        for _each_child in _node.get(3):

            #! check
            if  _each_child.type == ast_type.RETURN_STMNT:
                self.functionhasreturntype = True
           
            #! visit child
            self.visit(_each_child)
        
        if  not self.functionhasreturntype and not self.currentfunctiontype.matches(null_t()):
            error.raise_tracked(error_category.CompileError, "function \"%s\" has no visible return." %  _node.get(1), _node.site)

        if  self.currentfunctiontype.matches(null_t()):
            #! emit virtual null
            emit_opcode(self, nload, None)

            #! add return
            emit_opcode(self, return_control)

        #! end func scope
        self.symtbl.endscope()

        #! store code
        self.state.codes[self.names[-1]][_node.get(1)] = self.bcodes

        #! restore
        self.offset = _old_offset
        self.bcodes = _old_bcodes

        #! register
        self.symtbl.insert_fun(_node.get(1), self.offset, fn_t(self.currentfunctiontype, len(_parameters), _parameters), self.currentfunctiontype, _node.site)

        #! unset current function
        self.currentfunctiontype =\
        None
        
        #! val opcode
        emit_opcode(self, load_funpntr, self.names[-1], _node.get(1))

        #! var opcode
        emit_opcode(self, store_global, _node.get(1), self.offset)

        #! end
        self.offset += 1

    def ast_enum(self, _node):
        """    
               $0      $1
            subtypes  body
        """
        if  self.symtbl.contains(_node.get(0)):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(0), _node.site)

        #! new scope
        self.symtbl.newscope()

        _type = None

        _member = []
        _virtual_offset = int(self.offset)
        for _each_member in _node.get(1)[::-1]:
            #! visit value
            self.visit(_each_member[1])

            _current = self.tstack.popp()

            _type = _current if not _type else _type

            if  self.symtbl.haslocal(_each_member[0]):
                error.raise_tracked(error_category.CompileError, "an enum member \"%s\" has already been decalaired." % _each_member[0], _node.site);
            
            if  not _type.matches(_current):
                error.raise_tracked(error_category.CompileError, "enum value data types are not unique.", _node.site)

            _member.append((_each_member[0], _type))

            #! make member as string
            emit_opcode(self, sload, _each_member[0])

            #! register
            self.symtbl.insert_var(_each_member[0], _virtual_offset, _type, False, False, _node.site)

            #! end
            _virtual_offset += 1
        
        #! build enum
        emit_opcode(self, build_enum, _node.get(0), len(_node.get(1)))

        #! store enum
        emit_opcode(self, store_global, _node.get(0), self.offset)

        #! end scope
        self.symtbl.endscope()
        
        #! register
        self.symtbl.insert_enum(_node.get(0), self.offset, enum_t(_type, tuple(_member)), _node.site)

        #!end
        self.offset += 1
        
    def ast_if_stmnt(self, _node):
        """ 
               $0        $1        $2
            condition  statement  else
        """
        if  _node.get(0).type == ast_type.SHORTC_OP:
            #! check op
            if  _node.get(0).get(1) == "&&":
                self.if_logic_and(_node)
            else:
                self.if_logic_or(_node)
        else:
            self.if_using_normal_condition(_node)
    
    def if_logic_and(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical and(&&). both operands
        #! must evaluate to true.
        #! if any operand produces false, 
        #! then the condition is false.
        #! so jump to else|endif without evaluating lhs.
        _if_false__jump_to_else_or_endif =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to else
        _to_else =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! compile statement
        self.visit(_node.get(1))

        #! NOTE: body|statement does not emit type, so do not pop.
        
        _jump_to_end = ...

        #! jump to end if has else
        if  _node.get(2):
            _jump_to_end =\
            emit_opcode(self, jump_to, TARGET)

        #! IF FALSE
        _if_false__jump_to_else_or_endif[2] = get_byteoff(self)
        _to_else[2] = get_byteoff(self)

        #! compile if has else
        if  _node.get(2):
            self.visit(_node.get(2))

            #! NOTE: body|statement does not emit type, so do not pop.

        #! END IF
        if  _node.get(2):
            _jump_to_end[2] = get_byteoff(self)

    def if_logic_or(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical or(||), atleast 1 operand
        #! produces true to make the condition satisfiable.
        #! IF rhs produces true. do not evaluate lhs.
        _if_true__jump_to_statement =\
        emit_opcode(self, pop_jump_if_true, TARGET)
        
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to else
        _to_else =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! if rhs true
        _if_true__jump_to_statement[2] = get_byteoff(self)
        
        #! compile statement
        self.visit(_node.get(1))

        #! NOTE: body|statement does not emit type, so do not pop.
        
        _jump_to_end = ...

        #! jump to end if has else
        if  _node.get(2):
            _jump_to_end =\
            emit_opcode(self, jump_to, TARGET)

        #! IF FALSE
        _to_else[2] = get_byteoff(self)

        #! compile if has else
        if  _node.get(2):
            self.visit(_node.get(2))

            #! NOTE: body|statement does not emit type, so do not pop.

        #! END IF
        if  _node.get(2):
            _jump_to_end[2] = get_byteoff(self)

    def if_using_normal_condition(self, _node):
        """ If statement that uses normal expression.
        """

        #! compile condition
        self.visit(_node.get(0))

        _cond = self.tstack.popp()

        #! check condition
        if  not _cond.isboolean():
            error.raise_tracked(error_category.CompileError, "if condition must be a boolean type, got %s." % _cond.repr(), _node.get(0).site)

        _jump_to_else =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile statement
        self.visit(_node.get(1))

        _jump_to_end = ...

        #! jump to end if has else
        if  _node.get(2):
            _jump_to_end =\
            emit_opcode(self, jump_to, TARGET)

        #! jump to else or end if
        _jump_to_else[2] = get_byteoff(self)
        
        #! compile if has else
        if  _node.get(2):
            self.visit(_node.get(2))

        #! END IF
        if  _node.get(2):
            _jump_to_end[2] = get_byteoff(self)

    def ast_switch_stmnt(self, _node):
        """ 
               $0       $1
            condition  body
        """
        _to_end_switch = []

        #! compile condition
        self.visit(_node.get(0))

        #! cond dtype
        _condtype = self.tstack.popp()

        if  _condtype.isany():
            error.raise_tracked(error_category.CompileError, "type of switch condition can't be unknown at compile time.", _node.get(0).site)

        _cases = _node.get(1)[0]

        for _case in _cases:
            
            _to_case_satement = []

            for _each_expr in _case[0]:
                #! duplicate switch condition
                emit_opcode(self, dup_top)

                #! compile each case expression
                self.visit(_each_expr)

                #! opcode
                if  _condtype.isint():
                    emit_opcode(self, equal_i)

                elif _condtype.isfloat():
                    emit_opcode(self, equal_f)
                
                elif _condtype.isstring():
                    emit_opcode(self, equal_s)
                
                elif _condtype.isboolean():
                    emit_opcode(self, equal_b)
                
                elif _condtype.isnull():
                    emit_opcode(self, equal_n)
                
                else:
                    emit_opcode(self, addressof)

                _expr_type = self.tstack.popp()

                #! add jump
                _to_case_satement.append(
                    emit_opcode(self, pop_jump_if_true, TARGET))

                if  not _condtype.matches(_expr_type):
                    error.raise_tracked(error_category.CompileError, "case expression does not match switch condition switch(%s) != case ..., ..., %s:." % (_condtype.repr(), _expr_type.repr()), _each_expr.site)
            
            #! jump to next case
            _next_case =\
            emit_opcode(self, jump_to, TARGET)

            for _idx in range(len(_to_case_satement)):
                #! jump here if match found
                _to_case_satement[_idx][2] = get_byteoff(self)
                
            #! compile case statement
            self.visit(_case[1])

            #! NOTE: body|statement does not emit type, so do not pop.

            #! jump to end
            _to_end_switch.append(
                emit_opcode(self, jump_to, TARGET))
            
            #! next case
            _next_case[2] = get_byteoff(self)

        #! compile if has else
        if  _node.get(1)[1]:
            self.visit(_node.get(1)[1])
        
        for _idx in range(len(_to_end_switch)):
            #! jump here after case statement executed.
            _to_end_switch[_idx][2] = get_byteoff(self)

        #! pop switch condition
        emit_opcode(self, pop_top)
    
    def ast_for_stmnt(self, _node):
        """
              $0    $1    $2    $3
            _init _cond _mutt _stmnt
        """
        if  _node.get(1):
            #! check op
            if  _node.get(1).get(1) == "&&":
                self.for_logic_and(_node)
                return
            elif _node.get(1).get(1) == "||":
                self.for_logic_or(_node)
                return
        
        #! end
        self.for_using_regular_condition(_node)
    
    def for_logic_and(self, _node):
        """ For using logical and.
        """
        #! if has init
        if  _node.get(0):
            #! compile initialize
            self.visit(_node.get(0))

            #! ignore type
            self.tstack.popp()

            #! pop initialize
            emit_opcode(self, pop_top)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! && operator
        _op = _node.get(1).get(1)

        #! compile rhs
        self.visit(_node.get(1).get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be a boolean type, got %s." % (_op, _rhs_type.repr()), _node.get(1).site)

        _if_false__jump_to_endfor =\
        emit_opcode(self, pop_jump_if_false, TARGET)


        #! compile lhs
        self.visit(_node.get(1).get(0))

        _lhs_type = self.tstack.popp()

        #! check rhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _node.get(1).site)

        _to_endfor =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile stmnt|body
        self.visit(_node.get(3))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! if has mutation
        if  _node.get(2):
            #! compile mutation
            self.visit(_node.get(2))

            #! ignore type
            self.tstack.popp()

            #! pop mutation
            emit_opcode(self, pop_top)

        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END FOR
        _if_false__jump_to_endfor[2] = get_byteoff(self)
        _to_endfor[2] = get_byteoff(self)
        
        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def for_logic_or(self, _node):
        """ For using logical or.
        """
        #! if has init
        if  _node.get(0):
            #! compile initialize
            self.visit(_node.get(0))

            #! ignore type
            self.tstack.popp()

            #! pop initialize
            emit_opcode(self, pop_top)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! && operator
        _op = _node.get(1).get(1)

        #! compile rhs
        self.visit(_node.get(1).get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be a boolean type, got %s." % (_op, _rhs_type.repr()), _node.get(1).site)

        _if_true__jump_to_statement =\
        emit_opcode(self, pop_jump_if_true, TARGET)


        #! compile lhs
        self.visit(_node.get(1).get(0))

        _lhs_type = self.tstack.popp()

        #! check rhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _node.get(1).site)

        _to_endfor =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! jump here!
        _if_true__jump_to_statement[2] = get_byteoff(self)

        #! compile stmnt|body
        self.visit(_node.get(3))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! if has mutation
        if  _node.get(2):
            #! compile mutation
            self.visit(_node.get(2))

            #! ignore type
            self.tstack.popp()

            #! pop mutation
            emit_opcode(self, pop_top)

        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END FOR
        _to_endfor[2] = get_byteoff(self)
        
        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()

    def for_using_regular_condition(self, _node):
        #! if has init
        if  _node.get(0):
            #! compile initialize
            self.visit(_node.get(0))

            #! ignore type
            self.tstack.popp()

            #! pop initialize
            emit_opcode(self, pop_top)

        _loop_begin = get_byteoff(self)
        _jump_to_end_for = ...


        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! if has condition
        if  _node.get(1):
            #! compile condition
            self.visit(_node.get(1))

            _condtype = self.tstack.popp()

            #! check if boolean
            if  not _condtype.isboolean():
                error.raise_tracked(error_category.CompileError, "for condition must be a boolean type, got %s." % _condtype.repr(), _node.get(1).site)

            _jump_to_end_for =\
            emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile stmnt|body
        self.visit(_node.get(3))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! if has mutation
        if  _node.get(2):
            #! compile mutation
            self.visit(_node.get(2))

            #! ignore type
            self.tstack.popp()

            #! pop mutation
            emit_opcode(self, pop_top)

        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END FOR
        if  _node.get(1):
            _jump_to_end_for[2] = get_byteoff(self)
        
        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def ast_while_stmnt(self, _node):
        """   
              $0    $1
            _cond _body
        """
        if  _node.get(0).type == ast_type.SHORTC_OP:
            if  _node.get(0).get(1) == "&&":
                self.while_logic_and(_node)
            else:
                self.while_logic_or(_node)
        else:
            self.while_using_normal_condition(_node)
    
    def while_logic_and(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical and(&&). both operands
        #! must evaluate to true.
        #! if any operand produces false, 
        #! then the condition is false.
        #! so jump to end while without evaluating lhs.
        _if_false__jump_to_endwhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to end while
        _to_endwhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! compile statement
        self.visit(_node.get(1))

        #! NOTE: body|statement does not emit type, so do not pop.
        
        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END WHILE
        _if_false__jump_to_endwhile[2] = get_byteoff(self)
        _to_endwhile[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def while_logic_or(self, _node):
        _condition = _node.get(0)
        _op = _condition.get(1)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

       
        #! when logical or(||), atleast 1 operand
        #! produces true to make the condition satisfiable.
        #! IF rhs produces true. do not evaluate lhs.
        _if_true__jump_to_statement =\
        emit_opcode(self, pop_jump_if_true, TARGET)
    
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to end while
        _to_endwhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! jump here!
        _if_true__jump_to_statement[2] = get_byteoff(self)

        #! compile statement
        self.visit(_node.get(1))

        #! NOTE: body|statement does not emit type, so do not pop.
        
        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END WHILE
        _to_endwhile[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
 
    def while_using_normal_condition(self, _node):
        """ While using normal expression.
        """

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile condition
        self.visit(_node.get(0))

        _type = self.tstack.popp()

        #! check type
        if  not _type.isboolean():
            error.raise_tracked(error_category.CompileError, "while condition must be a boolean type, got %s." % _type.repr(), _node.get(0).site)

        _if_false__jump_to_end =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! compile body
        self.visit(_node.get(1))

        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END WHILE
        _if_false__jump_to_end[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def ast_dowhile_stmnt(self, _node):
        """  
              $0    $1
            _body _cond
        """
        if  _node.get(1).type == ast_type.SHORTC_OP:
            #! check op
            if  _node.get(1).get(1) == "&&":
                self.dowhile_logic_and(_node)

            else:
                self.dowhile_logic_or(_node)
        else:
            self.dowhile_using_normal_condition(_node)
    
    def dowhile_logic_and(self, _node):
        _condition = _node.get(1)
        _op = _condition.get(1)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile body
        self.visit(_node.get(0))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical and(&&). both operands
        #! must evaluate to true.
        #! if any operand produces false, 
        #! then the condition is false.
        #! so jump to end do while without evaluating lhs.
        _if_false__jump_to_enddowhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to end do while
        _to_enddowhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! jumpto begin loop
        emit_opcode(self, jump_to, _loop_begin)

        #! END DO WHILE
        _if_false__jump_to_enddowhile[2] = get_byteoff(self)
        _to_enddowhile[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def dowhile_logic_or(self, _node):
        _condition = _node.get(1)
        _op = _condition.get(1)

        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile body
        self.visit(_node.get(0))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! compile rhs
        self.visit(_condition.get(2))

        _rhs_type = self.tstack.popp()

        #! check rhs type
        if  not _rhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "right operand for op \"%s\" must be boolean type, got %s." % (_op, _rhs_type.repr()), _condition.site)

        #! when logical and(&&). both operands
        #! must evaluate to true.
        #! if any operand produces false, 
        #! then the condition is false.
        #! so jump to end do while without evaluating lhs.
        emit_opcode(self, pop_jump_if_true, _loop_begin)
        
        #! compile lhs
        self.visit(_condition.get(0))

        _lhs_type = self.tstack.popp()

        #! check lhs type
        if  not _lhs_type.isboolean():
            error.raise_tracked(error_category.CompileError, "left operand for op \"%s\" must be a boolean type, got %s." % (_op, _lhs_type.repr()), _condition.site)

        #! if lhs evaluates to false for
        #! both operand. jump to end do while
        _to_enddowhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)
        
        #! jumpto begin loop
        emit_opcode(self, jump_to, _loop_begin)

        #! END DO WHILE
        _to_enddowhile[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()
    
    def dowhile_using_normal_condition(self, _node):
        _loop_begin = get_byteoff(self)

        #! init starts and breaks
        _breaks = []
        self.loops .append(_loop_begin)
        self.breaks.append(_breaks)

        #! compile body
        self.visit(_node.get(0))

        #! NOTE: body|statement does not emit type, so do not pop.

        #! compile condition 
        self.visit(_node.get(1))

        _type = self.tstack.popp()

        #! check type
        if  not _type.isboolean():
            error.raise_tracked(error_category.CompileError, "while condition must be a boolean type, got %s." % _type.repr(), _node.get(1).site)

        _if_false__jump_to_enddowhile =\
        emit_opcode(self, pop_jump_if_false, TARGET)

        #! jumpto loop begin
        emit_opcode(self, jump_to, _loop_begin)

        #! END DO WHILE
        _if_false__jump_to_enddowhile[2] = get_byteoff(self)

        #! remove loop start
        self.loops.pop()

        #! jump here
        for _each_brk in _breaks:
            #! set target here!
            _each_brk[2] = get_byteoff(self)

        #! remove local break
        self.breaks.pop()

    def ast_block_stmnt(self, _node):
        """   $0
            _body
        """
        self.symtbl.newscope()
        
        for _each_node in _node.get(0):
            #! compile node
            self.visit(_each_node)

            #! NOTE: body|statement does not emit type, so do not pop.

        self.symtbl.endscope()

    #! =========== simple statement ===========

    def ast_function_wrapper(self, _node):
        """    
                $0        $1          $2          $3     $4
            returntype  wraptype  wrapper_name  params  return
        """
        _old_offset = self.offset
        _old_bcodes = self.bcodes

        self.offset = 0
        self.bcodes = []

        #! =======================
        _parameters = []

        #! new func scope
        self.symtbl.newscope()

        #! visit return type
        self.visit(_node.get(0))

        _desiredreturntype = self.tstack.popp()

        _param0 = _node.get(1)

        #! visit type
        self.visit(_param0[1])

        #! parameter 1 datatype
        _ptype0 = self.tstack.popp()
        
        _name = _node.get(2)

        #! check if function name is already defined.
        # if  self.symtbl.contains(_name):
        #     error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _name, _node.site)
        
        #! make param list
        _parameters.append((_param0[0], _ptype0))

        #! opcode
        emit_opcode(self, store_fast, _param0[0], self.offset)

        #! register
        self.symtbl.insert_var(_param0[0], self.offset, _ptype0, False, False, _node.site)

        self.offset += 1

        #! compile parameters
        for _each_param in _node.get(3):

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
            self.symtbl.insert_var(_each_param[0], self.offset, _vtype, False, False, _node.site)

            self.offset += 1
            #! end

        #! compile body
        self.visit(_node.get(4))

        #! currentreturn
        _returntype = self.tstack.popp()

        if  not _desiredreturntype.matches(_returntype):
            error.raise_tracked(error_category.CompileError, "expected return type %s, got %s." %  (_desiredreturntype.repr(), _returntype.repr()), _node.site)

        #! add return
        emit_opcode(self, return_control)

        #! end func scope
        self.symtbl.endscope()

        #! store code
        self.state.codes[self.names[-1]][_name] = self.bcodes

        #! restore
        self.offset = _old_offset
        self.bcodes = _old_bcodes

        #! register
        self.symtbl.insert_fun(_name, self.offset, fn_t(_returntype, len(_parameters), _parameters), _returntype, _node.site)

        #! val opcode
        emit_opcode(self, load_funpntr, self.names[-1], _name)

        #! var opcode
        emit_opcode(self, store_global, _name, self.offset)

        #! end
        self.offset += 1

    def ast_native_function(self, _node):
        """    
            $0        $1          $2       $3     $4
            mod   returntype  func_name  params  body
        """
        _parameters = []

        #! target mod
        _mod = _node.get(0)

        #! new func scope
        self.symtbl.newscope()

        #! visit returntype
        self.visit(_node.get(1))

        _returntype = self.tstack.popp()

        #! check if function name is already defined.
        # if  self.symtbl.contains(_node.get(2)):
        #     error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _node.get(2), _node.site)

        #! compile parameters
        for _each_param in _node.get(3):

            #! visit type
            self.visit(_each_param[1])

            #! param dtype
            _vtype = self.tstack.popp()

            #! check if parameter is already defined.
            if  self.symtbl.haslocal(_each_param[0]):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_param[0], _node.site)

            #! make param list
            _parameters.append((_each_param[0], _vtype))

        #! end func scope
        self.symtbl.endscope()

        #! datatype
        _datatype = nativefn_t(_returntype, len(_parameters), _parameters)

        #! register
        self.symtbl.insert_fun(_node.get(2), self.offset, _datatype, _returntype, _node.site)

        #! validate
        _modinfo = getbuiltin(_mod)

        #! check if native exist
        if  not _modinfo:
            error.raise_tracked(error_category.CompileError, "module \"%s\" is not defined." %  _mod, _node.site)
        
        #! check if function is in native
        if  not _modinfo.hasmeta(_node.get(2)):
            error.raise_tracked(error_category.CompileError, "function \"%s\" is not defined at \"%s\"." %  (_node.get(2), _mod), _node.site)

        _meta = _modinfo.getmeta(_node.get(2))

        #! check if meta matches
        if  not _meta.matches(_datatype):
            error.raise_tracked(error_category.CompileError, "function data not matched \"%s\" and \"%s\"." %  (_meta.repr(), _datatype.repr()), _node.site)

        #! val opcode
        emit_opcode(self, load_mod_funpntr, _mod, _node.get(2))

        #! var opcode
        emit_opcode(self, store_global, _node.get(2), self.offset)

        #! end
        self.offset += 1

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
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, True, False, _node.site)

            self.offset     += 1
            self.virtoffset += 1
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
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, False, False, _node.site)

            self.offset += 1
            #! end

    def ast_const_stmnt(self, _node):
        #! global scope?
        _is_global = self.symtbl.isglobal()

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
            
            #! check
            _opcode = store_global if _is_global else store_local

            #! opcode
            emit_opcode(self, _opcode, _variable[0], self.offset)

            #! register
            self.symtbl.insert_var(_variable[0], self.offset, _vtype, _is_global, True, _node.site)

            self.offset += 1

            #! increase when global
            if  _is_global:
                self.virtoffset += 1

            #! end
    
    def ast_assert_stmnt(self, _node):
        if  _node.get(0).type == ast_type.SHORTC_OP:
            self.assert_using_short_circuiting(_node)
        
        else:
            self.assert_using_normal_condition(_node)


    def assert_using_normal_condition(self, _node):
        #! compile condition
        self.visit(_node.get(0))

        #! pop type
        self.tstack.popp()
        
        #! add jump
        _jump_to_end =\
        emit_opcode(self, pop_jump_if_true, TARGET)

        #! compile error
        self.visit(_node.get(1))

        #! pop type
        self.tstack.popp()

        #! assert
        emit_opcode(self, assert_error)

        #! end assert
        _jump_to_end[2] = get_byteoff(self)

    
    def ast_break_stmnt(self, _node):
        self.breaks[-1].append(
            emit_opcode(self, jump_to, TARGET))
    

    def ast_continue_stmnt(self, _node):
        emit_opcode(self, jump_to, self.loops[-1])
    

    def ast_return_stmnt(self, _node):
        """   $0
            return
        """
        if  not _node.get(0):
            #! emit nulltype
            push_ttable(self, null_t())

            #! opcode
            emit_opcode(self, nload, None)
        
        else:
            #! visit expr
            self.visit(_node.get(0))
        
        _dtype = self.tstack.popp()

        if  not self.currentfunctiontype.matches(_dtype):
            error.raise_tracked(error_category.CompileError, "expected return type %s, got %s." %  (self.currentfunctiontype.repr(), _dtype.repr()), _node.site)

        #! opcode
        emit_opcode(self, return_control)
    

    def ast_expr_stmnt(self, _node):
        #! statement
        self.visit(_node.get(0))

        #! pop last type
        self.tstack.popp()

        #! opcode
        emit_opcode(self, pop_top)

class codegen(generator):
    """ Analyzer and byte-code like generator for atom.

        Code block generator.
    """

    def __init__(self, _state):
        super().__init__()
        #! init prop
        self.state   = _state
        self.gparser = parser(self.state)
        self.names   = []

    #! ========== simple ============
    
    def ast_import(self, _node):
        """ I Forgot to implement 2 pass compiler,
            and instead combined analyzer and compiler together.
        """
        for _each_import in _node.get(0):

            #! put extra
            _fpath = _each_import + ".as"
            
            #! check file
            if  not file_isfile(self.state, _fpath):
                error.raise_tracked(error_category.CompileError, "file not found or invalid file \"%s\"." % _each_import, _node.site)

            #! read file first
            read_file(self.state, _fpath)

            #! check if exist
            if  self.symtbl.contains(_each_import):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_import, _node.site)

            #! check for circular import
            if  self.imptbl.contains(_each_import + "->" + self.names[-1]) or self.imptbl.contains(_each_import + "->" + _each_import):
                error.raise_tracked(error_category.CompileError, "can't import \"%s\" due to circular import." %  _each_import, _node.site)

            #! insert if not circular
            self.imptbl.insert(self.names[-1] + "->" + _each_import, None)

            #! parse
            _parse = parser(self.state)

            #! push name
            self.names.append(_each_import)
            self.state.codes[_each_import] = ({})

            #! ==================

            self.symtbl.newparentscope()

            _ast_nodes = _parse.raw_parse()
            _length    = len(_ast_nodes)

            _resume = 0

            for _idx in range(_length):

                _each_node = _ast_nodes[_idx]

                if  _each_node.type == ast_type.FROM      or\
                    _each_node.type == ast_type.IMPORT    or\
                    _each_node.type == ast_type.VAR_STMNT or\
                    _each_node.type == ast_type.CONST_STMNT:
                    #! compile file
                    self.visit(_each_node)

                    _resume = _idx + 1

                    #! next
                    continue
                
                #! make interface

                if  _idx == _resume:
                    for _j in range(_idx, _length):

                        _node_to_make = _ast_nodes[_j]

                        if  _node_to_make.type == ast_type.FROM      or\
                            _node_to_make.type == ast_type.IMPORT    or\
                            _node_to_make.type == ast_type.VAR_STMNT or\
                            _node_to_make.type == ast_type.CONST_STMNT:
                            #! pause
                            _resume = _j + 1
                            break
                        
                        elif _node_to_make.type == ast_type.STRUCT     or\
                             _node_to_make.type == ast_type.IMPLEMENTS or\
                             _node_to_make.type == ast_type.FUNCTION   or\
                             _node_to_make.type == ast_type.FUNCTION_WRAPPER or\
                             _node_to_make.type == ast_type.NATIVE_FUNCTION:
                            #! make interface for node
                            self.visit_int(_node_to_make)

                        else:
                            self.virtoffset += 1
                    
                    #! end

                #! visit each node
                self.visit(_each_node)

            _symbols =\
            self.symtbl.endparentscope()
            
            _members = []

            #! build
            for _each_child in _symbols.aslist():
                #! emit load global (value)
                emit_opcode(self, load_global, _each_child[0], _each_child[1].get_offset())

                #! emit sload (key)
                emit_opcode(self, sload, _each_child[0])

                #! append a member
                _members.append((_each_child[0], _each_child[1].get_datatype()))
            
            #! emit build_module
            emit_opcode(self, build_module, _each_import, len(_members))

            #! store as variable
            emit_opcode(self, store_global, _each_import, self.offset)

            #! register as toplevel global var
            self.symtbl.insert_module(_each_import, self.offset, module_t(_each_import, _members), True, True, _node.site)

            #!
            self.offset     += 1
            self.virtoffset += 1
            self.names.pop()
        #! end
    
    def ast_from(self, _node):
        """
            I Forgot to implement 2 pass compiler,
            and instead combined analyzer and compiler together.
        """
        _import = _node.get(0)

        #! put extra
        _fpath = _import + ".as"
        
        #! check file
        if  not file_isfile(self.state, _fpath):
            error.raise_tracked(error_category.CompileError, "file not found or invalid file \"%s\"." % _import, _node.site)

        #! read file first
        read_file(self.state, _fpath)

        #! check if exist
        if  self.symtbl.contains(_import):
            error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _import, _node.site)

        #! check for circular import
        if  self.imptbl.contains(_import + "->" + self.names[-1]) or self.imptbl.contains(_import + "->" + _import):
            error.raise_tracked(error_category.CompileError, "can't import \"%s\" due to circular import." %  _import, _node.site)

        #! insert if not circular
        self.imptbl.insert(self.names[-1] + "->" + _import, None)

        #! parse
        _parse = parser(self.state)

        #! push name
        self.names.append(_import)
        self.state.codes[_import] = ({})

        #! =========================

        self.symtbl.newparentscope()

        _ast_nodes = _parse.raw_parse()
        _length    = len(_ast_nodes)

        _resume = 0

        for _idx in range(_length):
            
            _each_node = _ast_nodes[_idx]

            if  _each_node.type == ast_type.FROM      or\
                _each_node.type == ast_type.IMPORT    or\
                _each_node.type == ast_type.VAR_STMNT or\
                _each_node.type == ast_type.CONST_STMNT:
                #! compile file
                self.visit(_each_node)

                _resume = _idx + 1

                #! next
                continue
            
            #! make interface

            if  _idx == _resume:
                for _j in range(_idx, _length):

                    _node_to_make = _ast_nodes[_j]

                    if  _node_to_make.type == ast_type.FROM      or\
                        _node_to_make.type == ast_type.IMPORT    or\
                        _node_to_make.type == ast_type.VAR_STMNT or\
                        _node_to_make.type == ast_type.CONST_STMNT:
                        #! pause
                        _resume = _j + 1
                        break
                    
                    elif _node_to_make.type == ast_type.STRUCT     or\
                         _node_to_make.type == ast_type.IMPLEMENTS or\
                         _node_to_make.type == ast_type.FUNCTION   or\
                         _node_to_make.type == ast_type.FUNCTION_WRAPPER or\
                         _node_to_make.type == ast_type.NATIVE_FUNCTION:
                        #! make interface for node
                        self.visit_int(_node_to_make)

                    else:
                        self.virtoffset += 1
                
                #! end

            #! visit each node
            self.visit(_each_node)

        _symbols =\
        self.symtbl.endparentscope()
        
        _members = []

        #! build
        for _each_child in _symbols.aslist():
            #! emit load global (value)
            emit_opcode(self, load_global, _each_child[0], _each_child[1].get_offset())

            #! emit sload (key)
            emit_opcode(self, sload, _each_child[0])

            #! append a member
            _members.append((_each_child[0], _each_child[1].get_datatype()))
        
        #! emit build_module
        emit_opcode(self, build_module, _import, len(_members))

        #! store as variable
        emit_opcode(self, store_global, _import, self.offset)

        _datatype = module_t(_import, _members)

        #! register as toplevel global var
        self.symtbl.insert_module(_import, self.offset, _datatype, True, True, _node.site)

        #!
        self.offset     += 1
        self.virtoffset += 1

        self.names.pop()

        _modoff = (self.offset - 1)

        for _each_attrib in _node.get(1):
            #! check if exist
            if  self.symtbl.contains(_each_attrib):
                error.raise_tracked(error_category.CompileError, "variable \"%s\" was already defined." %  _each_attrib, _node.site)
            
            #! load module
            emit_opcode(self, load_global, _import, _modoff)

            #! load attrib as string
            emit_opcode(self, sload, _each_attrib)

            #! get attribute
            emit_opcode(self, get_attribute)

            #! store as global variable
            emit_opcode(self, store_global, _each_attrib, self.offset)

            #! check for attribute
            if  not _datatype.hasAttribute(_each_attrib):
                error.raise_tracked(error_category.CompileError, "module %s has no attribute \"%s\"." %  (_import, _each_attrib), _node.site)

            #! register
            self.symtbl.insert_var(_each_attrib, self.offset, _datatype.getAttribute(_each_attrib), True, True, _node.site)

            #! end
            self.offset     += 1
            self.virtoffset += 1

    def ast_source(self, _node):
        """ I Forgot to implement 2 pass compiler,
            and instead combined analyzer and compiler together.
        """
        _children = _node.get(0)
        _length   = len(_children)

        _resume = 0

        #! visit each
        for _idx in range(_length):

            _each_node = _children[_idx]

            if  _each_node.type == ast_type.FROM      or\
                _each_node.type == ast_type.IMPORT    or\
                _each_node.type == ast_type.VAR_STMNT or\
                _each_node.type == ast_type.CONST_STMNT:
                #! compile file
                self.visit(_each_node)

                _resume = _idx + 1

                #! next
                continue
                
            #! make interface
            
            if  _idx == _resume:
                for _j in range(_idx, _length):

                    _node_to_make = _children[_j]

                    if  _node_to_make.type == ast_type.FROM      or\
                        _node_to_make.type == ast_type.IMPORT    or\
                        _node_to_make.type == ast_type.VAR_STMNT or\
                        _node_to_make.type == ast_type.CONST_STMNT:
                        #! pause
                        _resume = _j + 1
                        break
                    
                    elif _node_to_make.type == ast_type.STRUCT     or\
                         _node_to_make.type == ast_type.IMPLEMENTS or\
                         _node_to_make.type == ast_type.FUNCTION   or\
                         _node_to_make.type == ast_type.FUNCTION_WRAPPER or\
                         _node_to_make.type == ast_type.NATIVE_FUNCTION:
                        #! make interface for node
                        self.visit_int(_node_to_make)

                    else:
                        self.virtoffset += 1
                
                #! end

            #! visit each node
            self.visit(_each_node)
        
        #! add main
        self.ensure_main_function()
    
    def ensure_main_function(self):
        #! call main
        if  not self.symtbl.contains("main"):
            error.raise_untracked(error_category.CompileError, "main function is not defined!")
        
        _main = self.symtbl.lookup("main")

        if  not _main.get_datatype().isfunction():
            error.raise_tracked(error_category.CompileError, "main is not a user defined function.", _main.get_site())
        
        #! load function
        emit_opcode(self, load_global, "main", _main.get_offset())

        #! make type
        _required_main = fn_t(integer_t(), 1, [("_args", array_t(string_t()))])

        #! check if valid main
        if  not _required_main.matches(_main.get_datatype()):
            error.raise_tracked(error_category.CompileError, "invalid main function, required %s, got %s." % (_required_main.repr(), _main.get_datatype().repr()), _main.get_site())

        #! make args
        for _args in self.state.aargv:
            #! emit arg as string
            emit_opcode(self, sload, _args)
        
        #! make it as array
        emit_opcode(self, build_array, len(self.state.aargv))

        #! remap main
        self.state.calls[self.callid] = _main.site
        self.callid += 1

        #! call
        emit_opcode(self, call_function, 1, self.callid - 1)

        #! add return
        emit_opcode(self, return_control)
    
    
    def generate(self):
        #! push name
        _name = path.basename(self.gparser.lexer.current.fpath.split(".")[0])
        self.names.append(_name)
        self.state.codes[_name] = ({})

        #! compile each child node
        self.visit(self.gparser.parse())

        assert self.tstack.isempty(), "Not all type in stack has been popped out!"

        #! set program code
        self.state.codes["program"] = self.bcodes

        # for i in self.bcodes:
        #     print(i)
        
        #! clean
        self.symtbl = None
        self.imptbl = None

        #! end
        return self.bcodes