from enum import Enum


class ast_type(Enum):
    INT          = 1
    FLOAT        = 2
    STR          = 3
    BOOL         = 4
    NULL         = 5
    REF          = 6
    ARRAY        = 7
    MAP          = 8
    ATTRIBUTE    = 9
    ELEMENT      = 10
    CALL         = 12
    UNARY_OP     = 13
    UNARY_CAST   = 14
    UNARY_UNPACK = 15
    BINARY_OP    = 16
    SHORTC_OP    = 17
    SIMPLE_ASS   = 18
    AUGMENT_ASS  = 19
    IMPORT       = 20
    VAR_STMNT    = 21
    LET_STMNT    = 22
    CONST_STMNT  = 23
    EXPR_STMNT   = 24
    SOURCE       = 25



class aAst(object):
    """ Base ast for atom.
    """

    def __init__(self, _type, _site):
        self.type = _type
        self.site = _site
    
    def get(self, _index): raise NotImplementedError("prototype")


class stmnt_ast(aAst):
    """ Ast for statement.

        Attributes
        ----------
        _type : ast_type
        _loc  : str
        _args : tuple

        Pattern
        -------
        stmnt_ast(TYPE, LOC, $1, $2, $3, ... $N)
    """

    def __init__(self, _type, _loc, *_arg):
        #! init default
        super().__init__(_type, _loc)

        #! init prop
        self.statements = tuple(_arg)
    
    def get(self, _index):
        return self.statements[_index]


class expr_ast(aAst):
    """ Ast for expression.

        Attributes
        ----------
        _type : ast_type
        _loc  : str
        _args : tuple

        Pattern
        -------
        expr_ast(TYPE, LOC, $1, $2, $3, ... $N)
    """

    def __init__(self, _type, _loc, *_arg):
        #! init default
        super().__init__(_type, _loc)

        #! init prop
        self.expression = tuple(_arg)

    def get(self, _index):
        return self.expression[_index]