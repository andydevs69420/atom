from enum import Enum


class ast_type(Enum):
    ANY_T        = 0
    INT_T        = 1
    FLOAT_T      = 2
    STR_T        = 3
    BOOL_T       = 4
    VOID_T       = 5
    ARRAY_T      = 6
    FN_T         = 7
    MAP_T        = 8
    USER_T       = 9
    INT          = 10
    FLOAT        = 11
    STR          = 12
    BOOL         = 13
    NULL         = 14
    REF          = 15
    ARRAY        = 16
    MAP          = 17
    ATTRIBUTE    = 18
    ELEMENT      = 19
    CALL         = 20
    UNARY_OP     = 21
    UNARY_CAST   = 22
    UNARY_UNPACK = 23
    BINARY_OP    = 24
    SHORTC_OP    = 25
    SIMPLE_ASS   = 26
    AUGMENT_ASS  = 27
    FUNCTION     = 28
    IMPORT       = 29
    VAR_STMNT    = 30
    LET_STMNT    = 31
    CONST_STMNT  = 32
    RETURN_STMNT = 33
    EXPR_STMNT   = 34
    SOURCE       = 35



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