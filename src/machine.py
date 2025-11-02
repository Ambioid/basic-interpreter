from typing import List
from syntax import *
import random
import math
import time

addr = int

class EnvVariable:
    value: int | float | str
    def __init__(self, value: int | float | str):
        self.value = value

class EnvFunction:
    param: str
    expr: NumExpr
    def __init__(self, param, expr):
        self.param = param
        self.expr = expr    

class EnvArray:
    dim: ArrayDecl
    data: list[int]
    
    def __init__(self, dim: ArrayDecl):
        self.dim = dim
    
    def index(self, ind, indexing):
        mod = (-1 if indexing == Option.OPT_BASE_ONE else 0)
        return (ind[1] + mod) * self.dim.bounds[1] + (ind[0] + mod)
    
    def get(self, indices, indexing):
        ind = self.index(indices, indexing)
        return self.data[ind]
    
    def set(self, indices, indexing, val):
        ind = self.index(indices, indexing)
        self.data[ind] = val


class Interpreter:
    program_counter: addr = 0
    call_stack = List[addr]
    program: Program
    statements: dict[int:Block] = {}
    line_nums: list[int] = []

    variables: dict[str: EnvVariable] = {}
    arrays: dict[str: EnvArray] = {}
    functions: dict[str: EnvFunction] = {}

    indexing: Option

    def __init__(self, program: Program):
        self.program = program
        self.add_to_statements(program.block)
        print(self.statements)

        self.line_nums = list(sorted(list(self.statements.keys())))
        self.indexing = Option.OPT_BASE_ZERO

    def add_to_statements(self, block: Block) -> None:
        match block:
            case Line(line_num, statement):
                self.statements.update({line_num:statement})
            case ForBlock(line_num, control_var, init_val, limit, step_by, body):
                self.statements.update({line_num: block})
                for block in body:
                    self.add_to_statements(block)

    def register_function(self, name: str, function: EnvFunction) -> None:
        self.functions.update({name:function})
    def register_variable(self, name: str, variable: EnvVariable) -> None:
        self.variables.update({name: variable})
    def register_array(self, name: str, array: EnvArray) -> None:
        self.variables.update({name: array})

    def run_num_expr(self, num_expr:NumExpr, env: dict = {}) -> float | int:
        match num_expr:
            case BinOp(op, lhs, rhs):
                match op:
                    case BinOpKind.BOP_PLUS:
                        return self.run_num_expr(lhs) + self.run_num_expr(rhs)
                    case BinOpKind.BOP_MINUS:
                        return self.run_num_expr(lhs) - self.run_num_expr(rhs)
                    case BinOpKind.BOP_MULTIPLY:
                        return self.run_num_expr(lhs) * self.run_num_expr(rhs)
                    case BinOpKind.BOP_DIVIDE:
                        return self.run_num_expr(lhs) / self.run_num_expr(rhs)
                    case BinOpKind.BOP_CARET:
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
                match fun_name:
                    case "ABS":
                        return abs(self.run_num_expr(arg))
                    case "ATN":
                        return math.atan(self.run_num_expr(arg))
                    case "COS":
                        return math.cos(self.run_num_expr(arg))
                    case "EXP":
                        return math.exp(self.run_num_expr(arg))
                    case "INT":
                        return math.floor(self.run_num_expr(arg))
                    case "LOG":
                        return math.atan(self.run_num_expr(arg))
                    case "SGN":
                        val = self.run_num_expr(arg)
                        if val == 0: return 0
                        elif val < 0: return -1
                        else: return 1
                    case "SIN":
                        return math.sin(self.run_num_expr(arg))
                    case "SQR":
                        return math.sqrt(self.run_num_expr(arg))
                    case "TAN":
                        return math.tan(self.run_num_expr(arg))
                    case _:
                        fun: EnvFunction = self.functions[fun_name]
                        
                        env.update({fun.param : EnvVariable(arg)})
                        res = self.run_num_expr(fun.expr, env)
                        env.pop(fun.param)

                        return res
            
            case SimpleNumVar(name):
                if name == "RND":
                    return random.random()
                if name in self.variables.keys():
                    return self.variables[name].value   
                elif name in env.keys():
                    return env[name].value
                raise AssertionError("Invalid identifier")
                    
            case NumArrayElem(name, indices):
                vals = []
                for ind in indices:
                    vals.append(round(self.run_num_expr(ind)))

                return self.arrays[name].get(vals, self.indexing)
    
    def get_next_line_num(self, num):
        higher = filter(lambda x:x>num, self.line_nums)
        if len(higher) == 0: self.running = False
        next = min(higher)
        return next
    
    def progress_program_counter(self):
        pc = self.program_counter
        return self.get_next_line_num(pc)
        
    
    def run(self):
        self.running = True
        
        while self.running:
            match self.statements[self.program_counter]:
                case Line(line_num, statement):
                    match statement:
                        case Data(data_list):
                            pass
                        case Def(name, params, body):
                            self.register_function(name, EnvFunction(params, body))
                            self.progress_program_counter()
                            continue
                        case Dim(array_decls):
                            for decl in array_decls:
                                self.register_array(decl.name, EnvArray(decl))
                            self.progress_program_counter()
                            continue
                        case GoSub(line_num):
                            self.call_stack.append(self.program_counter)
                            self.program_counter = self.get_next_line_num(line_num)
                            continue
                        case Goto(line_num):
                            self.program_counter = self.get_next_line_num(line_num-1)
                            continue
                        case IfThen(condition, goto):
                            match condition:
                                case RelationalNumExpr(relation, lhs, rhs):
                                    a = self.run_num_expr(lhs)
                                    b = self.run_num_expr(rhs)
                                    match relation:
                                        case Relation.REL_EQUALS:
                                            branch = (a == b)
                                        case Relation.REL_NOT_EQUAL:
                                            branch = (a != b)
                                        case Relation.REL_GREATER:
                                            branch = (a > b)
                                        case Relation.REL_GREATER_THAN_OR_EQ:
                                            branch = (a >= b)
                                        case Relation.REL_LESS_THAN:
                                            branch = (a < b)
                                        case Relation.REL_LESS_THAN_OR_EQ:
                                            branch = (a <= b)
                                case RelationalStrExpr(relation, lhs, rhs):
                                    assert relation in [Relation.REL_EQUALS, Relation.REL_NOT_EQUAL]
                                    match relation:
                                        case Relation.REL_EQUALS:
                                            branch = (a == b)
                                        case Relation.REL_NOT_EQUAL:
                                            branch = (a != b)
                            if branch:
                                self.program_counter = self.get_next_line_num(line_num-1)
                                continue
                            else:
                                self.progress_program_counter()
                                continue
                        case Input(vars):
                            pass
                        case NumLet(var, val):
                            if type(var) == SimpleNumVar:
                                if var.name in self.variables.keys():
                                    self.variables[var.name].value = self.run_num_expr(val)
                                    self.progress_program_counter()
                                    continue
                                else:
                                    self.register_variable(var.name, EnvVariable(self.run_num_expr(val)))
                                    self.progress_program_counter()
                                    continue
                            elif type(var) == NumArrayElem:
                                if var.array_name in self.arrays.keys():
                                    self.arrays[var.array_name].set(var.indices, self.indexing, self.run_num_expr(var))
                                    self.progress_program_counter()
                                    continue
                                else:
                                    raise AssertionError("Array not defined")
                        case StringLet(var, val):
                            pass
                        case OnGoto(on, labels):
                            pass
                        case Option.OPT_BASE_ZERO:
                            self.indexing = Option.OPT_BASE_ZERO
                            self.progress_program_counter()
                            continue
                        case Option.OPT_BASE_ONE:
                            self.indexing = Option.OPT_BASE_ONE
                            self.progress_program_counter()
                            continue
                        case Print(print_list):
                            for item in print_list:
                                # TODO: Figure out what is tabcall
                                pass

                        case Randomize():
                            random.seed(time.time())
                            self.progress_program_counter()
                            continue
                        case Read(vars):
                            pass
                        case Restore():
                            pass
                        case Return():
                            self.program_counter = self.get_next_line_num(self.call_stack.pop())
                            continue
                        case Stop():
                            self.running = False
                            continue
                        

                case ForBlock(line_num, control_var, init_val, limit, step_by):
                    pass