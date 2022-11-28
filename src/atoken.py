from enum import Enum
from builtins import repr

class token_type(Enum):
    COMMENT    = 0x00
    IDENTIFIER = 0x01
    INTEGER    = 0x02
    FLOAT      = 0x03
    STRING     = 0x04
    SYMBOL     = 0x05
    EOF        = 0x06


class atoken(object):
    """ Token for atom.
    """

    def __init__(self, _ttype, _line_offset, _colm_offset):
        self.ttype = _ttype
        self.value = None
        self.ln_of = _line_offset
        self.cm_of = _colm_offset

    def __str__(self):
        return "Token(type: %s, value: %s);" % (self.ttype.name, repr(self.value))
    
    @staticmethod
    def make_location_from_offsets(_file, _code, _line_start, _line_end, _colm_start, _colm_end):
        #! ensure valid line length
        _line_end = _line_start if _line_end < _line_start else _line_end

        _lines = _code.split("\n")
        _paddN = 3

        _stx = 0 if ((_line_start - 1) - _paddN) < 0 else ((_line_start - 1) - _paddN)
        _end = (len(_lines) - 1) if (_line_end + _paddN) > len(_lines) else (_line_end + _paddN)

        _print_lines = _lines[_stx:_end]

        _format = "-At %s:%d:%d\n" % (_file, _line_start, _colm_start)

        for _idx in range(len(_print_lines)):

            _wsdiff =  len(str(_end)) - len(str((_idx + 1) + _stx))
            _format += "%s%d |" % ((' ' * _wsdiff), (_idx + 1) + _stx)

            if  ((_idx + 1) + _stx) >= _line_start and ((_idx + 1) + _stx) <= _line_end:
                _format += "> "
            else:
                _format += "  "

            _format += _print_lines[_idx]

            if  _idx < (len(_print_lines) - 1):
                _format += "\n"


        #! end
        return _format