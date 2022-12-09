
class operation:
  
    @staticmethod
    def op_any_t():
        from . import any_t
        return any_t()

    @staticmethod
    def op_integer_t():
        from . import integer_t
        return integer_t()

    @staticmethod
    def op_signedbyte_t():
        from . import signedbyte_t
        return signedbyte_t()
    
    @staticmethod
    def op_signedshort_t():
        from . import signedshort_t
        return signedshort_t()
    
    @staticmethod
    def op_signedint_t():
        from . import signedint_t
        return signedint_t()
    
    @staticmethod
    def op_signedlong_t():
        from . import signedlong_t
        return signedlong_t()
    
    @staticmethod
    def op_signedbigint_t():
        from . import signedbigint_t
        return signedbigint_t()
    
    @staticmethod
    def op_float_t():
        from . import float_t
        return float_t()
    
    @staticmethod
    def op_float32_t():
        from . import float32_t
        return float32_t()
    
    @staticmethod
    def op_float64_t():
        from . import float64_t
        return float64_t()
    
    @staticmethod
    def op_string_t():
        from . import string_t
        return string_t()
    
    @staticmethod
    def op_boolean_t():
        from . import boolean_t
        return boolean_t()
    
    @staticmethod
    def op_null_t():
        from . import null_t
        return null_t()
    
    @staticmethod
    def op_array_t(_internal):
        from . import array_t
        return array_t(_internal)
    
    @staticmethod
    def op_fn_t(_returntype, _paramcount, _parameters):
        from . import fn_t
        return fn_t(_returntype, _paramcount, _parameters)
    
    @staticmethod
    def op_nativefn_t(_returntype, _paramcount, _parameters):
        from . import nativefn_t
        return nativefn_t(_returntype, _paramcount, _parameters)
    
    @staticmethod
    def op_map_t(_key, _val):
        from . import map_t
        return map_t(_key, _val)
    
    @staticmethod
    def op_error_t():
        from . import error_t
        return error_t()





