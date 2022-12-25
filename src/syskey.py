

class keywords:
    #! typing keywords
    INT_T    = "int"
    FLOAT_T  = "float"
    STRING_T = "string"
    BOOL_T   = "bool"
    VOID_T   = "void"
    ARRAY_T  = "array"
    FN_T     = "fn"
    MAP_T    = "map"

    #!
    SELF     = "self"
    TRUE     = "true"
    FALSE    = "false"
    NULL     = "null"
    TYPEOF   = "typeof"

    NATIVE   = "native"
    FUNCTION = "function"
    STRUCT   = "struct"
    IMPLEMENTS = "implements"
    ENUM     = "enum"
    IF       = "if"
    SWITCH   = "switch"
    CASE     = "case"
    ELSE     = "else"
    FOR      = "for"
    WHILE    = "while"
    DO       = "do"
    TRY      = "try"
    EXCEPT   = "except"
    FINALLY  = "finally"

    DEFINE   = "define"
    IMPORT   = "import"
    FROM     = "from"
    CONST    = "const"
    VAR      = "var"
    LET      = "let"
    BREAK    = "break"
    CONTINUE = "continue"
    RETURN   = "return"

    @staticmethod
    def is_keyword(_key):
        _as_dict = keywords.__dict__
        for _k, _v in zip(_as_dict.keys(), _as_dict.values()):

            if  not (_k.startswith("__") and _k.endswith("__")):
                if  _v == _key and type(_v) == str:
                    return True
        #! end
        return False


