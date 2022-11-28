
from atoken import (token_type, atoken)
from lexer import lexer
from error import (error_category, error)

from ast import (ast_type, stmnt_ast, expr_ast)

from syskey import (keywords)

class parser(object):
    """ Parser for atom.
    """

    def __init__(self, _state):
        self.__state   = _state
        self.lexer     = lexer(self.__state)
        self.lookahead = self.lexer.getNext()
        self.previous  = self.lexer
    

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
            self.expect_t(token_type.SYMBOL)

            if  not self.check_t(token_type.IDENTIFIER):
                error.raise_tracked(
                    error_category.ParseError, "unexpected end of list after \"%s\"." % self.previous.value, self.d_location(_start))

            _lists.append(self.raw_iden())

        #! end
        return tuple(_lists)
    
    def expr_g1(self):
        """ ATOM

            Rule
            ----
            atom := <terminal: int>
                    | <terminal: float>
                    | <terminal: str>
                    | <terminal: bool>
                    | <terminal: null>
                    | <terminal: ref>
                    ;
        """
        if  self.check_t(token_type.INTEGER):
            return self.expr_0()
        if  self.check_t(token_type.FLOAT  ):
            return self.expr_1()
        if  self.check_t(token_type.STRING ):
            return self.expr_2()
        if  self.check_both(token_type.IDENTIFIER, keywords.TRUE ) or\
            self.check_both(token_type.IDENTIFIER, keywords.FALSE):
            return self.expr_3()
        if  self.check_both(token_type.IDENTIFIER, keywords.NULL ):
            return self.expr_4()
    
    def expr_0(self):
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
            ast_type.INT, "", _int.value)

    def expr_1(self):
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
            ast_type.FLOAT, "", _flt.value)
    
    def expr_2(self):
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
            ast_type.STR, "", _str.value)

    def expr_3(self):
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
            ast_type.BOOL, "", _bool.value)
    
    def expr_4(self):
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
            ast_type.NULL, "", _null.value)

    def expr_N(self):
        """ ADDETIVE expression.

            Returns
            -------
            ast
        """
        _start = self.lookahead
        _node  = self.expr_g1()

        if not _node: return _node

        while self.check_both(token_type.SYMBOL, "+") or\
              self.check_both(token_type.SYMBOL, "-"):
            
            _opt = self.lookahead.value
            self.expect_t(token_type.SYMBOL)

            _rhs = self.expr_g1()
            if  not _rhs:
                error.raise_tracked(
                    error_category.ParseError, "missing right operand \"%s\"." % self.previous.value, self.d_location(_start))
            
            _node = expr_ast(
                ast_type.BINARY_OP, self.d_location(_start), _node, _opt, _rhs)
        
        #! end
        return _node
                

    def stmnt_g1(self):
        """ COMPOUND statement.

            Returns
            -------
            ast
        """
        return self.stmnt_g2()

    def stmnt_g2(self):
        """ SIMPLE statement.

            Returns
            -------
            ast
        """
        if  self.check_both(token_type.IDENTIFIER, keywords.IMPORT):
            return self.stmnt_s0()

        #! end
        return self.stmnt_sN()

    def stmnt_s0(self):
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

        #! ';'
        self.expect_both(token_type.SYMBOL, ";")

        return stmnt_ast(
            ast_type.IMPORT, self.d_location(_start), _imports)
    

    def stmnt_sN(self):
        """ EXPRESSION_STATEMENT statement.

            Syntax
            ------
            nullable_expr ';'

            Returns
            -------
            ast
        """
        _node = self.expr_N()
        if not _node: return _node

        # ';'
        self.expect_both(token_type.SYMBOL, ";")
        
        #! end
        return stmnt_ast(
            ast_type.EXPR_STMNT, "", _node)
        
    def stmnt_g3(self):
        """ SOURCE file.

            Syntax
            ------
            stmnt_g1* EOF

            Returns
            -------
            ast
        """
        _stmnt = []

        while self.hasNext():
            _node = self.stmnt_g1()

            #! check if epsilon
            if not _node: break

            #! child node
            _stmnt.append(_node)
        
        #! eof
        self.expect_t(token_type.EOF)

        return stmnt_ast(
            ast_type.SOURCE, "", _stmnt)
    
    def hasNext(self):
        return not self.check_t(token_type.EOF)
    
    def parse(self):
        return self.stmnt_g3()
        

        


