from lexer import Lexer, LETTERS, DIGITS
from tokens import Token, TokenKind
from typing import List, Tuple, Optional
import syntax as ast

class EndLineTrigger(Exception):
    pass

class Parser:
    lexer: Lexer

    def __init__(self, lexer):
        self.lexer = lexer

    def parse_program(self) -> ast.Program:
        statements = []
        while True:
            assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
            if self.lexer.double_peek().kind in [
                TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
                TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
                TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
                TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
                TokenKind.KW_RETURN, TokenKind.KW_STOP, TokenKind.KW_FOR]:
                statements.extend(self.parse_block())
            elif self.lexer.double_peek().kind in [TokenKind.KW_END]:
                self.parse_endline()
                break
            else:
                raise AssertionError("Invalid tokenage")
        self.parse_endline()
        return ast.Program(statements)

    def parse_block(self) -> List[ast.Block]:
        statements = []
        while True:
            assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
            if self.lexer.double_peek().kind in [
                TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
                TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
                TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
                TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
                TokenKind.KW_RETURN, TokenKind.KW_STOP]:
                statements.append(self.parse_line())
            elif self.lexer.double_peek().kind in [TokenKind.KW_FOR]:
                statements.append(self.parse_for_block())
            else:
                break
        return statements

    def parse_endline(self) -> None:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value
        assert self.lexer.next() == TokenKind.KW_END
        assert self.lexer.next() == TokenKind.EOL
        return

    def parse_line(self) -> ast.Line:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        statement = self.parse_statement()

        assert self.lexer.next() == TokenKind.EOL
        return ast.Line(line_number, statement)

    def parse_for_block(self) -> ast.ForBlock:
        line_number, control, init, limit, inc = self.parse_for_line()

        body = self.parse_for_body()
        return ast.ForBlock(line_number, control, init, limit, inc, body)

    def parse_statement(self) -> ast.Stmt:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number

        match self.lexer.double_peek().kind:
            case TokenKind.KW_DATA:
                return self.parse_data_statement()
            case TokenKind.KW_DEF:
                return self.parse_def_statement()
            case TokenKind.KW_DIM:
                return self.parse_dimension_statement()
            case TokenKind.KW_GO:
                if self.lexer.triple_peek().kind == TokenKind.KW_SUB:
                    return self.parse_gosub_statement()
                elif self.lexer.triple_peek().kind == TokenKind.KW_TO:
                    return self.parse_goto_statement()
                else:
                    raise AssertionError("Invalid Go statement")
            case TokenKind.KW_IF:
                return self.parse_if_then_statement()
            case TokenKind.KW_INPUT:
                return self.parse_input_statement()
            case TokenKind.KW_LET:
                return self.parse_let_statement()
            case TokenKind.KW_ON:
                return self.parse_on_goto_statement()
            case TokenKind.KW_OPTION:
                return self.parse_option_statement()
            case TokenKind.KW_PRINT:
                return self.parse_print_statement()
            case TokenKind.KW_RANDOMIZE:
                return self.parse_randomize_statement()
            case TokenKind.KW_READ:
                return self.parse_read_statement()
            # case TokenKind.KW_REM:
            #     self.parse_remark()
            #     return None
            case TokenKind.KW_RESTORE:
                return self.parse_restore_statement()
            case TokenKind.KW_RETURN:
                return self.parse_return_statement()
            case TokenKind.KW_STOP:
                return self.parse_stop_statment()
            case _:
                raise AssertionError("Thats not a statement you fool.")

    def parse_for_line(self) -> Tuple[int, ast.SimpleNumVar, ast.NumExpr, ast.NumExpr, Optional[ast.NumExpr]]:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        control, init, limit, inc = self.parse_for_statement()

        assert self.lexer.next() == TokenKind.EOL
        return (line_number, control, init, limit, inc)

    def parse_for_statement(self) -> Tuple[ast.SimpleNumVar, ast.NumExpr, ast.NumExpr, Optional[ast.NumExpr]]:
        assert self.lexer.next() == TokenKind.KW_FOR

        control = self.parse_control_variable()

        assert self.lexer.next() == TokenKind.SYM_EQUAL

        init = self.parse_initial_value()

        assert self.lexer.next() == TokenKind.KW_TO

        limit = self.parse_limit()

        inc = None
        if self.lexer.peek().kind == TokenKind.KW_STEP:
            assert self.lexer.next() == TokenKind.KW_STEP
            inc = self.parse_increment()

        return (control, init, limit, inc)

    def parse_for_body(self) -> ast.Block:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        if self.lexer.double_peek().kind in [
            TokenKind.KW_DATA, TokenKind.KW_DEF, TokenKind.KW_DIM, TokenKind.KW_GO,
            TokenKind.KW_IF, TokenKind.KW_INPUT, TokenKind.KW_LET, TokenKind.KW_ON,
            TokenKind.KW_OPTION, TokenKind.KW_PRINT, TokenKind.KW_RANDOMIZE,
            TokenKind.KW_READ, TokenKind.KW_REM, TokenKind.KW_RESTORE, 
            TokenKind.KW_RETURN, TokenKind.KW_STOP, TokenKind.KW_FOR]:
            block = self.parse_block()

        self.parse_next_line()

        return block

    def parse_control_variable(self) -> ast.SimpleNumVar:
        return self.parse_simple_numeric_variable()
        
    def parse_initial_value(self) -> ast.NumExpr:
        return self.parse_numeric_expression()
        
    def parse_limit(self) -> ast.NumExpr:
        return self.parse_numeric_expression()
        
    def parse_increment(self) -> ast.NumExpr:
        return self.parse_numeric_expression()

    def parse_next_line(self) -> None:
        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        self.parse_next_statement()
        assert self.lexer.next() == TokenKind.EOL
        return

    def parse_simple_numeric_variable(self) -> ast.SimpleNumVar:
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
        
        return ast.SimpleNumVar(identifier)

    def parse_next_statement(self) -> None:
        assert self.lexer.next().kind == TokenKind.KW_NEXT

        self.parse_control_variable()
        return
    
    def parse_data_statement(self) -> ast.Data:
        assert self.lexer.next().kind == TokenKind.KW_DATA

        data = self.parse_data_list()
        return ast.Data(data)

    def parse_data_list(self) -> List[ast.Datum]:
        data = []
        data.append(self.parse_datum())

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                data.append(self.parse_datum())
            else: break

        return data

    def parse_def_statement(self) -> ast.Def:
        assert self.lexer.next().kind == TokenKind.KW_DEF

        name = "FN" + self.parse_numeric_defined_function()

        param = None
        if self.lexer.peek().kind == TokenKind.SYM_L_PAREN:
            param = self.parse_parameter_list()

        assert self.lexer.next().kind == TokenKind.SYM_EQUAL

        body = self.parse_numeric_expression()
        return ast.Def(name, param, body)

    def parse_numeric_defined_function(self) -> str:
        assert self.lexer.next().kind == TokenKind.KW_FN

        assert self.lexer.next().kind == TokenKind.IDENTIFIER
        tok = self.lexer.next()
        identifier = self.lexer.get_token_string(tok)
        assert identifier[0] in LETTERS
        assert len(identifier) == 1

        return identifier

    def parse_parameter_list(self) -> ast.SimpleNumVar:
        assert self.lexer.next().kind == TokenKind.SYM_L_PAREN

        val = self.parse_parameter()

        assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
        return val

    def parse_parameter(self) -> ast.SimpleNumVar:
        return self.parse_simple_numeric_variable()

    def parse_dimension_statement(self) -> ast.Dim:
        decls = []
        assert self.lexer.next().kind == TokenKind.KW_DIM

        decls.append(self.parse_array_declaration())

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                decls.append(self.parse_array_declaration())
            else:
                break
        return ast.Dim(decls)

    def parse_array_declaration(self) -> ast.ArrayDecl:
        name = self.parse_numeric_array_name()

        assert self.lexer.next().kind == TokenKind.SYM_L_PAREN

        bounds = self.parse_bounds()

        assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
        return ast.ArrayDecl(name, bounds)

    def parse_numeric_array_name(self) -> str:
        assert self.lexer.next().kind == TokenKind.IDENTIFIER
        tok = self.lexer.next()
        identifier = self.lexer.get_token_string(tok)
        assert identifier[0] in LETTERS
        assert len(identifier) == 1

        return identifier
    
    def parse_bounds(self) -> Tuple[int, Optional[int]]:
        assert (bound1 := self.lexer.next()).kind == TokenKind.INTEGER

        int1 = int(self.lexer.get_token_string(bound1))

        int2 = None
        if self.lexer.peek().kind == TokenKind.SYM_COMMA:
            self.lexer.next()
            assert (bound2 := self.lexer.next()).kind == TokenKind.INTEGER
            int2 = int(self.lexer.get_token_string(bound2))

        return int1, int2
        
    def parse_gosub_statement(self) -> ast.GoSub:
        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_SUB

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value
        assert line_number is int 
        return ast.GoSub(line_number)

    def parse_goto_statement(self) -> ast.Goto:
        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_TO

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value

        assert line_number is int 
        return ast.Goto(line_number)

    def parse_on_goto_statement(self) -> ast.OnGoto:
        labels = []

        assert self.lexer.next().kind == TokenKind.KW_ON

        on_expr = self.parse_numeric_expression()

        assert self.lexer.next().kind == TokenKind.KW_GO
        assert self.lexer.next().kind == TokenKind.KW_TO

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        labels.append(self.lexer.next().value)

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                
                assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
                labels.append(self.lexer.next().value)
            else:
                break
        
        return ast.OnGoto(on_expr, labels)

    def parse_if_then_statement(self) -> ast.IfThen:
        assert self.lexer.next().kind == TokenKind.KW_IF

        expr = self.parse_relational_expression()

        assert self.lexer.next().kind == TokenKind.KW_THEN

        assert self.lexer.peek().kind == TokenKind.INTEGER # Line number
        line_number = self.lexer.next().value        

        assert line_number is int 
        return ast.IfThen(expr, line_number)

    def parse_input_statement(self) -> ast.Input:
        assert self.lexer.next().kind == TokenKind.KW_INPUT

        vars = self.parse_variable_list()

        return ast.Input(vars)

    def parse_variable_list(self) -> List[ast.NumVar | ast.StringVar]:
        vars = []
        vars.append(self.parse_variable())

        while True:
            if self.lexer.peek().kind == TokenKind.SYM_COMMA:
                self.lexer.next()
                vars.append(self.parse_variable())
            else:
                break
        return vars

    def parse_option_statement(self) -> ast.Option:
        assert self.lexer.next().kind == TokenKind.KW_OPTION

        assert self.lexer.next().kind == TokenKind.KW_BASE

        assert (tok := self.lexer.next()).kind == TokenKind.INTEGER
        assert (value := int(self.lexer.get_token_string(tok))) in [0, 1]

        match value:
            case 0: 
                return ast.Option.OPT_BASE_ZERO
            case 1:
                return ast.Option.OPT_BASE_ONE

    def parse_randomize_statement(self) -> ast.Randomize:
        assert self.lexer.next().kind == TokenKind.KW_RANDOMIZE
        return ast.Randomize()

    def parse_read_statement(self) -> ast.Read:
        assert self.lexer.next().kind == TokenKind.KW_READ

        vars = self.parse_variable_list()

        return ast.Read(vars)

    def parse_remark(self) -> None:
        while self.lexer.next().kind != TokenKind.EOL:
            pass
        return

    def parse_restore_statement(self) -> ast.Restore:
        assert self.lexer.next().kind == TokenKind.KW_RESTORE
        return ast.Restore()

    def parse_return_statement(self) -> ast.Return:
        assert self.lexer.next().kind == TokenKind.KW_RETURN
        return ast.Return()

    def parse_stop_statment(self) -> ast.Stop:
        assert self.lexer.next().kind == TokenKind.KW_STOP
        return ast.Stop()

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
        match self.lexer.peek().kind:
            case TokenKind.

    def parse_numeric_expression(self) -> ast.NumExpr:
        pom = [TokenKind.SYM_PLUS, TokenKind.SYM_MINUS]
        sign = None
        if (peeked := self.lexer.peek().kind) in pom:
            self.lexer.next()
            sign = ast.UnaryOpKind.UOP_NEG if peeked == TokenKind.SYM_PLUS else ast.UnaryOpKind.UOP_POS
 
        lhs = self.parse_term()
        if sign is not None:
            lhs = ast.UnaryOp(op=sign, operand=lhs)
        
        while (peeked := self.lexer.peek().kind) in pom:
            op = ast.BinOpKind.BOP_PLUS if peeked == TokenKind.SYM_PLUS else ast.BinOpKind.BOP_MINUS
            self.lexer.next()
            lhs = ast.BinOp(op=op, lhs=lhs, rhs=self.parse_term())

        return lhs


    def parse_term(self) -> ast.NumExpr:
        lhs = self.parse_factor()
        while self.lexer.peek().kind in [TokenKind.SYM_ASTERISK, TokenKind.SYM_SLASH]:
            op = None
            match self.lexer.peek():
                case TokenKind.SYM_ASTERISK:
                    op = ast.BinOpKind.BOP_MULTIPLY
                case TokenKind.SYM_SLASH:
                    op = ast.BinOpKind.BOP_DIVIDE
            assert op is not None 
            lhs = ast.BinOp(op=op, lhs=lhs, rhs=self.parse_factor())
        
        return lhs


    def parse_factor(self) -> ast.NumExpr:
        lhs = self.parse_primary()
        while self.lexer.peek().kind == TokenKind.SYM_CARET:
            lhs = ast.BinOp(op=ast.BinOpKind.BOP_CARET, lhs=lhs, rhs=self.parse_numeric_expression())
        
        return lhs

    
    def parse_primary(self) -> ast.NumExpr:
        match self.lexer.peek().kind:
            case TokenKind.KW_FN:
                assert self.lexer.peek().kind == TokenKind.IDENTIFIER
                ident = self.lexer.get_token_string(self.lexer.next())
                fixed_ident = "FN"+ident if not ident.startswith("FN") else ident
                arg = None
                if self.lexer.peek().kind == TokenKind.SYM_L_PAREN:
                    arg = self.parse_numeric_expression()
                    assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
                return ast.NumFunctionCall(fun_name=ast.NumFunDefined(name=fixed_ident), arg = arg)
            case TokenKind.IDENTIFIER:
                name = self.lexer.get_token_string(self.lexer.next())
                if self.lexer.peek().kind == TokenKind.SYM_L_PAREN:
                    indices = [self.parse_numeric_expression()]
                    while self.lexer.peek().kind != TokenKind.SYM_R_PAREN:
                        assert self.lexer.next().kind == TokenKind.SYM_COMMA
                        indices.append(self.parse_numeric_expression())
                    assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
                    return ast.NumArrayElem(array_name=name, indices=indices)
                else:
                    return ast.SimpleNumVar(name=name)
            case TokenKind.INTEGER:
                return ast.NumRep(num=int(self.lexer.get_token_string(self.lexer.next())))
            case TokenKind.FLOAT:
                return ast.NumRep(num=float(self.lexer.get_token_string(self.lexer.next())))
            case TokenKind.SYM_L_PAREN:
                expr = self.parse_numeric_expression()
                assert self.lexer.next().kind == TokenKind.SYM_R_PAREN
                return expr
            case _:
                raise AssertionError("expected 'FN', integer, float or left parenthesis, got " + str(self.lexer.peek().kind))
