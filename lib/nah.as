    def ast_if_stmnt(self, _node):
        """ 
               $0        $1        $2
            condition  statement  else
        """

        if  _node.get(0).type == ast_type.SHORTC_OP:
            self.if_with_short_circuiting(_node)
        else:
            self.if_using_normal_condition()
    
    def if_with_short_circuiting(self, _node):
        """ If statement that uses logical (&& or ||) as condition operator.
        """
       
        _condtition = _node.get(0)

        _op = _condtition.get(1)

        #! compile rhs
        self.visit(_condtition.get(2))

        _jump_loc = ...
        if  _op == "&&":
            #! when logical and(&&). both operands
            #! must evaluate to true.
            #! if any operand produces false, 
            #! then the condition is false.
            #! so jump to else without evaluating lhs.
            _jump_loc =\
            emit_opcode(self, jump_if_false, TARGET)

            #! pop rhs if its true.
            emit_opcode(self, pop_top)
        
        else:
            #! when logical or(||), atleast 1 operand
            #! produces true to make the condition satisfiable.
            #! IF rhs produces true. do not evaluate lhs
            _jump_loc =\
            emit_opcode(self, jump_if_true, TARGET)

            #! pop rhs if its true.
            emit_opcode(self, pop_top)
        
        #! compile lhs
        self.visit(_condtition.get(0))

        #! if lhs evaluates to false for
        #! both operand. jump to else
        _to_else =\
        emit_opcode(self, jump_if_false, TARGET)

        #! pop lhs if its true.
        emit_opcode(self, pop_top)
        
        #! compile statement
        self.visit(_node.get(1))
        
        #! jump to end if
        _jump_to_end =\
        emit_opcode(self, jump_to, TARGET)

        #! IF FALSE
        _jump_loc[2] = get_byteoff(self)

        _to_else[2] = get_byteoff(self)

        #! compile if has else
        if  _node.get(2):
            self.visit(_node.get(2))

        #! END IF
        _jump_to_end[2] = get_byteoff(self)