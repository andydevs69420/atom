

from error import (error_category, error)
from atoken import (token_type, atoken)

class lexer(object):
    """ Lexical analysis for atom.
    """

    def __init__(self, _state):
        self.state   = _state
        self.current = self.state.files.pop()


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
    
    def c_is_newline(self):
        return ord(self.current.clook) == 0x0a
    
    def c_is_com_start(self):
        return ord(self.current.clook) == 0x23
    
    def c_is_idn_start(self):
        _c = ord(self.current.clook)
        return (
            (_c >= 0x061 and _c <= 0x7a) or
            (_c >= 0x041 and _c <= 0x5a) or 
            (_c == 0x5f) or self.current.clook.isidentifier() # or simply use "isidentifier"
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

    #! ============= HELPERS =============
    def make_site(self, _start):
        return atoken.make_location_from_offsets(self.current.fpath, self.current.fcode, _start.ln_of, self.current.safe_line, _start.cm_of, self.current.safe_colm)

    #! ============= BUILDER =============

    def comment(self):
        _token = atoken(token_type.COMMENT, self.current.cline, self.current.ccolm)
        _token.value = self.current.clook

        self.forward()

        if  self.current.clook != '!':
            error.raise_tracked(error_category.LexicalError, "invalid comment initializer \"%s\". Did you mean \"#!\"??" % _token.value, self.make_site(_token))
        
        self.forward()

        while self.hasNext() and not self.c_is_newline():
            self.forward()
        
        #! end
        return


    def token_0(self):
        """ IDENTIFIER token.

            Returns
            -------
            atoken
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
            atoken
        """
        _token = atoken(token_type.INTEGER, self.current.cline, self.current.ccolm)
        _token.value  = ""
        _token.value += self.num_part()

        if  _token.value == '0':

            if   self.current.clook in ('x', 'X'):
                 _token.value += self.nextchr ()
                 _token.value += self.hex_part()

            elif self.current.clook in ('o', 'O'):
                 _token.value += self.nextchr ()
                 _token.value += self.oct_part()
            
            elif self.current.clook in ('b', 'B'):
                 _token.value += self.nextchr ()
                 _token.value += self.bin_part()
                
            if  len(_token.value) == 2:
                error.raise_tracked(error_category.LexicalError, "improper formed literal \"%s\"." % _token.value, self.make_site(_token))
            
            if  len(_token.value) >= 3: # > 2
                #! convert
                _token.value = str(eval(_token.value))

                #! end
                return _token
        
        #! continue
        if   self.current.clook == '.':
            _token.ttype =  token_type.FLOAT
            _token.value += self.nextchr ()

            if  not self.c_is_num_start():
                error.raise_tracked(error_category.LexicalError, "invalid float value \"%s\"." % _token.value, self.make_site(_token))
            
            #! append next [0-9]+
            _token.value += self.num_part()

        
        if   self.current.clook in ('e', 'E'):
            _token.ttype =  token_type.FLOAT
            _token.value += self.nextchr ()

            #! allow sign if truncation,
            if   self.current.clook in ('+', '-'):
                _token.value += self.nextchr ()

            if  not self.c_is_num_start():
                error.raise_tracked(error_category.LexicalError, "invalid float value while truncation\"%s\"." % _token.value, self.make_site(_token))
            
            #! append next [0-9]+
            _token.value += self.num_part()
            
        
        if  _token.ttype == token_type.FLOAT:
            _token.value  = str(float(_token.value))

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
    
    def token_2(self):
        """ STRING token.

            Returns
            -------
            atoken
        """
        _token = atoken(token_type.STRING, self.current.cline, self.current.ccolm)
        _token.value  = ""

        _o, _c = self.current.clook, None
        self.forward()

        _c = self.current.clook

        while self.hasNext() and not (_o == _c):

            if  ord(self.current.clook) == 0x0a:
                break
            
            if  ord(self.current.clook) == 0x5c:
                self.forward()

                if   self.current.clook == 'b':
                    _token.value += '\b'
                elif self.current.clook == 't':
                    _token.value += '\t'
                elif self.current.clook == 'n':
                    _token.value += '\n'
                elif self.current.clook == 'r':
                    _token.value += '\r'
                elif self.current.clook == "'":
                    _token.value += '\''
                elif self.current.clook == '"':
                    _token.value += '\"'
                else:
                    _token.value += "\\" + self.current.clook

            else:
                _token.value += self.current.clook
            
            self.forward()
            _c = self.current.clook
        
        if  _o != _c:
            error.raise_tracked(error_category.LexicalError, "string is not properly terminated %s." % repr(_token.value), self.make_site(_token))

        else:
            self.forward()
        
        #! end
        return _token

    def token_3(self):
        """ SYMBOL token.

            Returns
            -------
            atoken
        """
        _token = atoken(token_type.SYMBOL, self.current.cline, self.current.ccolm)
        _token.value = ""

        if   self.current.clook == '~':
            _token.value += self.nextchr()

            if   self.current.clook == '=':
                _token.value += self.nextchr()

        elif self.current.clook == '^':
            _token.value += self.nextchr()

            if   self.current.clook == '^':
                _token.value += self.nextchr()

            if   self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '*':
            _token.value += self.nextchr()

            if   self.current.clook == '*' or\
                 self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '/' or\
             self.current.clook == '%' or\
             self.current.clook == '+':
            _token.value += self.nextchr()

            if   self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '-':
            _token.value += self.nextchr()

            if   self.current.clook == '=':
                _token.value += self.nextchr()
            elif self.current.clook == '>':
                _token.value += self.nextchr()
        
        elif self.current.clook == '<':
            _token.value += self.nextchr()

            if   self.current.clook == '<':
                _token.value += self.nextchr()
            
            if   self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '>':
            _token.value += self.nextchr()

            if   self.current.clook == '>':
                _token.value += self.nextchr()
            
            if   self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '=' or\
             self.current.clook == '!':
            _token.value += self.nextchr()

            if   self.current.clook == '=':
                _token.value += self.nextchr()

        elif self.current.clook == '&':
            _token.value += self.nextchr()

            if   self.current.clook == '&' or\
                 self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == '|':
            _token.value += self.nextchr()

            if   self.current.clook == '|' or\
                 self.current.clook == '=':
                _token.value += self.nextchr()
        
        elif self.current.clook == ':':
            _token.value += self.nextchr()

            if   self.current.clook == ':':
                _token.value += self.nextchr()

        elif self.current.clook == '(' or\
             self.current.clook == ')' or\
             self.current.clook == '[' or\
             self.current.clook == ']' or\
             self.current.clook == '{' or\
             self.current.clook == '}' or\
             self.current.clook == '?' or\
             self.current.clook == '.' or\
             self.current.clook == '!' or\
             self.current.clook == ';' or\
             self.current.clook == ',':
            _token.value += self.nextchr()
        
        else:
            _token.value += self.nextchr()
            error.raise_tracked(error_category.LexicalError, "unknown symbol %s remove this symbol." % repr(_token.value), self.make_site(_token))

        #! end
        return _token
    
    def token_4(self):
        """ EOF token.

            Returns
            -------
            atoken
        """
        _token = atoken(token_type.EOF, self.current.cline, self.current.ccolm)
        _token.value = "eof"

        #! end
        return _token

    def getNext(self):
        while self.hasNext():

            if   self.c_is_ignorable():
                self.forward()
            
            elif self.c_is_com_start():
                self.comment()

            elif self.c_is_idn_start():
                return self.token_0()

            elif self.c_is_num_start():
                return self.token_1()
            
            elif self.c_is_str_start():
                return self.token_2()

            else:
                return self.token_3()
        
        #! eof
        return self.token_4()
    

    def nextchr(self):
        _old = self.current.clook

        self.forward()
        return _old

    def forward(self):
        if  self.c_is_newline():
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
#! END LEXER