from ast import UnaryOp
from typing import List
from syntax import ForBlock, Stmt, Program
import syntax as ast


addr = int

class Interpreter:
    program_counter: addr = 0
    call_stack = List[addr]
    program: Program
    statements = {}

    variables: dict[str: float | int] = {}
    functions: dict[str: tuple(str, NumExpr)]

    def __init__(self, program):
        # Program is a class that contains block
        # Block is a list that contains either
        # the statements or linenumber
        self.program = program
        self.add_to_statements(program.block)
        print(self.statements)

    def add_to_statements(self, block: ast.Block):
        match block:
            case Line(line_num, statement):
                self.statements.update({line_num:statement})
            case ForBlock(line_num, control_var, init_val, limit, step_by, body):
                self.statements.update({line_num: block})
                for block in body:
                    self.add_to_statements(block)

    def run_num_expr(self, num_expr:NumExpr) -> float | int:
        match num_expr:
            case BinOp(op, lhs, rhs):
                match op:
                    case "BOP_PLUS":
                        return self.run_num_expr(lhs) + self.run_num_expr(rhs)
                    case "BOP_MINUS":
                        return self.run_num_expr(lhs) - self.run_num_expr(rhs)
                    case "BOP_MULTIPLY":
                        return self.run_num_expr(lhs) * self.run_num_expr(rhs)
                    case "BOP_DIVIDE":
                        return self.run_num_expr(lhs) / self.run_num_expr(rhs)
                    case "BOP_CARET":
                        return self.run_num_expr(lhs) ** self.run_num_expr(rhs)

            case UnaryOp(op, operand):
                match op:
                    case "UOP_POS":
                        return operand
                    case "UOP_NEG":
                        return -operand


            case NumRep(num): 
                return num 

            case NumFunctionCall(fun_name, arg): 
                fun = self.functions[fun_name]
                self.variables.update({fun[0]:arg})

                res = run_num_expr()
                self.variables.pop(fun[0])

                return res

            case _:
                if isinstance(item, NumVar.__value__):  #This should be the only case
                    match num_expr:
                        case SimpleNumVar(name):
                            return name

                        case NumArrayElem(array_name, indices):
                            




        

    def run(self):
        running = True
        
        while running:
            
            match self.program.block[index]:
                case Line(line_num, statement):

                    match statement:
                        case Data(data_list):

                        case Def(name, params, body):

                        case Dim(array_decls):

                        case GoSub(line_num):
                            
                        case Goto(line_num):

                        case IfThen(condition, goto):

                        case Input(vars):

                        case NumLet(var, val):


                        case StringLet(var, val):

                        case OnGoto(on, labels):

                        case Option(OPT_BASE_ZERO, OPT_BASE_ONE):

                        case Print(print_list):
                            for item in print_list:
                                # TODO: Figure out what is tabcall
                                
                                if isinstance(item, NumExpr.__value__): 
                                    


                                elif type(item) in StringExpr:
                                
                                match item:
                                    case NumExpr
                                        match 
                                    case StringExpr


                        case Randomize():

                        case Read(vars):

                        case Restore():

                        case Return():

                        case Stop():

                        

                case ForBlock(line_num, control_var, init_val, limit, step_by):



            

            
        
        
