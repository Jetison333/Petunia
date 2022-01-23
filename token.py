from enum import Enum, auto
import re

class TokenType(Enum):
    STRING = auto()
    LIT = auto()
    NUM = auto()
    
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
    INDENT = auto()
    DEDENT = auto()

    APPEND = ','



class Token():
    def __init__(self, typ, lineNum, literal = None):
        self.type = typ
        self.literal = literal
        self.lineNum = lineNum

    def __repr__(self):
        return f'<Token Object, type = {self.type}, literal = {self.literal}>'

class Tokenizer():
    def __init__(self, program):
        self.program = program.split('\n')
        self.current = 0
        self.tokens = []
        self.line_num = 0
        self.parse()

    def advance(self):
        self.current += 1
        return self.program[self.current-1]

    def addToken(self, typ, literal = None):
        self.tokens.append(Token(typ, self.line_num, literal))

    def parse(self):
        stack = [0]
        self.addToken(TokenType.INDENT)
        for line_num, line in enumerate(self.program):
            self.line_num = line_num + 1
            
            whitespace = len(line) - len(line.lstrip(' '))
            if whitespace > stack[-1]:
                stack.append(whitespace)
                self.addToken(TokenType.INDENT)
            elif whitespace < stack[-1]:
                while whitespace < stack[-1]:
                    stack.pop()
                    self.addToken(TokenType.DEDENT)
                assert whitespace == stack[-1], f'Error: inconsistent dedent at {self.line_num}'

            for word in line.split():
                if word == '--':
                    self.addToken(TokenType.DEDENT)
                    self.addToken(TokenType.INDENT)
                else:
                    try:
                        self.addToken(TokenType(word))
                    except Exception:
                        if is_float(word):
                            self.addToken(TokenType.NUM, float(word))
                        else:
                            self.addToken(TokenType.LIT, word)

        for _ in range(len(stack)-1):
            self.addToken(TokenType.DEDENT)
        self.addToken(TokenType.DEDENT)
            

def is_float(n):
    try:
        float(n)
        return True
    except Exception:
        return False
            























