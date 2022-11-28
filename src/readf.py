
from os import path as ospath

from error import (error_category, error)
from afile import afile


CONST_REQUIRED_EXT = ".as"


def read_file(_state, _file_path):

    if  not _file_path.endswith(CONST_REQUIRED_EXT):
        error.raise_untracked(error_category.IOError, "not a valid atom file \"%s\"." % _file_path)

    for _dir in _state.paths:
        _loc = ospath.abspath(ospath.join(_dir, _file_path))

        if  ospath.exists(_loc) and ospath.isfile(_loc):
            try:
                #! prevent duplicate
                if  ospath.basename(_loc) in _state.names:
                    return

                #! read
                _file = open(_loc, "r")
                _state.files.generic_push(afile(_loc, _file.read()))

                #! close stream
                _file.close()

                #! reg
                _state.names.append(ospath.basename(_loc))

                #! end
                return

            except IOError:
                error.raise_untracked(error_category.IOError, "file is not readable \"%s\"." % _file_path)
        #! end
    
    #! finalize
    error.raise_untracked(error_category.FileNotFound, "file not found \"%s\" (No such file or dir)." % _file_path)