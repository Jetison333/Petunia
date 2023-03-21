from TokenType import TokenType

from utils import *

import re

class Token():
    def __init__(self, typ, lineNum, literal = None):
        self.type = typ
        self.literal = literal
        self.lineNum = lineNum

    def __repr__(self):
        return f'{{Token Object, type = {self.type}, literal = {self.literal}}}'

class Tokenizer():
    def __init__(self, program):
        self.program = program.split('\n')
        self.current = 0
        self.tokens = []
        self.line_num = 0
        self.parse()

    def addToken(self, typ, literal = None):
        self.tokens.append(Token(typ, self.line_num, literal))

    def parse(self):
        stack = [0]
        self.addToken(TokenType.INDENT)
        for line_num, line in enumerate(self.program):
            self.line_num = line_num + 1

            if not line or line.isspace() or line.lstrip(' ')[0] == '#':
                continue
            
            whitespace = len(line) - len(line.lstrip(' '))
            if whitespace > stack[-1]:
                stack.append(whitespace)
                self.addToken(TokenType.INDENT)
            while whitespace < stack[-1]:
                stack.pop()
                self.addToken(TokenType.DEDENT)
            assert whitespace == stack[-1], f'Error: inconsistent dedent at {self.line_num}'

            for word in line.split():
                if word[0] == "#":
                    break
                if word == '--':
                    self.addToken(TokenType.DEDENT)
                    self.addToken(TokenType.INDENT)
                else:
                    try:
                        self.addToken(TokenType(word))
                    except Exception:
                        if is_int(word):
                            self.addToken(TokenType.INT, int(word))
                        elif is_float(word):
                            self.addToken(TokenType.FLOAT, float(word))
                        else:
                            self.addToken(TokenType.LIT, word)

        for _ in stack:
            self.addToken(TokenType.DEDENT)

            
