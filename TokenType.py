from enum import Enum, auto

class TokenType(Enum):
    LIT = auto()
    NUM = auto()

    BOOL = 'bool'
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    
    PLUS = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    POW = '^'
    MOD = '%'

    EQUAL = '='
    GT = '>'
    LT = '<'
    NOT = '!'
    AND = '&'
    OR = '|'

    DEF = 'def'
    IF = 'if'
    WHILE = 'while'
    
    SET = 'set'
    NEW = 'new'
    
    INDENT = auto()
    DEDENT = auto()

    APPEND = ','