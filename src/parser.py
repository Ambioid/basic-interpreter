from lexer import Lexer, LETTERS, DIGITS
from tokens import Token, TokenKind
from typing import Optional
import syntax as ast

class EndLineTrigger(Exception):
    pass

class Parser:
    lexer: Lexer

    def __init__(self, lexer):
        self.lexer = lexer

    def parse_program(self) -> "Program":
        while True:
            assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
            if self.lexer.double_peek().kind in [
                TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
                TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
                TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
                TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
                TokenKind.KW_RETURN, TokenKind.KW_STOP, TokenKind.KW_FOR]:
                self.parse_block()
            elif self.lexer.double_peek().kind in [TokenKind.KW_END]:
                break
            else:
                raise AssertionError("Invalid tokenage")
        self.parse_endline()
        return

    def parse_block(self) -> "Block":
        while True:
            assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
            if self.lexer.double_peek().kind in [
                TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
                TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
                TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
                TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
                TokenKind.KW_RETURN, TokenKind.KW_STOP]:
                self.parse_line()
            elif self.lexer.double_peek().kind in [TokenKind.KW_FOR]:
                self.parse_for_block()
            else:
                break

    def parse_endline(self) -> "Endline":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value
        assert self.lexer.next() == TokenKind.KW_END
        assert self.lexer.next() == TokenKind.EOL
        return

    def parse_line(self) -> "Line":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        self.parse_statement()

        assert self.lexer.next() == TokenKind.EOL
        return        

    def parse_for_block(self) -> "ForBlock":
        self.parse_for_line()

        self.parse_for_body()
        return

    def parse_statement(self) -> "Statement":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number

        match self.lexer.double_peek().kind:
            case TokenKind.KW_DATA:
                self.parse_data_statement()
            case TokenKind.KW_DEF:
                self.parse_def_statement()
            case TokenKind.KW_DIM:
                self.parse_dimension_statement()
            case TokenKind.KW_GO:
                if self.lexer.triple_peek().kind == TokenKind.KW_SUB:
                    self.parse_gosub_statement()
                elif self.lexer.triple_peek().kind == TokenKind.KW_TO:
                    self.parse_goto_statement()
                else:
                    raise AssertionError("Invalid Go statement")
            case TokenKind.KW_IF:
                self.parse_if_then_statement()
            case TokenKind.KW_INPUT:
                self.parse_input_statement()
            case TokenKind.KW_LET:
                self.parse_let_statement()
            case TokenKind.KW_ON:
                self.parse_on_goto_statement()
            case TokenKind.KW_OPTION:
                self.parse_option_statement()
            case TokenKind.KW_PRINT:
                self.parse_print_statement()
            case TokenKind.KW_RANDOMIZE:
                self.parse_randomize_statement()
            case TokenKind.KW_READ:
                self.parse_read_statement()
            case TokenKind.KW_REM:
                self.parse_remark()
            case TokenKind.KW_RESTORE:
                self.parse_restore_statement()
            case TokenKind.KW_RETURN:
                self.parse_return_statement()
            case TokenKind.KW_STOP:
                self.parse_stop_statment()
            case _:
                raise AssertionError("Thats not a statement you fool.")

    def parse_for_line(self) -> "ForLine":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        self.parse_for_statement()

        assert self.lexer.next() == TokenKind.EOL
        return        

    def parse_for_statement(self) -> "ForStatement":
        assert self.lexer.next() == TokenKind.KW_FOR

        self.parse_control_variable()

        assert self.lexer.next() == TokenKind.SYM_EQUAL

        self.parse_initial_value()

        assert self.lexer.next() == TokenKind.KW_TO

        self.parse_limit()

        if self.lexer.peek().kind == TokenKind.KW_STEP:
            assert self.lexer.next() == TokenKind.KW_STEP

            self.parse_increment()
        return

    def parse_for_body(self) -> "ForBody":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        if self.lexer.double_peek().kind in [
            TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
            TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
            TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
            TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
            TokenKind.KW_RETURN, TokenKind.KW_STOP, TokenKind.KW_FOR]:
            self.parse_block()

        self.parse_next_line()

        return

    def parse_control_variable(self) -> "ControlVariable":
        self.parse_simple_numeric_variable()
        return

    def parse_initial_value(self) -> "InitialValue":
        self.parse_numeric_expression()
        return

    def parse_limit(self) -> "Limit":
        self.parse_numeric_expression()
        return

    def parse_increment(self) -> "Increment":
        self.parse_numeric_expression()
        return

    def parse_next_line(self) -> "NextLine":
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        self.parse_next_statement()

        assert self.lexer.next() == TokenKind.EOL

    def parse_simple_numeric_variable(self) -> "SimpleNumericVariable":
        assert self.lexer.peek().kind == TokenKind.IDENTIFIER
        tok = self.lexer.next()
        identifier = self.lexer.get_token_string(tok)
        assert identifier[0] in LETTERS

        if len(identifier) == 1:
            assert identifier[0] in LETTERS
        elif len(identifier) == 2:
            assert identifier[0] in LETTERS
            assert identifier[1] in DIGITS
        else:
            raise AssertionError("Invalid simple numeric variable, get good")
        
        return

    def parse_next_statement(self) -> "NextStatement":
        assert self.lexer.next().kind == TokenKind.KW_NEXT

        self.parse_control_variable()

        return
    
    def parse_data_statement(self) -> "DataStatement":
        assert self.lexer.next().kind == TokenKind.KW_DATA

        self.parse_data_list()
        return

    def parse_data_list(self) -> "DataList":
        self.parse_datum()

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                self.parse_datum()
            else: break

        return

    def parse_def_statement(self) -> "DefStatement":
        assert self.lexer.next().kind == TokenKind.KW_DEF

        self.parse_numeric_defined_function()

        if self.lexer.peek().kind == TokenKind.SYM_L_PAREN:
            self.parse_parameter_list()

        assert self.lexer.next().kind == TokenKind.SYM_EQUAL

        self.parse_numeric_expression()
        return

    def parse_numeric_defined_function(self) -> "NumericDefinedFunction":
        assert self.lexer.next().kind == TokenKind.KW_FN

        assert self.lexer.next().kind == TokenKind.IDENTIFIER
        tok = self.lexer.next()
        identifier = self.lexer.get_token_string(tok)
        assert identifier[0] in LETTERS
        assert len(identifier) == 1

        return

    def parse_parameter_list(self) -> "ParameterList":
        assert self.lexer.next().kind == TokenKind.SYM_L_PAREN

        self.parse_parameter()

        assert self.lexer.next().kind == TokenKind.SYM_R_PAREN

    def parse_parameter(self) -> "Parameter":
        self.parse_simple_numeric_variable()
        return

    def parse_dimension_statement(self) -> "DimensionStatement":
        assert self.lexer.next().kind == TokenKind.KW_DIM

        self.parse_array_declaration()

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                self.parse_array_declaration()

    def parse_array_declaration(self) -> "ArrayDeclaration":
        self.parse_numeric_array_name()

        assert self.lexer.next().kind == TokenKind.SYM_L_PAREN

        self.parse_bounds()

        assert self.lexer.next().kind == TokenKind.SYM_R_PAREN

    def parse_numeric_array_name(self) -> "NumericArrayName":
        assert self.lexer.next().kind == TokenKind.IDENTIFIER
        tok = self.lexer.next()
        identifier = self.lexer.get_token_string(tok)
        assert identifier[0] in LETTERS
        assert len(identifier) == 1

        return
    
    def parse_bounds(self) -> "Bounds":
        assert (bound1 := self.lexer.next().kind) == TokenKind.INTEGER

        if self.lexer.peek().kind == TokenKind.SYM_COMMA:
            self.lexer.next()
            assert (bound2 := self.lexer.next().kind) == TokenKind.INTEGER

        return
        
    def parse_gosub_statement(self) -> "GoSubStatement":
        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_SUB

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        return

    def parse_goto_statement(self) -> "GoToStatement":
        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_TO

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        return

    def parse_on_goto_statement(self) -> "OnGoToStatement":
        assert self.lexer.next().kind == TokenKind.KW_ON

        self.parse_numeric_expression()

        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_TO

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                
                assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
                line_number = self.lexer.next().value
            else:
                break
        
        return

    def parse_if_then_statement(self) -> "IfThenStatement":
        assert self.lexer.next().kind == TokenKind.KW_IF

        self.parse_relational_expression()

        assert self.lexer.next().kind == TokenKind.KW_THEN

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value        

        return

    def parse_relation(self) -> "Relation":
        tok = self.lexer.next()
        assert tok.kind in [TokenKind.SYM_EQUAL, TokenKind.SYM_NEQ, 
                            TokenKind.SYM_L_ANGLE, TokenKind.SYM_R_ANGLE,
                            TokenKind.SYM_LEQ, TokenKind.SYM_GEQ]
        rel = tok.kind
        return

    def parse_equality_relation(self) -> "EqualityRelation":
        tok = self.lexer.next()
        assert tok.kind in [TokenKind.SYM_EQUAL, TokenKind.SYM_NEQ]
        rel = tok.kind
        return

    def parse_string_expression(self) -> "StringExpression":
        pass

    def parse_input_statement(self) -> "InputStatement":
        assert self.lexer.next().kind == TokenKind.KW_INPUT

        self.parse_variable_list()

        return

    def parse_variable_list(self) -> "VariableList":
        self.parse_variable()

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                self.parse_variable()
            else:
                break

        return

    def parse_option_statement(self) -> "OptionStatement":
        assert self.lexer.next().kind == TokenKind.KW_OPTION

        assert self.lexer.next().kind == TokenKind.KW_BASE

        assert (tok := self.lexer.next().kind) == TokenKind.INTEGER
        assert tok.value in [0, 1]

        return

    def parse_randomize_statement(self) -> "RandomizeStatement":
        assert self.lexer.next().kind == TokenKind.KW_RANDOMIZE
        return

    def parse_read_statement(self) -> "ReadStatement":
        assert self.lexer.next().kind == TokenKind.KW_READ

        self.parse_variable_list()

        return

    def parse_remark(self) -> None:
        while self.lexer.next().kind != TokenKind.EOL:
            pass
        return

    def parse_restore_statement(self) -> "RestoreStatement":
        assert self.lexer.next().kind == TokenKind.KW_RESTORE
        return

    def parse_return_statement(self) -> "ReturnStatement":
        assert self.lexer.next().kind == TokenKind.KW_RETURN
        return

    def parse_stop_statment(self) -> "StopStatement":
        assert self.lexer.next().kind == TokenKind.KW_STOP
        return
    

    def parse_variable(self) -> "Variable":
        pass

    def parse_let_statement(self) -> "LetStatement":
        pass

    def parse_print_statement(self) -> "PrintStatement":
        assert self.lexer.next().kind == TokenKind.KW_PRINT
    
    def parse_relational_expression(self) -> "RelationalExpression":
        # TODO OR STRING COMP
        if (True):
            self.parse_numeric_expression()

            self.parse_relation()

            self.parse_numeric_expression()
        elif (True):
            self.parse_string_expression()

            self.parse_equality_relation()

            self.parse_string_expression()
        else:
            raise AssertionError("Not a valid expression")
        #todo later

    
    def parse_datum(self) -> "Datum":
        # Quoted string | Unquoted string
        pass

    def parse_numeric_expression(self) -> ast.NumExpr:
        pass

    def parse_term(self) -> ast.NumExpr:
        pass

    def parse_factor(self) -> ast.NumExpr:
        pass
    
    def parse_primary(self) -> ast.NumExpr:
        match self.lexer.peek().kind:
            case TokenKind.IDENTIFIER:
                pass
            case TokenKind.INTEGER:
                pass
            case TokenKind.FLOAT:
                pass
            case TokenKind.SYM_L_PAREN:
                expr = self.parse_numeric_expression()
                assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
                return expr
