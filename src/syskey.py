

class keywords:

    TRUE   = "true"
    FALSE  = "false"
    NULL   = "null"
    IMPORT = "import"
    CONST  = "const"
    VAR    = "var"
    LET    = "let"


    @staticmethod
    def is_keyword(_key):
        _as_dict = keywords.__dict__
        for _k, _v in zip(_as_dict.keys(), _as_dict.values()):

            if  not (_k.startswith("__") and _k.endswith("__")):
                if  _v == _key and type(_v) == str:
                    return True
        
        #! end
        return False


