from colorama import init, Fore

init(False, True)

import gc
from sys import argv, setrecursionlimit
setrecursionlimit(20_000)

from astate import astate
from codegen import codegen
from virtualmachine import virtualmachine
from readf import read_file
from error import error_category, error




def infomode():
    _banner =\
"""  
       /A     | GITHUB : https://github.com/andydevs69420/atom.git
      /AA\    | AUTHOR : Philipp Andrew Roa Redondo
     /AA A\   | PROJECT: Atom programming language high-fidelity prototype
    /A  AAA\  | DESCRIPTION: A prototype language for it's main implementation.

    How to run?
        ex:
            atom.exe file.as arg1 arg2
""" 
    print("%s%s%s" % (Fore.GREEN, _banner, Fore.RESET))


def main():
    #! make state
    _state = astate()
    
    print("STATE CREATED!")

    #! do info mode
    if len(argv) <= 1: return infomode()

    #! read file
    read_file(_state, argv[1])

    #! set args
    _state.aargv.extend(argv[1:])

    #! compile
    _cgen = codegen(_state)
    _cgen.generate()

    print("Compile finished...")
    gc.collect()

    #! run
    _virm = virtualmachine(_state)
    _virm.run()

    #! end

main()


