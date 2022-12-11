from aobjects import *
from atyping import *
from error import (error_category, error)



#! ========================== utf
""" USES Binary to easily understand.
"""

#! MASK
_1BYTE_UTF = 0b00000000
_2BYTE_UTF = 0b11000000
_3BYTE_UTF = 0b11100000
_4BYTE_UTF = 0b11110000


_2BYTE_FOLLOW = 0b00011111
_3BYTE_FOLLOW = 0b00001111
_4BYTE_FOLLOW = 0b00000111

_VALID_TRAIL_BIT   = 0b10000000
_MAXIMUM_TRAIL_BIT = 0b00111111


def get_head_size(_codepoint_part:int):
    if  (_codepoint_part & _4BYTE_UTF) == _4BYTE_UTF:
        return 4
    if  (_codepoint_part & _3BYTE_UTF) == _3BYTE_UTF:
        return 3
    if  (_codepoint_part & _2BYTE_UTF) == _2BYTE_UTF:
        return 2
    if  (_codepoint_part & _1BYTE_UTF) == _1BYTE_UTF:
        return 1
    #! end
    return 0

def getUtfSize(_codepoint:int):
    if   _codepoint < 0x000080:
        return 1
    elif _codepoint < 0x000800:
        return 2
    elif _codepoint < 0x010000:
        return 3
    elif _codepoint < 0x10FFFF:
        return 4
    #! end
    return 0


def split_code_points(_codepoint:int):
    _size = getUtfSize(_codepoint)

    _sequence = []

    if  _size == 2:
        #! 1st byte
        _sequence.append(
            (_codepoint >> 6) | _2BYTE_UTF
        )
        #! 2nd byte
        _sequence.append(
            (_codepoint & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )

    elif _size == 3:
        #! 1st byte
        _sequence.append(
            (_codepoint >> 12) | _3BYTE_UTF
        )
        #! 2nd byte
        _sequence.append(
            ((_codepoint >> 6) & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )
        #! 3rd byte
        _sequence.append(
            (_codepoint & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )
    
    elif _size == 4:
        #! 1st byte
        _sequence.append(
            (_codepoint >> 18) | _4BYTE_UTF
        )
        #! 2nd byte
        _sequence.append(
            ((_codepoint >> 12) & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )
        #! 3rd byte
        _sequence.append(
            ((_codepoint >> 6) & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )
        #! 4th byte
        _sequence.append(
            (_codepoint & _MAXIMUM_TRAIL_BIT) | _VALID_TRAIL_BIT
        )

    return _sequence


def build_from_code_points(_code_points_array:list[int]):
    _index = 0


    _str = ""

    while _index < len(_code_points_array):
        _ord = 0
        _size = get_head_size(_code_points_array[_index])

        if  _size == 1:
            _ord = _code_points_array[_index]
            _index += 1
        
        elif _size == 2:
            _ord  = (_code_points_array[_index] & _2BYTE_FOLLOW) << 6
            _ord |= (_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BIT)
            _index += 2
        
        elif _size == 3:
            _ord  = (_code_points_array[_index] & _3BYTE_FOLLOW) << 12
            _ord |= ((_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BIT) << 6)
            _ord |= (_code_points_array[_index + 2] & _MAXIMUM_TRAIL_BIT)
            _index += 3
        
        elif _size == 4:
            _ord  = (_code_points_array[_index] & _4BYTE_FOLLOW) << 18
            _ord |= ((_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BIT) << 12)
            _ord |= ((_code_points_array[_index + 2] & _MAXIMUM_TRAIL_BIT) << 6)
            _ord |= (_code_points_array[_index + 3] & _MAXIMUM_TRAIL_BIT)
            _index += 4
        
        _str += chr(_ord)
    
    return _str

class stringstd:

    metadata = ({

        "strlen": nativefn_t(integer_t() , 1, [
            ("__string__", string_t()), 
        ]), 

        "strtoupper": nativefn_t(string_t() , 1, [
            ("__string__", string_t()), 
        ]), 

        "strtolower": nativefn_t(string_t() , 1, [
            ("__string__", string_t()), 
        ]), 

        "strsplit": nativefn_t(array_t(string_t()), 2, [
            ("__string__"   , string_t()), 
            ("__delimeter__", string_t()), 
        ]), 

        "strreverse": nativefn_t(string_t(), 1, [
            ("__string__", string_t()), 
        ]), 

        "strrepeat": nativefn_t(string_t(), 2, [
            ("__string__", string_t()), 
            ("__times__" , integer_t()), 
        ]), 

        "charcodepoints": nativefn_t(array_t(integer_t()) , 1, [
            ("__string__", string_t()), 
        ]), 

    })

    @staticmethod
    def hasmeta(_attribute):
        return _attribute in stringstd.metadata.keys()
    
    @staticmethod
    def getmeta(_attribute):
        assert stringstd.hasmeta(_attribute), "invalid std!"
        return stringstd.metadata[_attribute]
    
    @staticmethod
    def get(_attribute):
        match _attribute:
            case "strlen":
                return stringstd.strlen
            
            case "strtoupper":
                return stringstd.strtoupper
            
            case "strtolower":
                return stringstd.strtolower

            case "strsplit":
                return stringstd.strsplit
            
            case "strreverse":
                return stringstd.strreverse
            
            case "strrepeat":
                return stringstd.strrepeat

            case "charcodepoints":
                return stringstd.charcodepoints
            
            case _:
                raise AttributeError("No such attribute \"%s\"" % _attribute)

    @staticmethod
    def strlen(_state, __string__):
        return ainteger(len(__string__.raw))
    
    @staticmethod
    def strtoupper(_state, __string__):
        return astring(__string__.raw.upper())

    @staticmethod
    def strtolower(_state, __string__):
        return astring(__string__.raw.lower())
    
    @staticmethod
    def strsplit(_state, __string__, __delimeter__):
        _string = __string__.raw

        #! end
        return aarray(*[astring(_str) for _str in _string.split(__delimeter__.raw)])

    @staticmethod
    def strreverse(_state, __string__):
        return astring(__string__.raw[::-1])
    
    @staticmethod
    def strrepeat(_state, __string__, __times__):
        return astring(__string__.raw * __times__.raw)

    @staticmethod
    def charcodepoints(_state, __string__):
        _string = __string__.raw

        _codepoints = []

        #! iter
        for _each_char in _string:
            _utf_size = getUtfSize(ord(_each_char))

            if  _utf_size == 1:
                _codepoints.append(ord(_each_char))
            elif _utf_size > 1:
                _codepoints.extend(split_code_points(ord(_each_char)))
            else:
                error.raise_fromstack(error_category.UtfError, "invalid utf %s." % _string, _state.stacktace)

        return aarray(*_codepoints)

