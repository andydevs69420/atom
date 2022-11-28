

class afile(object):
    """ Input file for atom.
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
