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
    POSTFIX_INC_DEC = 22
    TERNARY       = 23
    UNARY_OP      = 24
    UNARY_INC_DEC = 25
    UNARY_UNPACK  = 26
    TRY_OP        = 27
    BINARY_OP     = 28
    SHORTC_OP     = 29
    SIMPLE_ASS    = 30
    AUGMENT_ASS   = 31
    FUNCTION      = 32
    STRUCT        = 33
    FUNCTION_WRAPPER = 34
    ENUM          = 35
    IF_STMNT      = 36
    SWITCH_STMNT  = 37
    FOR_STMNT     = 38

    IMPORT        = 100
    NATIVE_FUNCTION  = 101
    VAR_STMNT     = 102
    LET_STMNT     = 103
    CONST_STMNT   = 104
    RETURN_STMNT  = 105
    EXPR_STMNT    = 106
    SOURCE        = 107



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