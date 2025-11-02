from enum import Enum
from typing import Optional

from attr import dataclass


@dataclass
class Program:
    block: list["Line | ForBlock"]


@dataclass
class Line:
    line_num: int
    statement: "Stmt"


@dataclass
class ForBlock:
    line_num: int
    control_var: "SimpleNumVar"
    init_val: "NumExpr"
    limit: "NumExpr"
    step_by: Optional["NumExpr"]
    body: "Block"


Block = Line | ForBlock


@dataclass
class BinOp:
    op: "BinOpKind"
    lhs: "NumExpr"
    rhs: "NumExpr"


class BinOpKind(Enum):
    BOP_PLUS = 0
    BOP_MINUS = 1
    BOP_MULTIPLY = 2
    BOP_DIVIDE = 3
    BOP_CARET = 4


@dataclass
class UnaryOp:
    op: "UnaryOpKind"
    operand: "NumExpr"


class UnaryOpKind(Enum):
    UOP_POS = 0
    UOP_NEG = 1


@dataclass
class NumArrayElem:
    # Single char
    array_name: str
    # One or more
    indices: list["NumExpr"]

@dataclass
class SimpleNumVar:
    name: str

NumVar = SimpleNumVar | NumArrayElem


@dataclass
class NumRep:
    num: int | float


@dataclass
class NumFunctionCall:
    fun_name: "NumFunName"
    arg: Optional["NumExpr"]


class NumFunBuiltin(Enum):
    NFB_ABS = 0
    NFB_ATN = 1
    NFB_COS = 2
    NFB_EXP = 3
    NFB_INT = 4
    NFB_LOG = 5
    NFB_RND = 6
    NFB_SGN = 7
    NFB_SIN = 8
    NFB_SQR = 9
    NFB_TAN = 10


@dataclass
class NumFunDefined:
    # Starts with 'FN'
    name: str


NumFunName = NumFunBuiltin | NumFunDefined


NumExpr = BinOp | UnaryOp | NumVar | NumRep | NumFunctionCall


@dataclass
class Data:
    data_list: list["Datum"]


Datum = int | str


@dataclass
class Def:
    # Starts with 'FN'
    name: str
    params: SimpleNumVar
    body: NumExpr


@dataclass
class Dim:
    # One or more
    array_decls: list["ArrayDecl"]


@dataclass
class ArrayDecl:
    # Single letter
    name: str
    bounds: tuple[int, Optional[int]]


@dataclass
class GoSub:
    line_num: int


@dataclass
class Goto:
    line_num: int


@dataclass
class IfThen:
    condition: "RelationalExpr"
    # Line number
    goto: int

@dataclass
class RelationalNumExpr:
    relation: "Relation"
    lhs: NumExpr
    rhs: NumExpr

@dataclass
class RelationalStrExpr:
    relation: "Relation"
    lhs: "StringExpr"
    rhs: "StringExpr"

RelationalExpr = RelationalNumExpr | RelationalStrExpr

class Relation(Enum):
    REL_EQUALS = 0
    REL_NOT_EQUAL = 1
    REL_LESS_THAN = 2
    REL_GREATER = 3
    REL_LESS_THAN_OR_EQ = 4
    REL_GREATER_THAN_OR_EQ = 5


@dataclass
class Input:
    vars: list["NumVar | StringVar"]


@dataclass
class StringVar:
    # Ends in '$'
    name: str


@dataclass
class NumLet:
    var: NumVar
    val: NumExpr


@dataclass
class StringLet:
    var: StringVar
    val: "StringExpr"

#                        string literal/constant
StringExpr = StringVar | str


@dataclass
class OnGoto:
    on: NumExpr
    labels: list[int]


class Option(Enum):
    OPT_BASE_ZERO = 0
    OPT_BASE_ONE = 1


@dataclass
class Print:
    print_list: list["PrintItem"]


@dataclass
class TabCall:
    inner: NumExpr


PrintItem = NumExpr | StringExpr | TabCall


@dataclass
class Randomize: pass


@dataclass
class Read:
    vars: list[NumVar | StringVar]


@dataclass
class Restore: pass


@dataclass
class Return: pass


@dataclass
class Stop: pass


Stmt = Data | Def | Dim | GoSub | Goto | IfThen | Input | NumLet | StringLet | OnGoto | Option | Print | Randomize | Read | Restore | Return | Stop # type: ignore