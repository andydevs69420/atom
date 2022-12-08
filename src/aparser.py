
from atoken import (token_type, atoken)
from alexer import lexer
from error import (error_category, error)
from aast import (ast_type, stmnt_ast, expr_ast)
from syskey import keywords
from atyping import type_names
from context import context

class parser(object):
    """ Parser for atom.
    """

    MAX_NESTED_EXPR = 255
    MAX_NESTED_TYPE = 10

    def __init__(self, _state):
        self.state     = _state
        self.lexer     = lexer(self.state)
        self.lookahead = self.lexer.getNext()
        self.previous  = self.lexer
        self.context   = []
        self.nestedtyp = 0
        self.nestedexp = 0
    
    #! ======= NESTING CONTROL ========

    def save(self, _type=False):
        return self.nestedexp if not _type else self.nestedtyp
    
    def incr(self, _type=False):
        if  not _type:
            self.nestedexp += 1
            if  self.nestedexp >= parser.MAX_NESTED_EXPR:
                error.raise_untracked(error_category.ParseError, "too much nesting level for an expression!!!")

        else:
            self.nestedtyp += 1
            if  self.nestedtyp >= parser.MAX_NESTED_TYPE:
                error.raise_untracked(error_category.ParseError, "too much nesting level for a type!!!")
    
    def decr(self, _type=False):
        if  not _type:
            self.nestedexp -= 1

        else:
            self.nestedtyp -= 1

    def rest(self, _saved, _type=False):
        if  _type == False:
            self.nestedexp = _saved
        
        else:
            self.nestedtyp = _saved

    #! =========== CONTEXT  ===========
    def enter(self, _ctx):
        self.context.append(_ctx)
    
    def leave(self, _ctx):
        assert (self.context.pop() == _ctx), "invalid context was popped!"
    
    def under(self, _ctx, _immediate):
        if  _immediate:
            return self.context[-1] == _ctx
        
        #! end
        return _ctx in self.context

    #! =========== HELPERS  ===========

    def c_location(self):
        """ Current location.
        """
        return atoken.make_location_from_offsets(
            self.lexer.current.fpath, self.lexer.current.fcode, self.lookahead.ln_of, self.lookahead.ln_of, self.lookahead.cm_of, self.lookahead.cm_of)
        #! end
    
    def d_location(self, _defined):
        """ Defined location.

            Parametrs
            ---------
            _defined : atoken
        """
        return atoken.make_location_from_offsets(
            self.lexer.current.fpath, self.lexer.current.fcode, _defined.ln_of, self.previous.ln_of, _defined.cm_of, self.previous.cm_of)
        #! end

    #! =========== CHECKERS ===========

    def check_t(self, _ttype):
        """ Checks lookahead by type.

            Parameters
            ----------
            _ttype : token_type
        """
        assert type(_ttype) == token_type, "Nah!"
        return (self.lookahead.ttype == _ttype)
    
    def check_v(self, _value):
        """ Checks lookahead by value.

            Parameters
            ----------
            _value : str
        """
        assert type(_value) == str, "Nah!"
        return (self.lookahead.value == _value)
    
    def check_both(self, _ttype, _value):
        """ Checks lookahead by value.

            Parameters
            ----------
            _ttype : token_type
            _value : str
        """
        return (self.check_t(_ttype) and self.check_v(_value))

    def expect_t(self, _ttype):
        """ Expects lookeahead token by type.

            Parameters
            ----------
            _ttype : token_type
        """
        if  not self.check_t(_ttype):
            error.raise_tracked(error_category.ParseError, "unexpected \"%s\" token. Did you mean %s??" % (self.lookahead.value, _ttype.name), self.c_location())
            #! end
        
        #! next
        self.previous  = self.lookahead
        self.lookahead = self.lexer.getNext()

    def expect_v(self, _value):
        """ Expects lookeahead token by value.

            Parameters
            ----------
            _value : str
        """
        if  not self.check_v(_value):
            error.raise_tracked(error_category.ParseError, "unexpected token \"%s\". Did you mean \"%s\"??" % (self.lookahead.value, _value), self.c_location())
            #! end
        
        #! next
        self.previous  = self.lookahead
        self.lookahead = self.lexer.getNext()

    def expect_both(self, _ttype, _value):
        """ Expects lookeahead token from type and value.

            Parameters
            ----------
            _ttype : token_type
            _value : str
        """

        if  not self.check_both(_ttype, _value):
            error.raise_tracked(error_category.ParseError, "unexpected token \"%s\". Did you mean \"%s\"??" % (self.lookahead.value, _value), self.c_location())
            #! end
        
        #! next
        self.previous  = self.lookahead
        self.lookahead = self.lexer.getNext()


    #! =========== AST BUILD ==========

    def raw_iden(self):
        """ Raw identifier, but not keyword.

            Returns
            -------
            str
        """
        _idn = self.lookahead

        #! forward
        self.expect_t(token_type.IDENTIFIER)

        #! check if keyword
        if  keywords.is_keyword(_idn.value):
            error.raise_tracked(error_category.ParseError, "unexpected keyword \"%s\"." % _idn.value, self.d_location(_idn))

        #! end
        return _idn.value

    def list_idn(self):
        """ List of identifiers.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _lists = []

        _lists.append(self.raw_iden())

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! check
            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(error_category.ParseError, "unexpected end of list after \"%s\"." % self.previous.value, self.d_location(_start))
            
            #! append
            _lists.append(self.raw_iden())

        #! end
        return tuple(_lists)
    
    def list_expr(self):
        """ List of expression.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _lists = []

        _exprN = self.nullable_expr()

        #! is null?
        if not _exprN: return tuple(_lists)

        _lists.append(_exprN)

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! next
            _exprN = self.nullable_expr()

            #! check
            if  not _exprN:
                error.raise_tracked(error_category.ParseError, "unexpected end of expression after \"%s\"." % self.previous.value, self.d_location(_start))

            #! append
            _lists.append(_exprN)

        #! end
        return tuple(_lists)
    
    def list_key_pair(self):
        """ List of key value pair.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _lists = []

        _exprN = self.key_value_pair()

        #! is null?
        if not _exprN: return tuple(_lists)

        _lists.append(_exprN)

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! next
            _exprN = self.key_value_pair()

            #! check
            if  not _exprN:
                error.raise_tracked(error_category.ParseError, "unexpected end of key and pair after \"%s\"." % self.previous.value, self.d_location(_start))

            #! append
            _lists.append(_exprN)

        #! end
        return tuple(_lists)
    
    def key_value_pair(self):
        if  self.check_both(token_type.SYMBOL, "**"):
            return (self.non_nullable_expr(), None)

        _key = self.nullable_expr()

        #! is null?
        if not _key: return _key

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        _val = self.non_nullable_expr()

        #! end
        return (_key, _val)
    
    def list_declaire(self):
        """ List of declairation.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _list  = []
        _list.append(self.declaire())

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! check
            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(error_category.ParseError, "unexpected end of declairation after \"%s\"." % self.previous.value, self.d_location(_start))

            #! next
            _list.append(self.declaire())

        #! end
        return tuple(_list)

    def declaire(self):
        #! var name
        _var = self.raw_iden()

        if  not self.check_both(token_type.SYMBOL, "="):
            return (_var, None)

        #! '='
        self.expect_both(token_type.SYMBOL, "=")

        #! value
        _val = self.non_nullable_expr()

        return (_var, _val)
    
    def list_native_parameter(self):
        """ List of native parameters.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _list  = []

        _param = self.native_parameter()
        if not _param: return tuple(_list)

        _list.append(_param)

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! check
            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(error_category.ParseError, "unexpected end of parameters after \"%s\"." % self.previous.value, self.d_location(_start))

            _list.append(self.native_parameter())
        
        #! end
        return tuple(_list)
    
    def native_parameter(self):
        if  not self.check_t(token_type.IDENTIFIER):
            return None
        
        #! param name
        _identifier = self.raw_iden()

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        #! "datatype"
        _datatype = self.native_datatype()

        #!
        return (_identifier, _datatype)
    
    def list_parameter(self):
        """ List of parameters.

            Returns
            -------
            tuple
        """
        _start = self.lookahead
        _list  = []

        _param = self.parameter()
        if not _param: return tuple(_list)

        _list.append(_param)

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            #! check
            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(error_category.ParseError, "unexpected end of parameters after \"%s\"." % self.previous.value, self.d_location(_start))

            _list.append(self.parameter())
        
        #! end
        return tuple(_list)
    
    def parameter(self):
        if  not self.check_t(token_type.IDENTIFIER):
            return None
        
        #! param name
        _identifier = self.raw_iden()

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        #! "datatype"
        _datatype = self.datatype()

        #!
        return (_identifier, _datatype)

    def native_datatype(self):
        """ Use keywords from typing to ensure proper spelling.

            No void.
        """
        if  self.check_both(token_type.IDENTIFIER, type_names.ANY  ):
            return self.t_any()
        if  self.check_both(token_type.IDENTIFIER, type_names.INT  ):
            return self.t_int()
        if  self.check_both(token_type.IDENTIFIER, type_names.FLOAT):
            return self.t_flt()
        if  self.check_both(token_type.IDENTIFIER, type_names.STR  ):
            return self.t_str()
        if  self.check_both(token_type.IDENTIFIER, type_names.BOOL ):
            return self.t_bool()
        #! leave null for void
        if  self.check_both(token_type.IDENTIFIER, type_names.ARRAY):
            return self.t_array_native()
        if  self.check_both(token_type.IDENTIFIER, type_names.FN   ):
            return self.t_fn_native()
        if  self.check_both(token_type.IDENTIFIER, type_names.MAP  ):
            return self.t_map_native()
        #! end
        return self.t_user()
    
    def datatype(self):
        """ Use keywords from typing to ensure proper spelling.

            No void.
        """
        if  self.check_both(token_type.IDENTIFIER, type_names.ANY  ):
            #! disallow any
            return self.t_any_invalid()
        if  self.check_both(token_type.IDENTIFIER, type_names.INT  ):
            return self.t_int()
        if  self.check_both(token_type.IDENTIFIER, type_names.FLOAT):
            return self.t_flt()
        if  self.check_both(token_type.IDENTIFIER, type_names.STR  ):
            return self.t_str()
        if  self.check_both(token_type.IDENTIFIER, type_names.BOOL ):
            return self.t_bool()
        #! leave null for void
        if  self.check_both(token_type.IDENTIFIER, type_names.ARRAY):
            return self.t_array()
        if  self.check_both(token_type.IDENTIFIER, type_names.FN   ):
            return self.t_fn()
        if  self.check_both(token_type.IDENTIFIER, type_names.MAP  ):
            return self.t_map()
        #! end
        return self.t_user()
    
    def native_returntype(self):
        """ Use keywords from typing to ensure proper spelling.

            With void.
        """
        #! allow void when return.
        if  self.check_both(token_type.IDENTIFIER, type_names.VOID):
            return self.t_void()
    
        #! end
        return self.native_datatype()
    
    def returntype(self):
        """ Use keywords from typing to ensure proper spelling.

            With void.
        """
        #! allow void when return.
        if  self.check_both(token_type.IDENTIFIER, type_names.VOID):
            return self.t_void()
    
        #! end
        return self.datatype()

    def t_any(self):
        _any = self.lookahead.value

        #! "any"
        self.expect_both(token_type.IDENTIFIER, type_names.ANY)

        return expr_ast(
            ast_type.ANY_T, "...", _any)
        
    def t_any_invalid(self):
        _start = self.lookahead
        error.raise_tracked(error_category.ParseError, "invalid use of \"any\" type tag.", self.d_location(_start))

    def t_int(self):
        _int = self.lookahead.value

        #! "int"
        self.expect_both(token_type.IDENTIFIER, type_names.INT)

        return expr_ast(
            ast_type.INT_T, "...", _int)
    
    def t_flt(self):
        _float = self.lookahead.value

        #! "float"
        self.expect_both(token_type.IDENTIFIER, type_names.FLOAT)

        return expr_ast(
            ast_type.FLT_T, "...", _float)
    
    def t_str(self):
        _str = self.lookahead.value

        #! "str"
        self.expect_both(token_type.IDENTIFIER, type_names.STR)

        return expr_ast(
            ast_type.STR_T, "...", _str)
    
    def t_bool(self):
        _bool = self.lookahead.value

        #! "bool"
        self.expect_both(token_type.IDENTIFIER, type_names.BOOL)

        return expr_ast(
            ast_type.BOOL_T, "...", _bool)
    
    def t_void(self):
        _void = self.lookahead.value

        #! "void"
        self.expect_both(token_type.IDENTIFIER, type_names.VOID)

        return expr_ast(
            ast_type.VOID_T, "...", _void)

    def t_array_native(self):
        """ Native typing for array.

            Syntax|Grammar
            --------------
            "array" '[' native_datatype ']' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _array = _start.value

        #! nesting
        self.incr(_type=True)

        #! "array"
        self.expect_both(token_type.IDENTIFIER, type_names.ARRAY)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _internal = self.native_datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminated
        self.decr(_type=True)

        return expr_ast(
            ast_type.ARRAY_T, self.d_location(_start), _array, _internal)

    def t_array(self):
        """ Regular typing for array.

            Syntax|Grammar
            --------------
            "array" '[' datatype ']' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _array = _start.value

        #! nesting
        self.incr(_type=True)

        #! "array"
        self.expect_both(token_type.IDENTIFIER, type_names.ARRAY)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _internal = self.datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminted
        self.decr(_type=True)

        return expr_ast(
            ast_type.ARRAY_T, self.d_location(_start), _array, _internal)
    
    def t_fn_native(self):
        """ Native typing for function.

            Syntax|Grammar
            --------------
            "fn" '[' native_datatype ']' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _fn    = _start.value

        #! nesting
        self.incr(_type=True)

        #! "fn"
        self.expect_both(token_type.IDENTIFIER, type_names.FN)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _return = self.native_datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminated
        self.decr(_type=True)

        return expr_ast(
            ast_type.FN_T, self.d_location(_start), _fn, _return)

    def t_fn(self):
        """ Regular typing for function.

            Syntax|Grammar
            --------------
            "fn" '[' datatype ']' ;

            Returns
            -------
            ast
        """

        _start = self.lookahead
        _fn    = _start.value

        #! nesting
        self.incr(_type=True)

        #! "fn"
        self.expect_both(token_type.IDENTIFIER, type_names.FN)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _return = self.datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminated
        self.decr(_type=True)

        return expr_ast(
            ast_type.FN_T, self.d_location(_start), _fn, _return)
    
    def t_map_native(self):
        """ Native typing for map.

            Syntax|Grammar
            --------------
            "map" '[' native_datatype ':' native_datatype ']' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _map   = _start.value

        #! nesting
        self.incr(_type=True)

        #! "map"
        self.expect_both(token_type.IDENTIFIER, type_names.MAP)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _key_type = self.native_datatype()

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        _val_type = self.native_datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminated
        self.decr(_type=True)

        return expr_ast(
            ast_type.MAP_T, self.d_location(_start), _map, _key_type, _val_type)

    def t_map(self):
        """ Regular typing for map.

            Syntax|Grammar
            --------------
            "map" '[' datatype ':' datatype ']' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _map   = _start.value

        #! nesting
        self.incr(_type=True)

        #! "map"
        self.expect_both(token_type.IDENTIFIER, type_names.MAP)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _key_type = self.datatype()

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        _val_type = self.datatype()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! terminated
        self.decr(_type=True)

        return expr_ast(
            ast_type.MAP_T, self.d_location(_start), _map, _key_type, _val_type)
    
    def t_user(self):
        return expr_ast(
            ast_type.TYPE_T, self.d_location(self.lookahead), self.raw_iden())
    
    def atom(self):
        """ ATOM

            Rule
            ----
            atom := <terminal: int>
                    | <terminal: float>
                    | <terminal: str>
                    | <terminal: bool>
                    | <terminal: null>
                    | <terminal: ref>
                    | array_expr
                    | map_expr
                    | '(' non_nullable_expr ')' ;
                    | ε
                    ;
        """
        if  self.check_t(token_type.INTEGER):
            return self.integer()
        if  self.check_t(token_type.FLOAT  ):
            return self.float()
        if  self.check_t(token_type.STRING ):
            return self.string()
        if  self.check_both(token_type.IDENTIFIER, keywords.TRUE ) or\
            self.check_both(token_type.IDENTIFIER, keywords.FALSE):
            return self.boolean()
        if  self.check_both(token_type.IDENTIFIER, keywords.NULL ):
            return self.null()
        if  self.check_t(token_type.IDENTIFIER):
            return self.ref()
        if  self.check_both(token_type.SYMBOL, "["):
            return self.array_expr()
        if  self.check_both(token_type.SYMBOL, "{"):
            return self.map_expr()
        if  self.check_both(token_type.SYMBOL, "("):
            #! '('
            self.expect_both(token_type.SYMBOL, "(")

            _expr = self.non_nullable_expr()
            
            self.expect_both(token_type.SYMBOL, ")")
            #! ')'

            #! end
            return _expr
        
        #! epsilon
        return
    
    def integer(self):
        """ INT expr.

            Returns
            -------
            ast
        """
        _int = self.lookahead

        #! int
        self.expect_t(token_type.INTEGER)

        #! end
        return expr_ast(
            ast_type.INT, self.d_location(_int), _int.value)

    def float(self):
        """ FLOAT expr.

            Returns
            -------
            ast
        """
        _flt = self.lookahead

        #! float
        self.expect_t(token_type.FLOAT)

        #! end
        return expr_ast(
            ast_type.FLOAT, self.d_location(_flt), _flt.value)
    
    def string(self):
        """ STR expr.

            Returns
            -------
            ast
        """
        _str = self.lookahead

        #! string
        self.expect_t(token_type.STRING)

        #! end
        return expr_ast(
            ast_type.STR, self.d_location(_str), _str.value)

    def boolean(self):
        """ BOOL expr.

            Returns
            -------
            ast
        """
        _bool = self.lookahead

        #! bool
        self.expect_t(token_type.IDENTIFIER)

        #! end
        return expr_ast(
            ast_type.BOOL, self.d_location(_bool), _bool.value)
    
    def null(self):
        """ NULL expr.

            Returns
            -------
            ast
        """
        _null = self.lookahead

        #! null
        self.expect_t(token_type.IDENTIFIER)

        #! end
        return expr_ast(
            ast_type.NULL, self.d_location(_null), _null.value)
    
    def ref(self):
        """ REFERENCE expr.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _ref   = self.raw_iden()

        #! end
        return expr_ast(
            ast_type.REF, self.d_location(_start), _ref)
    
    def array_expr(self):
        """ ARRAY expression.

            Syntax|Grammar
            --------------
            '[' list_expr* ']'

            Returns
            -------
            ast
        """
        _start = self.lookahead

        self.enter(context.ARRAY)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _elements = self.list_expr()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        self.leave(context.ARRAY)

        #! end
        return expr_ast(
            ast_type.ARRAY, self.d_location(_start), _elements)
    
    def map_expr(self):
        """ MAP expression.

            Syntax|Grammar
            --------------
            '{' list_key_value_pair '}'

            Returns
            -------
            ast
        """
        _start = self.lookahead

        self.enter(context.MAP)

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _elements = self.list_key_pair()
        
        self.expect_both(token_type.SYMBOL, "}")
        #! '}'

        self.leave(context.MAP)

        #! end
        return expr_ast(
            ast_type.MAP, self.d_location(_start), _elements)
    

    def member(self):
        _start = self.lookahead
        _node  = self.atom()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, ".") or\
              self.check_both(token_type.SYMBOL, "[") or\
              self.check_both(token_type.SYMBOL, "!") or\
              self.check_both(token_type.SYMBOL, "("):

            #! nesting
            self.incr()

            if  self.check_both(token_type.SYMBOL, "."):
                #! '.'
                self.expect_t(token_type.SYMBOL)

                #! attrib
                _attrib = self.raw_iden()

                _node = expr_ast(
                    ast_type.ATTRIBUTE, self.d_location(_start), _node, _attrib)
            
            elif self.check_both(token_type.SYMBOL, "["):
                #! '['
                self.expect_both(token_type.SYMBOL, "[")

                _expr = self.non_nullable_expr()
                
                self.expect_both(token_type.SYMBOL, "]")
                #! ']'

                _node = expr_ast(
                    ast_type.ELEMENT, self.d_location(_start), _node, _expr)
            
            elif self.check_both(token_type.SYMBOL, "!"):
                #! '!'
                self.expect_both(token_type.SYMBOL, "!")

                #! wrapper name
                _name = self.raw_iden()

                #! '('
                self.expect_both(token_type.SYMBOL, "(")

                _params = self.list_expr()
                
                self.expect_both(token_type.SYMBOL, ")")
                #! ')'

                _node = expr_ast(
                    ast_type.CALL_WRAPPER, self.d_location(_start), _node, _name, _params)

            
            elif self.check_both(token_type.SYMBOL, "("):
                #! '('
                self.expect_both(token_type.SYMBOL, "(")

                _args = self.list_expr()
                
                self.expect_both(token_type.SYMBOL, ")")
                #! ')'

                _node = expr_ast(
                    ast_type.CALL, self.d_location(_start), _node, _args)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node

    def unary_op(self):
        _start = self.lookahead
        _node  = ...

        #! nesting
        self.incr()

        if  self.check_both(token_type.SYMBOL, "~" ) or\
            self.check_both(token_type.SYMBOL, "!" ) or\
            self.check_both(token_type.SYMBOL, "+" ) or\
            self.check_both(token_type.SYMBOL, "-" ):

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)
            
            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))

            _node = expr_ast(
                ast_type.UNARY_OP, self.d_location(_start), _opt, _rhs)
        
        #! unpack
        elif self.check_both(token_type.SYMBOL, "*" ):

            if  not self.under(context.ARRAY, True):
                error.raise_tracked(error_category.SemanticError, "cannot unpack here.", self.d_location(_start))

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))

            _node = expr_ast(
                ast_type.UNARY_UNPACK, self.d_location(_start), _opt, _rhs)
        
        elif self.check_both(token_type.SYMBOL, "**"):

            if  not self.under(context.MAP, True):
                error.raise_tracked(error_category.SemanticError, "cannot unpack here.", self.d_location(_start))

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))

            _node = expr_ast(
                ast_type.UNARY_UNPACK, self.d_location(_start), _opt, _rhs)
        
        else:
            _node = self.member()

        #! terminated
        self.decr()

        #! end
        return _node

    def power(self):
        """ POWER expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.unary_op()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "^^"):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node

    def multiplicative(self):
        """ MULTIPLICATIVE expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.power()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "*") or\
              self.check_both(token_type.SYMBOL, "/") or\
              self.check_both(token_type.SYMBOL, "%"):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.power()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node

    def addetive(self):
        """ ADDETIVE expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.multiplicative()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "+") or\
              self.check_both(token_type.SYMBOL, "-"):
            
            #! nesting
            self.incr()
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.multiplicative()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def shift(self):
        """ SHIFT expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.addetive()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "<<") or\
              self.check_both(token_type.SYMBOL, ">>"):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.addetive()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def relational(self):
        """ RELATIONAL expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.shift()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "<" ) or\
              self.check_both(token_type.SYMBOL, "<=") or\
              self.check_both(token_type.SYMBOL, ">" ) or\
              self.check_both(token_type.SYMBOL, ">="):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.shift()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def equality(self):
        """ EQUALITY expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.relational()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "==") or\
              self.check_both(token_type.SYMBOL, "!="):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.relational()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def bitwise(self):
        """ BITWISE expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.equality()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "&") or\
              self.check_both(token_type.SYMBOL, "|") or\
              self.check_both(token_type.SYMBOL, "^"):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.equality()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def short_circuiting(self):
        """ SHORT CIRCUITING | JUMP (depends on context) expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.bitwise()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "&&") or\
              self.check_both(token_type.SYMBOL, "||"):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.bitwise()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.SHORTC_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def simple_assignment(self):
        """ SIMPLE ASSIGNMENT expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.short_circuiting()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "="):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.bitwise()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.SIMPLE_ASS, self.d_location(_start), _node, _opt, _rhs)

        #! restore
        self.rest(_saved)

        #! end
        return _node
    
    def augmented_assignment(self):
        """ AUGMENTED ASSIGNMENT expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.simple_assignment()

        if not _node: return _node

        #! save old
        _saved = self.save()

        while self.check_both(token_type.SYMBOL, "~=" ) or\
              self.check_both(token_type.SYMBOL, "^^=") or\
              self.check_both(token_type.SYMBOL, "*=" ) or\
              self.check_both(token_type.SYMBOL, "/=" ) or\
              self.check_both(token_type.SYMBOL, "%=" ) or\
              self.check_both(token_type.SYMBOL, "+=" ) or\
              self.check_both(token_type.SYMBOL, "-=" ) or\
              self.check_both(token_type.SYMBOL, "<<=") or\
              self.check_both(token_type.SYMBOL, ">>=") or\
              self.check_both(token_type.SYMBOL, "&=" ) or\
              self.check_both(token_type.SYMBOL, "|=" ) or\
              self.check_both(token_type.SYMBOL, "^=" ):
            
            #! nesting
            self.incr()

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.simple_assignment()
            if  not _rhs:
                error.raise_tracked(error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.AUGMENT_ASS, self.d_location(_start), _node, _opt, _rhs)

        #! restore
        self.rest(_saved)

        #! end
        return _node

    def nullable_expr(self):
        return self.augmented_assignment()
    
    def non_nullable_expr(self):
        _node = self.nullable_expr()
        if  not _node:
            error.raise_tracked(error_category.ParseError, "expects an expression, got \"%s\"." % self.lookahead.value, self.c_location())

        #! end
        return _node

    def compound_stmnt(self):
        """ COMPOUND statement.

            Returns
            -------
            ast
        """
        if  self.check_both(token_type.IDENTIFIER, keywords.FUN):
            return self.function()
        if  self.check_both(token_type.IDENTIFIER, keywords.STRUCT):
            return self.struct()
        if  self.check_both(token_type.IDENTIFIER, keywords.ENUM):
            return self.enum()
        if  self.check_both(token_type.IDENTIFIER, keywords.IF):
            return self.if_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.SWITCH):
            return self.switch_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.FOR):
            return self.for_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.WHILE):
            return self.while_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.DO):
            return self.dowhile_stmnt()
        if  self.check_both(token_type.SYMBOL, "{"):
            return self.block_of_stmnt()
        #! end
        return self.simple_stmnt()

    def function(self):
        """ Function declairation.

            Syntax|Grammar
            --------------
            "fun" '[' returntype ']' raw_iden '(' list_parameters ')' function_body;

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! enter ctx
        self.enter(context.FUNCTION)

        #! "fun"
        self.expect_both(token_type.IDENTIFIER, keywords.FUN)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _return = self.returntype()
    
        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        _fname = self.raw_iden()

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _parameters = self.list_parameter()
    
        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        _body = self.function_body()

        #! leave ctx
        self.leave(context.FUNCTION)

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "function declairation should be done globally!", self.d_location(_start))

        #! end
        return stmnt_ast(
            ast_type.FUNCTION, self.d_location(_start), _return, _fname, _parameters, _body)
    
    def function_body(self):
        _body = []
        #! enter ctx
        self.enter(context.LOCAL)

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        while True:
            _node = self.compound_stmnt()

            #! check if epsilon
            if  not _node: break

            #! child node
            _body.append(_node)

        self.expect_both(token_type.SYMBOL, "}")
        #! '}'
        
        #! leave ctx
        self.leave(context.LOCAL)

        #! end
        return tuple(_body)
    
    def struct(self):
        """ STRUCT declairation.

            Syntax|Grammar
            --------------
            "struct" list_idn '{' struct_body '}' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        #! "struct"
        self.expect_both(token_type.IDENTIFIER, keywords.STRUCT)

        _subtypes = self.list_idn()

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _body = self.struct_body()

        self.expect_both(token_type.SYMBOL, "}")
        #! '}'

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "struct declairation should be done globally!", self.d_location(_start))

        return stmnt_ast(
            ast_type.STRUCT, self.d_location(_start), _subtypes, _body)
    
    def struct_body(self):
        _body = []

        _memberN = self.struct_member()

        while _memberN:
            _body.append(_memberN)

            #! ';'
            self.expect_both(token_type.SYMBOL, ";")
            
            #! next
            _memberN = self.struct_member()
        
        return tuple(_body)
    
    def struct_member(self):
        if  not self.check_t(token_type.IDENTIFIER):
            return None
        
        _name = self.raw_iden()

        #! ':'
        self.expect_both(token_type.SYMBOL, ":")

        _type = self.datatype()

        return (_name, _type)
    

    def enum(self):
        """ ENUM statement.

            Syntax|Grammar
            --------------
            "enum" raw_iden '{' enum_body '}' ;
        
            Returns
            -------
            ast
        """
        _start = self.lookahead
        #! "enum"
        self.expect_both(token_type.IDENTIFIER, keywords.ENUM)

        _enumname = self.raw_iden()

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _enumbody = self.enum_body()

        self.expect_both(token_type.SYMBOL, "}")
        #! '}'

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "enum declairation should be done globally!", self.d_location(_start))

        return stmnt_ast(
            ast_type.ENUM, self.d_location(_start), _enumname, _enumbody)

    
    def enum_body(self):
        _start = self.lookahead
        _body  = []

        _memberN = self.enum_member()
        if not _memberN:return tuple(_body)

        _body.append(_memberN)

        while self.check_both(token_type.SYMBOL, ","):
            #! ','
            self.expect_t(token_type.SYMBOL)

            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(error_category.SemanticError, "unexpected end of enum member.", self.d_location(_start))
            
            #! next
            _body.append(self.enum_member())

        return tuple(_body)
    
    def enum_member(self):
        if  not self.check_t(token_type.IDENTIFIER):
            return None
        
        _member = self.raw_iden()

        #! '='
        self.expect_both(token_type.SYMBOL, "=")

        _value = self.non_nullable_expr()

        return (_member, _value)
    
    def if_stmnt(self):
        """ IF/ELSE statement.

            Syntax|Grammar
            --------------
            "if" '(' non_nullable_expression ')' compound_stmnt ("else" compound_stmnt)? ;

            Returns
            -------
            ast
        """
        #! "if"
        self.expect_both(token_type.IDENTIFIER, keywords.IF)

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _condition = self.non_nullable_expr()

        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        _statement = self.compound_stmnt()

        #! if no else
        if  not self.check_both(token_type.IDENTIFIER, keywords.ELSE):
            return stmnt_ast(
                ast_type.IF_STMNT, "...", _condition, _statement, None)

        #! if wth else
        self.expect_both(token_type.IDENTIFIER, keywords.ELSE)

        _else = self.compound_stmnt()

        return stmnt_ast(
            ast_type.IF_STMNT, "...", _condition, _statement, _else)

    def switch_stmnt(self):
        #! "switch"
        self.expect_both(token_type.IDENTIFIER, keywords.SWITCH)

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _condition = self.non_nullable_expr()

        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _switch_body = self.switch_body()

        self.expect_both(token_type.SYMBOL, "}")
        #! '}'

        return stmnt_ast(
            ast_type.SWITCH_STMNT, "...", _condition, _switch_body)
    
    def switch_body(self):
        """ sequencial.
            case0:...
            case1:...
            case2:...
            caseN:...
            else :...
        """
        _cases = [[], None]
        while self.check_both(token_type.IDENTIFIER, keywords.CASE):
            #! "case"
            self.expect_both(token_type.IDENTIFIER, keywords.CASE)

            #! case match
            _match = self.list_expr()

            #! ':'
            self.expect_both(token_type.SYMBOL, ":")

            #! statement
            _stmnt = self.compound_stmnt()

            _cases[0].append((_match, _stmnt))
        

        if  len(_cases[0]) > 0 and self.check_both(token_type.IDENTIFIER, keywords.ELSE):
            #! allow "else" when "_cases" is not empty.
            #! "else"
            self.expect_both(token_type.IDENTIFIER, keywords.ELSE)

            #! ':'
            self.expect_both(token_type.SYMBOL, ":")

            #! "else" statement
            _cases[1] = self.compound_stmnt()

        #! end
        return tuple(_cases)

    def for_stmnt(self):
        """ FOR statement.

            Syntax|Grammar
            --------------
            "for" '(' nullable_expression ';' nullable_expression ';' nullable_expression ')' compound_stmnt ;

            Returns
            -------
            ast
        """
        #! "for"
        self.expect_both(token_type.IDENTIFIER, keywords.FOR)

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _init = self.nullable_expr()

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        _cond = self.nullable_expr()

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")
        
        _mutt = self.nullable_expr() #! mutation
        
        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        self.enter(context.LOOP)

        #! body
        _stmnt = self.compound_stmnt()

        self.leave(context.LOOP)

        return stmnt_ast(
            ast_type.FOR_STMNT, "...", _init, _cond, _mutt, _stmnt)
    
    def while_stmnt(self):
        """ WHILE statement.

            Syntax|Grammar
            --------------
            "while" '(' non_nullable_expression ')' compound_stmnt ;

            Returns
            -------
            ast
        """
        #! "while"
        self.expect_both(token_type.IDENTIFIER, keywords.WHILE)

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _cond = self.non_nullable_expr()
        
        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        self.enter(context.LOOP)

        #! body
        _stmnt = self.compound_stmnt()

        self.leave(context.LOOP)

        return stmnt_ast(
            ast_type.WHILE_STMNT, "...", _cond, _stmnt)
    
    def dowhile_stmnt(self):
        """ DO WHILE statement.

            Syntax|Grammar
            --------------
            "do" compound_stmnt "while" '(' non_nullable_expr ')' ;

            Returns
            -------
            ast
        """
        #! "do"
        self.expect_both(token_type.IDENTIFIER, keywords.DO)

        self.enter(context.LOOP)

        _body = self.compound_stmnt()

        self.leave(context.LOOP)

        #! "while"
        self.expect_both(token_type.IDENTIFIER, keywords.WHILE)

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _cond = self.non_nullable_expr()
        
        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        return stmnt_ast(
            ast_type.DOWHILE_STMNT, "...", _body, _cond)

    
    def block_of_stmnt(self):
        """ BLOCK OF STATEMENT.

            Syntax|Grammar
            --------------
            '{' compound_stmnt* '}'

            Returns
            -------
            ast
        """
        _body = []
        
        self.enter(context.LOCAL)
        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _stmntN = self.compound_stmnt()

        while _stmntN:
            #! insert
            _body.append(_stmntN)

            #! next
            _stmntN = self.compound_stmnt()
        
        self.expect_both(token_type.SYMBOL, "}")
        #! '}'
        self.leave(context.LOCAL)

        return stmnt_ast(
            ast_type.BLOCK_STMNT, "...", tuple(_body))

    def simple_stmnt(self):
        """ SIMPLE statement.

            Returns
            -------
            ast
        """
        if  self.check_both(token_type.IDENTIFIER, keywords.IMPORT):
            return self.import_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.WRAP):
            return self.function_wrapper()
        if  self.check_both(token_type.IDENTIFIER, keywords.NATIVE):
            return self.native_function_proto()
        if  self.check_both(token_type.IDENTIFIER, keywords.VAR):
            return self.var_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.LET):
            return self.let_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.CONST):
            return self.const_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.BREAK):
            return self.break_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.CONTINUE):
            return self.continue_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.RETURN):
            return self.return_stmnt()

        #! end
        return self.expr_stmnt()
    
    
    def import_stmnt(self):
        """ IMPORT statement.

            Syntax|Grammar
            --------------
            "import" '[' list_idn ']' ';'

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! "import"
        self.expect_both(token_type.IDENTIFIER, keywords.IMPORT)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _imports = self.list_idn()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "cannot declaire imports here!", self.d_location(_start))

        _locsite = self.d_location(_start)

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        return stmnt_ast(
            ast_type.IMPORT, _locsite, _imports)
    
    def function_wrapper(self):
        """ Function wrapper

            Syntax|Grammar
            --------------
            "wrap" parameter raw_iden '(' list_parameter ')' non_nullable_expression ;

            Returns
            -------
            ast
        """
        _start = self.lookahead
        #! "wrap"
        self.expect_both(token_type.IDENTIFIER, keywords.WRAP)

        _param0 = self.parameter()

        #! wrapper name
        _wrapname = self.raw_iden()

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _parameters = self.list_parameter()

        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        _expr = self.non_nullable_expr()

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "function wrapper declairation should be done globally!", self.d_location(_start))

        _locsite = self.d_location(_start)

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        return expr_ast(
            ast_type.FUNCTION_WRAPPER, _locsite, _param0, _wrapname, _parameters, _expr)
    
    def native_function_proto(self):
        """ Native function prototype.

            Syntax|Grammar
            --------------
            anotation
            "fun" '[' returntype ']' raw_iden '(' list_parameters ')' ';' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! "native"
        self.expect_both(token_type.IDENTIFIER, keywords.NATIVE)

        #! "::"
        self.expect_both(token_type.SYMBOL, "::")

        #! mod directory
        _lib = self.raw_iden()

        #! enter ctx
        self.enter(context.FUNCTION)

        #! "fun"
        self.expect_both(token_type.IDENTIFIER, keywords.FUN)

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _return = self.returntype()
    
        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        _fname = self.raw_iden()

        #! '('
        self.expect_both(token_type.SYMBOL, "(")

        _parameters = self.list_native_parameter()
    
        self.expect_both(token_type.SYMBOL, ")")
        #! ')'

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        #! leave ctx
        self.leave(context.FUNCTION)

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "function prototype declairation should be done globally!", self.d_location(_start))

        #! end
        return stmnt_ast(
            ast_type.NATIVE_FUNCTION, self.d_location(_start), _lib, _return, _fname, _parameters)
    
    def var_stmnt(self):
        #! "var"
        self.expect_both(token_type.IDENTIFIER, keywords.VAR)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        if  not self.under(context.GLOBAL, True):
            error.raise_tracked(error_category.SemanticError, "cannot use \"var\" to declaire variables here!", _ended)

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        #! end
        return stmnt_ast(
            ast_type.VAR_STMNT, _ended, _declaire)

    def let_stmnt(self):
        #! "let"
        self.expect_both(token_type.IDENTIFIER, keywords.LET)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        if  not self.under(context.LOCAL, False):
            error.raise_tracked(error_category.SemanticError, "cannot use \"let\" to declaire variables here!", _ended)

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        #! end
        return stmnt_ast(
            ast_type.LET_STMNT, _ended, _declaire)
    
    def const_stmnt(self):
        #! "const"
        self.expect_both(token_type.IDENTIFIER, keywords.CONST)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        #! end
        return stmnt_ast(
            ast_type.CONST_STMNT, _ended, _declaire)
    
    def break_stmnt(self):
        """ BREAK statement.

            Syntax|Grammar
            --------------
            "break" ';' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! "break"
        self.expect_both(token_type.IDENTIFIER, keywords.BREAK)

        if  not self.under(context.LOOP, False):
            error.raise_tracked(error_category.SemanticError, "invalid \"break\" outside loop.", self.d_location(_start))

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        return stmnt_ast(
            ast_type.BREAK_STMNT, "...")
    
    def continue_stmnt(self):
        """ CONTINUE statement.

            Syntax|Grammar
            --------------
            "continue" ';' ;

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! "continue"
        self.expect_both(token_type.IDENTIFIER, keywords.CONTINUE)

        if  not self.under(context.LOOP, False):
            error.raise_tracked(error_category.SemanticError, "invalid \"continue\" outside loop.", self.d_location(_start))

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        return stmnt_ast(
            ast_type.CONTINUE_STMNT, "...")

    def return_stmnt(self):
        _start = self.lookahead

        #! "return"
        self.expect_both(token_type.IDENTIFIER, keywords.RETURN)

        _expr = self.nullable_expr()

        if  not self.under(context.FUNCTION, False):
            error.raise_tracked(error_category.SemanticError, "invalid \"return\" outside function.", self.d_location(_start))

        self.expect_both(token_type.SYMBOL, ";")
        #! ';'

        return stmnt_ast(
            ast_type.RETURN_STMNT, self.d_location(_start), _expr)

    def expr_stmnt(self):
        """ EXPRESSION_STATEMENT statement.

            Syntax|Grammar
            --------------
            nullable_expr ';'

            Returns
            -------
            ast
        """
        _node = self.nullable_expr()
        if not _node: return _node

        # ';'
        self.expect_both(token_type.SYMBOL, ";")
        
        #! end
        return stmnt_ast(
            ast_type.EXPR_STMNT, "...", _node)
        
    def source(self):
        """ SOURCE file.

            Syntax|Grammar
            --------------
            compound_stmnt* EOF

            Returns
            -------
            ast
        """
        _stmnt = self.raw_parse()

        return stmnt_ast(
            ast_type.SOURCE, "...", _stmnt)
    
    def hasNext(self):
        return not self.check_t(token_type.EOF)
    
    def raw_parse(self):
        _stmnt = []

        #! enter ctx
        self.enter(context.GLOBAL)

        while self.hasNext():
            _node = self.compound_stmnt()

            #! check if epsilon
            if  not _node: break

            #! child node
            _stmnt.append(_node)
        
        #! eof
        self.expect_t(token_type.EOF)
        
        #! leave ctx
        self.leave(context.GLOBAL)

        assert self.nestedtyp <= 0, "uncaught incremental!!!"
        assert self.nestedexp <= 0, "uncaught incremental!!!"

        #! end
        return tuple(_stmnt)

    def parse(self):
        return self.source()
        

        


