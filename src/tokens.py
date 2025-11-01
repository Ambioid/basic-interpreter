from enum import Enum

class TokenKind(Enum):
    UNKNOWN = 0
    IDENTIFIER = 1 
    SYM_PLUS = 2
    SYM_MINUS = 3
    SYM_ASTERISK = 4
    SYM_EQUAL = 5
    SYM_SLASH = 6
    SYM_SEMICOLON = 7
    SYM_L_PAREN = 8
    SYM_R_PAREN = 9
    SYM_L_ANGLE = 10
    SYM_R_ANGLE = 11
    SYM_DOLLAR = 12
    SYM_DBL_QUOTE = 13
    SYM_PERIOD = 14
    SYM_COMMA = 15
    KW_LET = 16
    KW_DEF = 17
    KW_FN = 18
    KW_GO = 19
    KW_TO = 20
    KW_SUB = 21
    KW_RETURN = 22
    KW_ON = 23
    KW_STOP = 24
    KW_IF = 25
    KW_THEN = 26
    KW_FOR = 27
    KW_NEXT = 28
    KW_DATA = 29
    KW_DIM = 30
    KW_OPTION = 31
    KW_BASE = 32
    KW_REM = 33
    KW_RANDOMIZE = 34
    EOF = 35

class Token:
    kind: TokenKind
    start: int
    end: int

    def __init__(self, kind, start, end):
        self.kind = kind
        self.start = start
        self.end = end