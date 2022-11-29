
from atoken import (token_type, atoken)
from lexer import lexer
from error import (error_category, error)

from ast import (ast_type, stmnt_ast, expr_ast)

from syskey import (keywords)
from context import context

class parser(object):
    """ Parser for atom.
    """

    def __init__(self, _state):
        self.__state   = _state
        self.lexer     = lexer(self.__state)
        self.lookahead = self.lexer.getNext()
        self.previous  = self.lexer
        self.context   = []
    
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
            error.raise_tracked(
                error_category.ParseError, "unexpected \"%s\" token. Did you mean %s??" % (self.lookahead.value, _ttype.name), self.c_location())
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
            error.raise_tracked(
                error_category.ParseError, "unexpected token \"%s\". Did you mean \"%s\"??" % (self.lookahead.value, _value), self.c_location())
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
            error.raise_tracked(
                error_category.ParseError, "unexpected token \"%s\". Did you mean \"%s\"??" % (self.lookahead.value, _value), self.c_location())
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
            error.raise_tracked(
                error_category.ParseError, "unexpected keyword \"%s\"." % _idn.value, self.d_location(_idn))

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
                error.raise_tracked(error_category.ParseError, "unexpected end of list after \"%s\"." % self.previous.value, self.d_location(_start))

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
                error.raise_tracked(error_category.ParseError, "unexpected end of list after \"%s\"." % self.previous.value, self.d_location(_start))

            #! append
            _lists.append(_exprN)

        #! end
        return tuple(_lists)
    
    def key_value_pair(self):
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
                error.raise_tracked(error_category.ParseError, "unexpected end of list after \"%s\"." % self.previous.value, self.d_location(_start))

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
            ast_type.INT, "...", _int.value)

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
            ast_type.FLOAT, "...", _flt.value)
    
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
            ast_type.STR, "...", _str.value)

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
            ast_type.BOOL, "...", _bool.value)
    
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
            ast_type.NULL, "...", _null.value)
    
    def ref(self):
        """ REFERENCE expr.

            Returns
            -------
            ast
        """
        _ref = self.lookahead

        #! ref
        self.expect_t(token_type.IDENTIFIER)

        #! end
        return expr_ast(
            ast_type.NULL, "...", _ref.value)
    
    def array_expr(self):
        """ ARRAY expression.

            Syntax
            ------
            '[' list_expr* ']'

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! '['
        self.expect_both(token_type.SYMBOL, "[")

        _elements = self.list_expr()

        self.expect_both(token_type.SYMBOL, "]")
        #! ']'

        #! end
        return expr_ast(
            ast_type.ARRAY, self.d_location(_start), _elements)
    
    def map_expr(self):
        """ MAP expression.

            Syntax
            ------
            '{' list_key_value_pair '}'

            Returns
            -------
            ast
        """
        _start = self.lookahead

        #! '{'
        self.expect_both(token_type.SYMBOL, "{")

        _elements = self.list_key_pair()
        
        self.expect_both(token_type.SYMBOL, "}")
        #! '}'

        #! end
        return expr_ast(
            ast_type.MAP, self.d_location(_start), _elements)
    

    def member(self):
        _start = self.lookahead
        _node  = self.atom()

        while self.check_both(token_type.SYMBOL, ".") or\
              self.check_both(token_type.SYMBOL, "[") or\
              self.check_both(token_type.SYMBOL, "("):

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
            
            elif self.check_both(token_type.SYMBOL, "("):
                #! '('
                self.expect_both(token_type.SYMBOL, "(")

                _args = self.list_expr()
                
                self.expect_both(token_type.SYMBOL, ")")
                #! ')'

                _node = expr_ast(
                    ast_type.CALL, self.d_location(_start), _node, _args)
        
        #! end
        return _node

    def unary_op(self):
        _start = self.lookahead

        if  self.check_both(token_type.SYMBOL, "~") or\
            self.check_both(token_type.SYMBOL, "!") or\
            self.check_both(token_type.SYMBOL, "+") or\
            self.check_both(token_type.SYMBOL, "-"):

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)
            
            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))

            return expr_ast(
                ast_type.UNARY_OP, self.d_location(_start), _opt, _rhs)
        
        #! unpack
        if  self.check_both(token_type.SYMBOL, "*" ) or\
            self.check_both(token_type.SYMBOL, "**"):

            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))

            return expr_ast(
                ast_type.UNARY_UNPACK, self.d_location(_start), _opt, _rhs)
        
        #! cast
        if  self.check_both(token_type.SYMBOL, "("):
            _iscast, _cast_or_expr = False, ...
            
            #! '('
            self.expect_both(token_type.SYMBOL, "(")

            if  not self.check_t(token_type.IDENTIFIER):
                #! expresion
                _cast_or_expr = self.non_nullable_expr()
            else:
                #! cast
                _iscast = True
                _cast_or_expr = self.raw_iden()

            #! ')'
            self.expect_both(token_type.SYMBOL, ")")

            if not _iscast: return _cast_or_expr

            #! return as cast
            _expr = self.non_nullable_expr()
            
            #! end
            return expr_ast(
                ast_type.UNARY_CAST, self.d_location(_start), _cast_or_expr, _expr)

        #! end
        return self.member()

    def power(self):
        """ POWER expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.unary_op()

        if not _node: return _node

        while self.check_both(token_type.SYMBOL, "^^"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.unary_op()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "*") or\
              self.check_both(token_type.SYMBOL, "/") or\
              self.check_both(token_type.SYMBOL, "%"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.power()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "+") or\
              self.check_both(token_type.SYMBOL, "-"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.multiplicative()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "<<") or\
              self.check_both(token_type.SYMBOL, ">>"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.addetive()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "<" ) or\
              self.check_both(token_type.SYMBOL, "<=") or\
              self.check_both(token_type.SYMBOL, ">" ) or\
              self.check_both(token_type.SYMBOL, ">="):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.shift()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "==") or\
              self.check_both(token_type.SYMBOL, "!="):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.relational()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "&") or\
              self.check_both(token_type.SYMBOL, "|") or\
              self.check_both(token_type.SYMBOL, "^"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.equality()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "&&") or\
              self.check_both(token_type.SYMBOL, "||"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.bitwise()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.SHORTC_OP, self.d_location(_start), _node, _opt, _rhs)
        
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

        while self.check_both(token_type.SYMBOL, "="):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.bitwise()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.SIMPLE_ASS, self.d_location(_start), _node, _opt, _rhs)

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
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.simple_assignment()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % _opt, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.AUGMENTED_ASS, self.d_location(_start), _node, _opt, _rhs)

        #! end
        return _node

    def nullable_expr(self):
        return self.simple_assignment()
    
    def non_nullable_expr(self):
        _node = self.nullable_expr()
        if  not _node:
            error.raise_tracked(
                error_category.ParseError, "expects an expression, got \"%s\"." % self.lookahead.value, self.c_location())

        #! end
        return _node

    def compound_stmnt(self):
        """ COMPOUND statement.

            Returns
            -------
            ast
        """
        return self.simple_stmnt()

    def simple_stmnt(self):
        """ SIMPLE statement.

            Returns
            -------
            ast
        """
        if  self.check_both(token_type.IDENTIFIER, keywords.IMPORT):
            return self.import_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.VAR):
            return self.var_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.LET):
            return self.let_stmnt()
        if  self.check_both(token_type.IDENTIFIER, keywords.CONST):
            return self.const_stmnt()

        #! end
        return self.expr_stmnt()

    def import_stmnt(self):
        """ IMPORT statement.

            Syntax
            ------
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
            error.raise_tracked(error_category.SematicError, "cannot declaire imports here!", self.d_location(_start))

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        return stmnt_ast(
            ast_type.IMPORT, "...", _imports)
    
    def var_stmnt(self):
        #! "var"
        self.expect_both(token_type.IDENTIFIER, keywords.VAR)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        #! end
        return stmnt_ast(
            ast_type.VAR_STMNT, _ended, _declaire)

    def let_stmnt(self):
        #! "let"
        self.expect_both(token_type.IDENTIFIER, keywords.LET)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        if  not self.under(context.LOCAL, True):
            error.raise_tracked(error_category.SematicError, "cannot use \"let\" to declaire variables here!", _ended)

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        #! end
        return stmnt_ast(
            ast_type.LET_STMNT, _ended, _declaire)
    
    def const_stmnt(self):
        #! "const"
        self.expect_both(token_type.IDENTIFIER, keywords.CONST)
        
        _start = self.lookahead

        _declaire = self.list_declaire()

        _ended = self.d_location(_start)

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        #! end
        return stmnt_ast(
            ast_type.CONST_STMNT, _ended, _declaire)

    def expr_stmnt(self):
        """ EXPRESSION_STATEMENT statement.

            Syntax
            ------
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

            Syntax
            ------
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

        #! end
        return tuple(_stmnt)

    def parse(self):
        return self.source()
        

        


