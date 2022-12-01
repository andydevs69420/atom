



class agc:

    @staticmethod
    def markroot(_state):
        if  not _state.gcroot:
            return
        
        _state.gcroot.markbit = 1

    @staticmethod
    def markobject(_state, _object):
        #! make root if empty
        if  _state.gcroot == None:
            _object.markbit = 1
            _state .gcroot  = _object
            
            #! end
            return

        _object.markbit = 1
        _object.gcnext  = _state.gcroot
        _state .gcroot  = _object
    
    @staticmethod
    def markstack(_state):
        _state.gcroot = 2
    
    @staticmethod
    def markopstack(_state):
        _state.gcroot = 2

