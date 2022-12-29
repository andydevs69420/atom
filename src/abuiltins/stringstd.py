from aobjects import *
from atyping import *
from error import (error_category, error)

from inlineparser.intparser import parseInt
from inlineparser.floatparser import floatParse

from mem import atom_object_new_with_return

#! ========================== utf
""" USES Binary to easily understand.
"""

_1BYTE_UTF = 0b00000000
_2BYTE_UTF = 0b11000000
_3BYTE_UTF = 0b11100000
_4BYTE_UTF = 0b11110000


_2BYTE_FOLLOW = 0b00011111
_3BYTE_FOLLOW = 0b00001111
_4BYTE_FOLLOW = 0b00000111

_VALID_TRAIL_BYTE   = 0b10000000
_MAXIMUM_TRAIL_BYTE = 0b00111111


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
    elif _codepoint < 0x110000:
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
            (_codepoint & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
        )

    elif _size == 3:
        #! 1st byte
        _sequence.append(
            (_codepoint >> 12) | _3BYTE_UTF
        )
        #! 2nd byte
        _sequence.append(
            ((_codepoint >> 6) & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
        )
        #! 3rd byte
        _sequence.append(
            (_codepoint & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
        )
    
    elif _size == 4:
        #! 1st byte
        _sequence.append(
            (_codepoint >> 18) | _4BYTE_UTF
        )
        #! 2nd byte
        _sequence.append(
            ((_codepoint >> 12) & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
        )
        #! 3rd byte
        _sequence.append(
            ((_codepoint >> 6) & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
        )
        #! 4th byte
        _sequence.append(
            (_codepoint & _MAXIMUM_TRAIL_BYTE) | _VALID_TRAIL_BYTE
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
            _ord |= (_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BYTE)
            _index += 2
        
        elif _size == 3:
            _ord  = (_code_points_array[_index] & _3BYTE_FOLLOW) << 12
            _ord |= ((_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BYTE) << 6)
            _ord |= (_code_points_array[_index + 2] & _MAXIMUM_TRAIL_BYTE)
            _index += 3
        
        elif _size == 4:
            _ord  = (_code_points_array[_index] & _4BYTE_FOLLOW) << 18
            _ord |= ((_code_points_array[_index + 1] & _MAXIMUM_TRAIL_BYTE) << 12)
            _ord |= ((_code_points_array[_index + 2] & _MAXIMUM_TRAIL_BYTE) << 6)
            _ord |= (_code_points_array[_index + 3] & _MAXIMUM_TRAIL_BYTE)
            _index += 4
    
        _str += chr(_ord)
    
    return _str


def is_hex(_char):
    return is_hex_alpha(_char) or is_hex_numeric(_char)

def is_hex_alpha(_char):
    _chr = ord(_char)
    return (
        (_chr >= 0x41 and _chr <= 0x46) or
        (_chr >= 0x61 and _chr <= 0x66)
    )

def is_hex_numeric(_char):
    _chr = ord(_char)
    return (_chr >= 0x30 and _chr <= 0x39)

def get_hex_char_value(_hex_char):
    assert is_hex(_hex_char)
            # a   b   c   d   e   f 
    _alpha = [10, 11, 12, 13, 14, 15]

    if  is_hex_alpha(_hex_char):
        _ord = ord(_hex_char.upper())
        return _alpha[(_ord  % 16) - 1]
    
    #!
    return int(_hex_char)


def codepoint_to_hex(_codepoint_part:int):
    _alpha = ['a', 'b', 'c', 'd', 'e', 'f']

    _result = _codepoint_part
    _string = "\\x"
    _prev = 0
    
    while True:
        _prev = _result
        _result //= 16

        if  _result <= 0: break

        if  _result >= 10:
            _string += _alpha[_result - 10]

        else:
            _string += str(_result)

        _prev = _prev % 16

        #! remaining
        if  _prev >= 10:
            _string += _alpha[_prev - 10]

        else:
            _string += str(_prev)

    return _string

def is_valid_byte(_byte:int):
    return (_byte | 255) == 255

def is_valid_start_byte(_size, _byte):

    if  _size == 2:
        return (_byte | _2BYTE_UTF) == _2BYTE_UTF
    elif _size == 3:
        return (_byte | _3BYTE_UTF) == _3BYTE_UTF
    elif _size == 4:
        return (_byte | _4BYTE_UTF) == _4BYTE_UTF
    
    raise

def is_valid_trailbyte(_trail:int):
    return (_trail >= 0) and ((_trail & _VALID_TRAIL_BYTE) == _VALID_TRAIL_BYTE);




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

        "fromcharcodepoints": nativefn_t(string_t(), 1, [
            ("__codepoints__", array_t(integer_t())), 
        ]), 

        "tohexstring": nativefn_t(string_t(), 1, [
            ("__codepoints__", array_t(integer_t())), 
        ]), 

        "atoi": nativefn_t(integer_t(), 1, [
            ("__string__", string_t()), 
        ]), 

        "atof": nativefn_t(float_t(), 1, [
            ("__string__", string_t()), 
        ]), 

        "strformat": nativefn_t(string_t(), 2, [
            ("_format", string_t()), 
            ("_format_list", array_t(any_t()))
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

            case "fromcharcodepoints":
                return stringstd.fromcharcodepoints
            
            case "charcodepoints":
                return stringstd.charcodepoints

            case "tohexstring":
                return stringstd.tohexstring

            case "atoi":
                return stringstd.atoi
            
            case "atof":
                return stringstd.atof

            case "strformat":
                return stringstd.strformat

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
        return aarray(*[atom_object_new_with_return(_state, astring(_str)) for _str in _string.split(__delimeter__.raw)])

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
            elif _utf_size > 1 and _utf_size <= 4:
                _codepoints.extend(split_code_points(ord(_each_char)))
            else:
                error.raise_fromstack(error_category.UtfError, "invalid utf %s." % _string, _state.stacktace)
        
        return aarray(*[atom_object_new_with_return(_state, ainteger(_int)) for _int in _codepoints])

    @staticmethod
    def fromcharcodepoints(_state, __codepoints__):
        #! validate sequence

        _pure_array = [_int.raw for _int in __codepoints__.array]

        _idx = 0
        while _idx < len(_pure_array):

            _size = get_head_size(_pure_array[_idx])

            if  not is_valid_byte(_pure_array[_idx]):
                error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)

            if  _size == 1:
                if  is_valid_trailbyte(_pure_array[_idx]):
                    error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)
                #! 
                _idx += 1
                continue

            elif _size > 1:
                if  not is_valid_start_byte(_size, _pure_array[_idx]):
                    error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence %d, ..., ..., ." % (_size, _pure_array[_idx]) , _state.stacktrace)

                _score = 1
                _follow_index = _idx + 1

                for _trailing_index in range(_follow_index, len(_pure_array)):

                    if  is_valid_trailbyte(_pure_array[_trailing_index]):
                        _score += 1
                    
                if  _score != _size:
                    error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)

                _idx += _score

        return astring(build_from_code_points(_pure_array))

    @staticmethod
    def tohexstring(_state, __codepoints__):
        _pure_array = [_int.raw for _int in __codepoints__.array]
    
        _hexstr = ""

        _idx = 0
        while _idx < len(_pure_array):

            _size = get_head_size(_pure_array[_idx])

            if  not is_valid_byte(_pure_array[_idx]):
                error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)

            if  _size == 1:
                _hexstr += codepoint_to_hex(_pure_array[_idx])

                if  is_valid_trailbyte(_pure_array[_idx]):
                    error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)
                #! 
                _idx += 1
                continue

            elif _size > 1:
                _hexstr += codepoint_to_hex(_pure_array[_idx])

                _score = 1
                _follow_index = _idx + 1

                for _trailing_index in range(_follow_index, len(_pure_array)):
                    _hexstr += codepoint_to_hex(_pure_array[_trailing_index])

                    if  is_valid_trailbyte(_pure_array[_trailing_index]):
                        _score += 1
                    
                if  _score != _size:
                    error.raise_fromstack(error_category.UtfError, "invalid %d byte utf-8 sequence." % _size, _state.stacktrace)

                _idx += _score
        
        #!
        return astring(_hexstr)

    @staticmethod
    def atoi(_state, __string__):
        _string = parseInt(__string__.raw)

        if  not _string:
            error.raise_fromstack(error_category.NumberFormatError, "invalid integer string format (%s)." % __string__.raw, _state.stacktrace)
        
        return ainteger(_string)

    @staticmethod
    def atof(_state, __string__):
        _string = floatParse(__string__.raw)

        if  not _string:
            error.raise_fromstack(error_category.NumberFormatError, "invalid float string format (%s)." % __string__.raw, _state.stacktrace)
        
        return afloat(_string)

    @staticmethod
    def strformat(_state, _format, _format_list):
        _fmt = ""
        _tofmt = _format.raw

        _idx = 0
        _slots = 0

        _bracket_stack = []

        while _idx < len(_tofmt):

            _char = _tofmt[_idx]
            
            if  _char == "{":
                _bracket_stack.append(_char)
                _slots += 1

                if _slots > len(_format_list.array): break

                _fmt += _format_list.array[_slots - 1].__str__()
               
            elif _char == "}":
                if  len(_bracket_stack) > 0:
                    _bracket_stack.pop()

                    _idx += 1
                    #! next
                    continue

                #! regular char
                _fmt += _char

            else:
                _fmt += _char
            
            _idx += 1
        
        if  _slots != len(_format_list.array):
            error.raise_fromstack(error_category.StringFormatError, "Not all slots has been formatted, required %d, got %d." % (_slots, len(_format_list.array)), _state.stacktrace)
        
        return astring(_fmt)