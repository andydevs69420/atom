import gc
from sys import argv, setrecursionlimit
setrecursionlimit(20_000)

from astate import astate
from codegen import codegen
from virtualmachine import virtualmachine
from readf import read_file
from error import error_category, error

def main():
    _state = astate()
    read_file(_state, argv[1])

    #! set args
    _state.aargv.extend(argv[1:])

    #! compile
    #! try:
    _cgen = codegen(_state)
    _cgen.generate()
    #! except:
    #! error.raise_untracked(error_category.CompileError, "Could not compile file dut to unhandled exception.")

    print("Compile finished...")
    gc.collect()

    #! run
    _virm = virtualmachine(_state)
    _virm.run()

    #! end

main()


