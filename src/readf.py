
from os import path as ospath

from error import (error_category, error)
from afile import afile


CONST_REQUIRED_EXT = ".as"


def file_isfile(_state, _path_to_file):
    if  not _path_to_file.endswith(CONST_REQUIRED_EXT):
        return False
    
    for _dir in _state.paths:
        _loc = ospath.abspath(ospath.join(_dir, _path_to_file))

        if  ospath.exists(_loc) and ospath.isfile(_loc):
            return True

    #! end
    return False

def read_file(_state, _file_path):

    if  not file_isfile(_state, _file_path):
        error.raise_untracked(error_category.FileNotFound, "file not found \"%s\" (No such file or dir)" % _file_path)

    for _dir in _state.paths:
        _loc = ospath.abspath(ospath.join(_dir, _file_path))

        if  ospath.exists(_loc) and ospath.isfile(_loc):
            try:
                #! prevent duplicate|circular import
                # if  ospath.basename(_loc) in _state.names:
                #     return False

                #! read
                _file = open(_loc, "r")
                _state.files.append(afile(_loc, _file.read()))

                #! close stream
                _file.close()

                #! reg
                _state.names.append(ospath.basename(_loc))

                #! end
                return True

            except IOError:
                error.raise_untracked(error_category.IOError, "file is not readable \"%s\"." % _file_path)
        #! end
    
    #! finalize
    error.raise_untracked(error_category.FileNotFound, "file not found \"%s\" (No such file or dir)." % _file_path)