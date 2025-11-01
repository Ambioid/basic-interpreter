from tokens import Token, TokenKind
from typing import Union

WHITESPACE = [' ']

class Lexer:

    source: Union[str, None] = None
    peeked: Union[Token, None] = None
    index: int = 0

    def __init__(self, source):
        # Source is a string to be decomposed into tokens
        self.source = source
        pass

    def skip_whitespace(self):
        while self.source[self.index] in WHITESPACE:
            self.index += 1

    def process_alpha(self) -> Token:
        char: str = self.source[self.index]
        check = lambda key: key == self.source[self.index:self.index+len(key)] 
        match (char.lower()):
            case "l":
                if check("LET"):
                    self.index += 3
                    return Token(TokenKind.KW_LET, self.index, self.index+2)
                else:
                    start = self.index
                    while self.source[self.index] not in WHITESPACE:
                        self.index+=1
                    return Token(TokenKind.IDENTIFIER, start, self.index-1)
            case "d":
                print("D")
                if check("DEF"):
                    self.index += 3
                    return Token(TokenKind.KW_DEF, self.index, self.index+2)
                elif check("DATA"):
                    self.index += 4
                    return Token(TokenKind.KW_DATA, self.index, self.index+3)
                elif check("DIM"):
                    self.index += 3
                    return Token(TokenKind.KW_DIM, self.index, self.index+2)
                else:
                    start = self.index
                    while self.source[self.index] not in WHITESPACE:
                        self.index += 1
                    return Token(TokenKind.IDENTIFIER, start, self.index-1)
    
    def process_token(self):
        self.skip_whitespace()
        char: str = self.source[self.index]
        print(char)

        if char.isalpha():
            return self.process_alpha()
        
        elif char.isdigit():
            
            pass
        else:
            match (char):
                case "+":
                    self.index += 1
                    return Token(TokenKind.SYM_PLUS, self.index, self.index)
                case "-":
                    self.index += 1
                    return Token(TokenKind.SYM_MINUS, self.index, self.index)
                case "*":
                    self.index += 1
                    return Token(TokenKind.SYM_ASTERISK, self.index, self.index)
                case "=":
                    self.index += 1
                    return Token(TokenKind.SYM_EQUAL, self.index, self.index)
                case "/":
                    self.index += 1
                    return Token(TokenKind.SYM_SLASH, self.index, self.index)
                case ";":
                    self.index += 1
                    return Token(TokenKind.SYM_SEMICOLON, self.index, self.index)
                case "(":
                    self.index += 1
                    return Token(TokenKind.SYM_L_PAREN, self.index, self.index)
                case ")":
                    self.index += 1
                    return Token(TokenKind.SYM_R_PAREN, self.index, self.index)
                case "<":
                    self.index += 1
                    return Token(TokenKind.SYM_L_ANGLE, self.index, self.index)
                case ">":
                    self.index += 1
                    return Token(TokenKind.SYM_R_ANGLE, self.index, self.index)
                case "$":
                    self.index += 1
                    return Token(TokenKind.SYM_DOLLAR, self.index, self.index)
                case "\"":
                    self.index += 1
                    return Token(TokenKind.SYM_DBL_QUOTE, self.index, self.index)
                case ",":
                    self.index += 1
                    return Token(TokenKind.SYM_COMMA, self.index, self.index)

    def peek():

        pass

    def next():
        pass
    
        
print("DATA DIM LET +-=;")
l = Lexer("DATA DIM LET +-=;")
print(l.process_token())
print(l.process_token())
print(l.process_token())
print(l.process_token())
print(l.process_token())
print(l.process_token())
print(l.process_token())
print(l.process_token())
