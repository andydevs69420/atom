

from readf import read_file
from parser import parser


class generator(object):
    """ Base code generator for atom.
    """

    def __init__(self):
        self.locals = 0

    #! =========== VISITOR ===========
    
    def visit(self, _node):
        #! make visitor
        _visitor = getattr(self, "ast_" + _node.type.name.lower(), self.error)

        #! end
        return _visitor(_node)
    
    def error(self, _node):
        raise AttributeError("unimplemented node no# %d a.k.a %s!!!" % (_node.type.value, _node.type.name))
    
    #! =========== AST TREE ==========

    def ast_source(self, _node):
        print(_node)
        for _each_node in _node.statements[0]:
            self.visit(_each_node)



class codegen(generator):
    """ Analyzer and byte-code like generator for atom.
    """

    def __init__(self, _state):
        super().__init__()

        #! init prop
        self.__state = _state
        self.gparser = parser(self.__state)
    
    def ast_import(self, _node):

        for _each_import in _node.statements[0]:

            #! read file first
            read_file(self.__state, _each_import + ".as")

            print(_each_import)
    
    def generate(self):
        return self.visit(self.gparser.parse())

