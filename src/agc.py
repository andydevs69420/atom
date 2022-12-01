



class gc:

    @staticmethod
    def mark_root(_state):
        _state.gcroot.markbit = 1

    @staticmethod
    def mark_object(_state, _object):
        _object.markbit = 1
        _object.gcnext  = _state.gcroot
        _state.gcroot   = _object
    
    @staticmethod
    def mark_stack(_state):
        _state.gcroot = 2
    
    @staticmethod
    def mark_opstack(_state):
        _state.gcroot = 2

