from enum import Enum, auto

class TokenType(Enum):
    # Literals
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Keywords
    KW_FN = auto()
    KW_LET = auto()
    KW_VAR = auto()
    KW_IF = auto()
    KW_ELSE = auto()
    KW_FOR = auto()
    KW_IN = auto()
    KW_RETURN = auto()
    KW_PURE = auto()
    KW_TRANSACT = auto()
    KW_DECIDES = auto()
    
    # Types
    KW_INT = auto()
    KW_FLOAT = auto()
    KW_STRING = auto()
    KW_BOOL = auto()
    KW_VOID = auto()
    
    # Operators
    ASSIGN = auto()       # =
    EQUAL = auto()        # ==
    NOT_EQUAL = auto()    # !=
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # /
    PLUS_ASSIGN = auto()  # +=
    MINUS_ASSIGN = auto() # -=
    LESS = auto()         # <
    LESS_EQUAL = auto()   # <=
    GREATER = auto()      # >
    GREATER_EQUAL = auto()# >=
    DOT = auto()          # .
    ARROW = auto()        # ->
    RANGE = auto()        # ..
    QUESTION = auto()     # ?
    
    # Punctuation
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    COMMA = auto()        # ,
    COLON = auto()        # :
    SEMICOLON = auto()    # ;
    
    EOF = auto()

KEYWORDS = {
    "fn": TokenType.KW_FN,
    "let": TokenType.KW_LET,
    "var": TokenType.KW_VAR,
    "if": TokenType.KW_IF,
    "else": TokenType.KW_ELSE,
    "for": TokenType.KW_FOR,
    "in": TokenType.KW_IN,
    "return": TokenType.KW_RETURN,
    "pure": TokenType.KW_PURE,
    "transact": TokenType.KW_TRANSACT,
    "decides": TokenType.KW_DECIDES,
    "int": TokenType.KW_INT,
    "float": TokenType.KW_FLOAT,
    "string": TokenType.KW_STRING,
    "bool": TokenType.KW_BOOL,
    "void": TokenType.KW_VOID,
}

class Token:
    def __init__(self, type_, lexeme, line, col):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', L{self.line})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.source):
            c = self.source[self.pos]
            
            # Whitespace
            if c in ' \t\r\n':
                if c == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1
                continue
            
            # Comments (//)
            if c == '/' and self.pos + 1 < len(self.source) and self.source[self.pos+1] == '/':
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                continue
            
            # Identifiers and Keywords
            if c.isalpha() or c == '_':
                start = self.pos
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                    self.pos += 1
                text = self.source[start:self.pos]
                token_type = KEYWORDS.get(text, TokenType.IDENT)
                self.tokens.append(Token(token_type, text, self.line, self.col))
                self.col += len(text)
                continue
            
            # Numbers
            if c.isdigit():
                start = self.pos
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    self.pos += 1
                text = self.source[start:self.pos]
                self.tokens.append(Token(TokenType.NUMBER, text, self.line, self.col))
                self.col += len(text)
                continue
            
            
            two_char = self.source[self.pos:self.pos+2]
            if two_char == '==': self.tokens.append(Token(TokenType.EQUAL, "==", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '!=': self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '->': self.tokens.append(Token(TokenType.ARROW, "->", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '..': self.tokens.append(Token(TokenType.RANGE, "..", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '+=': self.tokens.append(Token(TokenType.PLUS_ASSIGN, "+=", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '-=': self.tokens.append(Token(TokenType.MINUS_ASSIGN, "-=", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '<=': self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", self.line, self.col)); self.pos += 2; self.col += 2; continue
            if two_char == '>=': self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", self.line, self.col)); self.pos += 2; self.col += 2; continue

            # Single-character operators
            single_char = {
                '=': TokenType.ASSIGN, '+': TokenType.PLUS, '-': TokenType.MINUS, 
                '*': TokenType.STAR, '/': TokenType.SLASH, '<': TokenType.LESS, 
                '>': TokenType.GREATER, '.': TokenType.DOT, '?': TokenType.QUESTION,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN, '{': TokenType.LBRACE, 
                '}': TokenType.RBRACE, '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                ',': TokenType.COMMA, ':': TokenType.COLON, ';': TokenType.SEMICOLON
            }
            if c in single_char:
                self.tokens.append(Token(single_char[c], c, self.line, self.col))
                self.pos += 1
                self.col += 1
                continue

            # Unexpected character
            raise Exception(f"Unexpected character '{c}' at line {self.line}")
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens