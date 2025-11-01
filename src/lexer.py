from tokens import Token, TokenKind
from typing import Union, Optional

WHITESPACE = [' ']

class Lexer:

    source: Optional[str] = None
    peeked: Optional[Token] = None
    current: int = 0
    start: int = 0

    def __init__(self, source):
        # Source is a string to be decomposed into tokens
        self.source = source
        pass

    def skip_whitespace(self):
        while self.source[self.current] in WHITESPACE:
            self.current += 1
        
        self.start = self.current

    def process_alpha(self) -> Token:
        char: str = self.source[self.current]
        check = lambda key: key == self.source[self.current:self.current+len(key)] 

        def check_kw(key: str, kind: TokenKind) -> Optional[TokenKind]:
            if key == self.source[self.start:self.start+len(key)]:
                self.current += len(key)
                return kind
            return None
        
        match (char.lower()):
            case "l":
                if (tok := check_kw("LET", TokenKind.KW_LET)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current+=1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "d":
                if (tok := check_kw("DEF", TokenKind.KW_DEF)) is not None:
                    return Token(tok, self.start, self.current)
                elif (tok := check_kw("DATA", TokenKind.KW_DATA)) is not None:
                    return Token(tok, self.start, self.current)
                elif (tok := check_kw("DIM", TokenKind.KW_DIM)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "f":
                if (tok := check_kw("FN", TokenKind.KW_FN)) is not None:
                    return Token(tok, self.start, self.current)
                elif (tok := check_kw("FOR", TokenKind.KW_FOR)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "g":
                if (tok := check_kw("GO", TokenKind.KW_GO)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "t":
                if (tok := check_kw("TO", TokenKind.KW_TO)) is not None:
                    return Token(tok, self.start, self.current)
                elif (tok := check_kw("THEN", TokenKind.KW_THEN)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "s":
                if (tok := check_kw("SUB", TokenKind.KW_SUB)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "i":
                if (tok := check_kw("IF", TokenKind.KW_IF)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "n":
                if (tok := check_kw("NEXT", TokenKind.KW_NEXT)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "o":
                if (tok := check_kw("OPTION", TokenKind.KW_OPTION)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
            
            case "b":
                if (tok := check_kw("BASE", TokenKind.KW_BASE)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
            case "r":
                if (tok := check_kw("RANDOMIZE", TokenKind.KW_RANDOMIZE)) is not None:
                    return Token(tok, self.start, self.current)
                elif (tok := check_kw("REM", TokenKind.KW_REM)) is not None:
                    return Token(tok, self.start, self.current)
                else:
                    while self.source[self.current] not in WHITESPACE:
                        self.current += 1
                    return Token(TokenKind.IDENTIFIER, self.start, self.current)
                
                
    def process_symbol(self) -> TokenKind:
        char: str = self.source[self.current]
        self.current += 1
        
        match (char):
            case "+":
                return TokenKind.SYM_PLUS
            case "-":
                return TokenKind.SYM_MINUS
            case "*":
                return TokenKind.SYM_ASTERISK
            case "=":
                return TokenKind.SYM_EQUAL
            case "/":
                return TokenKind.SYM_SLASH
            case ";":
                return TokenKind.SYM_SEMICOLON
            case "(":
                return TokenKind.SYM_L_PAREN
            case ")":
                return TokenKind.SYM_R_PAREN
            case "<":
                return TokenKind.SYM_L_ANGLE
            case ">":
                return TokenKind.SYM_R_ANGLE
            case "$":
                return TokenKind.SYM_DOLLAR
            case "\"":
                return TokenKind.SYM_DBL_QUOTE
            case ",":
                return TokenKind.SYM_COMMA
            case _:
                print(f"Unknown symbol: {char}")
    
    def process_token(self):
        self.skip_whitespace()
        self.start = self.current
        char: str = self.source[self.current]

        print(f"cur: {self.current}, <{self.source[self.current]}>")

        if char.isalpha():
            return self.process_alpha()
        
        elif char.isdigit():
            
            pass
        else:
            return Token(self.process_symbol(), self.start, self.start + 1)

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
