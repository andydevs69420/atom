
from sys import argv

from astate import state
from parser import parser


from readf import read_file

def main():
    _state = state()
    read_file(_state, argv[1])

    _p = parser(_state)
    _p.parse()
    #! end

main()


