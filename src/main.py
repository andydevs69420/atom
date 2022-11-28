
from sys import argv

from astate import state
from codegen import codegen


from readf import read_file

def main():
    _state = state()
    read_file(_state, argv[1])

    _cgen = codegen(_state)
    _cgen.generate()
    #! end

main()


