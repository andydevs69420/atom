
from sys import argv, setrecursionlimit
setrecursionlimit(100_000)


from astate import state
from codegen import codegen


from readf import read_file

def main():
    _state = state()
    read_file(_state, argv[1])

    #! compile
    _cgen = codegen(_state)
    _cgen.generate()

    #! run
    

    #! end

main()


