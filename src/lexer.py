
from sys import argv, path as syspath
from os import path as ospath

from builtins import (open, len, ord)

from error import (error_category, error)
from atoken import (token_type, atoken)

class lexer(object):
    """ Lexical analysis for atom.
    """

    def __init__(self, _state):
        self.state             = _state
        self.current:lex_input = None
    
    def read_input(self, _file_path):
        for _dir in self.state.paths:
            _loc = ospath.abspath(ospath.join(_dir, _file_path))

            if  ospath.exists(_loc) and ospath.isfile(_loc):
                try:
                    #! prevent duplicate
                    if  ospath.basename(_loc) in self.state.names:
                        return

                    #! read
                    _file = open(_loc, "r")
                    self.state.files.generic_push(lex_input(_loc, _file.read()))

                    #! close stream
                    _file.close()
                    return

                except IOError as e:
                    print(e)
                    error.raise_untracked(error_category.IOError, "file is not readable \"%s\"." % _file_path)
            #! end
        
        #! finalize
        error.raise_untracked(error_category.IOError, "file not found \"%s\" (No such file or dir)." % _file_path)

    #! ============= CHECKER =============

    def c_is_ignorable(self):
        _c = ord(self.current.clook)
        return (
            (_c == 0x00) or
            (_c == 0x08) or
            (_c == 0x09) or
            (_c == 0x0a) or
            (_c == 0x0d) or
            (_c == 0x20)
        )
    
    def c_is_idn_start(self):
        _c = ord(self.current.clook)
        return (
            (_c >= 0x061 and _c <= 0x7a) or
            (_c >= 0x041 and _c <= 0x5a) or 
            (_c == 0x5f)
        )
    
    def c_is_num_start(self):
        _c = ord(self.current.clook)
        return (_c >= 0x30 and _c <= 0x39)
    
    def c_is_hex_start(self):
        _c = ord(self.current.clook)
        return (
            (_c >= 0x061 and _c <= 0x66) or
            (_c >= 0x041 and _c <= 0x46) or 
            self.c_is_num_start()
        )
    
    def c_is_oct_start(self):
        _c = ord(self.current.clook)
        return (_c >= 0x30 and _c <= 0x37)
    
    def c_is_bin_start(self):
        _c = ord(self.current.clook)
        return (_c == 0x30 or _c == 0x31)
    
    def c_is_str_start(self):
        _c = ord(self.current.clook)
        return (_c == 0x22 or _c == 0x27)

    #! ============= BUILDER =============

    def token_0(self):
        """ IDENTIFIER token.

            Returns
            -------
            token
        """
        _token = atoken(token_type.IDENTIFIER, self.current.cline, self.current.ccolm)
        _token.value  = ""
        _token.value += self.idn_strt()
        _token.value += self.idn_part()

        #! end
        return _token
    
    def idn_strt(self):
        _idn = ""
        while self.hasNext() and self.c_is_idn_start():
            _idn += self.nextchr()

        #! end
        return _idn

    def idn_part(self):
        _idn = ""
        while self.hasNext() and (self.c_is_idn_start() or self.c_is_num_start()):
            _idn += self.nextchr()

        #! end
        return _idn

    def token_1(self):
        """ NUMBER token.

            ex
            --
            0xff -> INTEGER token

            0o23 -> INTEGER token

            0b10 -> INTEGER token

            2.2  -> FLOAT token

            2e+2 -> FLOAT token

            Returns
            -------
            token
        """
        _token = atoken(token_type.INTEGER, self.current.cline, self.current.ccolm)
        _token.value  = ""
        _token.value += self.num_part()

        if  _token.value == '0':
            _token.value += self.nextchr()

            if   _token.value in ('x', 'X'):
                 _token.value += self.nextchr ()
                 _token.value += self.hex_part()

            elif _token.value in ('o', 'O'):
                 _token.value += self.nextchr ()
                 _token.value += self.oct_part()
            
            elif _token.value in ('b', 'B'):
                 _token.value += self.nextchr ()
                 _token.value += self.bin_part()
                
            if  len(_token.value) == 2:
                return ...
        
        #! continue
        if  self.current.clook == '.':
            _token.value += self.nextchr ()

            

        #! end
        return _token
    
    def num_part(self):
        _num = ""
        while self.hasNext() and self.c_is_num_start():
            _num += self.nextchr()

        #! end
        return _num
    
    def hex_part(self):
        _hex = ""
        while self.hasNext() and self.c_is_hex_start():
            _hex += self.nextchr()

        #! end
        return _hex
    
    def oct_part(self):
        _oct = ""
        while self.hasNext() and self.c_is_oct_start():
            _oct += self.nextchr()

        #! end
        return _oct
    
    def bin_part(self):
        _bin = ""
        while self.hasNext() and self.c_is_bin_start():
            _bin += self.nextchr()

        #! end
        return _bin

    def getNext(self):
        assert not self.state.files.isempty(), "no input!"

        self.current = self.state.files.peek()

        while self.hasNext():

            if   self.c_is_ignorable():
                self.forward()

            elif self.c_is_idn_start():
                return self.token_0()

            elif self.c_is_num_start():
                return self.token_1()
        
        #! eof
        return
    

    def nextchr(self):
        _old = self.current.clook

        self.forward()
        return _old

    def forward(self):
        if  ord(self.current.clook) == 0x0a:
            self.current.safe_line = self.current.cline
            self.current.safe_colm = self.current.ccolm

            self.current.cline += 1
            self.current.ccolm  = 1

        else:
            self.current.ccolm += 1
        
        self.current.index += 1
        self.current.clook  = '\0' if not self.hasNext() else self.current.fcode[self.current.index]

    def hasNext(self):
        return self.current.index < len(self.current.fcode)


class lex_input(object):
    """ Input for lexical analysis.
    """

    def __init__(self, _file, _code):
        self.fpath = _file
        self.fcode = _code
        self.clook = '\0' if len(self.fcode) <= 0 else self.fcode[0]
        self.index = 0
        self.cline = 1
        self.ccolm = 1
        self.safe_line = 1
        self.safe_colm = 1

#! END LEXER