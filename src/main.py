
from sys import argv, path as syspath
from os import path as ospath

from astate import state
from lexer import lexer

def main():
    _state = state()
    x = lexer(_state)
    x.read_input(argv[1])
    print(x.getNext())
    #! end

main()


