
from atoken import (token_type, atoken)
from lexer import lexer
from error import (error_category, error)

from ast import (ast_type, stmnt_ast, expr_ast)

from syskey import (keywords)

class parser(object):
    """ Parser for atom.
    """

    def __init__(self, _state):
        self.state     = _state
        self.lexer     = lexer(self.state)
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
                error_category.ParseError, "unexpected stoken \"%s\". Did you mean \"%s\"??" % (self.lookahead.value, _value), self.c_location())
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

    def list_idn(self):
        """ List of identifiers.

            Returns
            -------
            tuple
        """

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
        if  self.check_both(token_type.IDENTIFIER, "import"):
            return self.stmnt_s0()

        raise Exception("Nah!")

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
    
    def hasNext(self):
        return not self.check_t(token_type.EOF)
    
    def parse(self):
        _stmnt = []

        while self.hasNext():
            _node = self.stmnt_g1()

            #! check if epsilon
            if not _node: break

            #! child node
            _stmnt.append(_node)
        
        #! eof
        self.expect_t(token_type.EOF)
        

        


