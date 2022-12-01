
from sys import argv, setrecursionlimit
setrecursionlimit(100_000)


from astate import astate
from codegen import codegen
from virtualmachine import virtualmachine

from readf import read_file

def main():
    _state = astate()
    read_file(_state, argv[1])

    #! compile
    _cgen = codegen(_state)
    _cgen.generate()

    #! run
    _virm = virtualmachine(_state)
    _virm.run()

    #! end

main()


