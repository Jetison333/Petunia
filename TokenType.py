from enum import Enum, auto

class TokenType(Enum):
    LIT = auto()
    NUM = auto()

    BOOL = 'bool'
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    ARRAY = 'array'
    AT = 'at'
    
    PLUS = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    POW = '^'
    MOD = '%'

    EQUAL = '='
    GT = '>'
    LT = '<'
    NOT = 'not'
    AND = 'and'
    OR = 'or'

    DEF = 'def'
    IF = 'if'
    WHILE = 'while'
    
    SET = 'set'
    SETAT = 'setat'
    NEW = 'new'
    
    INDENT = auto()
    DEDENT = auto()

    APPEND = ','