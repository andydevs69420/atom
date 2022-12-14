from enum import Enum


class ast_type(Enum):
    ANY_T         = 0
    INT_T         = 1
    FLOAT_T       = 2
    STR_T         = 3
    BOOL_T        = 4
    VOID_T        = 5
    ARRAY_T       = 6
    FN_T          = 7
    MAP_T         = 8
    TYPE_T        = 9
    INT           = 10
    FLOAT         = 11
    STR           = 12
    BOOL          = 13
    NULL          = 14
    REF           = 15
    ARRAY         = 16
    MAP           = 17
    ATTRIBUTE     = 18
    ELEMENT       = 19
    CALL_WRAPPER  = 20
    CALL          = 21
    TERNARY       = 22
    UNARY_OP      = 23
    UNARY_TYPEOF  = 24
    UNARY_UNPACK  = 25
    TRY_OP        = 26
    BINARY_OP     = 27
    SHORTC_OP     = 28
    SIMPLE_ASS    = 29
    AUGMENT_ASS   = 30
    FUNCTION      = 31
    METHOD        = 32
    STRUCT        = 33
    IMPLEMENTS    = 34
    FUNCTION_WRAPPER = 35
    ENUM          = 36
    IF_STMNT      = 37
    SWITCH_STMNT  = 38
    FOR_STMNT     = 39
    WHILE_STMNT   = 40
    DOWHILE_STMNT = 41
    TRY_EXCEPT_FINALLY = 42
    BLOCK_STMNT   = 43

    IMPORT        = 100
    FROM          = 101
    NATIVE_FUNCTION  = 102
    VAR_STMNT     = 103
    LET_STMNT     = 104
    CONST_STMNT   = 105
    ASSERT_STMNT  = 106
    BREAK_STMNT   = 107
    CONTINUE_STMNT= 108
    RETURN_STMNT  = 109
    EXPR_STMNT    = 110
    SOURCE        = 111



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