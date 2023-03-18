from token_petunia import Tokenizer
from TokenType import TokenType
from DataType import DataType
from consume_count import tokenConsumeCount, litConsumeCount
from Function import Function


class Expr():
    def __init__(self, token, subExpr = None):
        self.token = token
        if subExpr == None:
            self.subExpr = []
        else:
            self.subExpr = subExpr

    def __repr__(self):
        return f"{{Expr Object, token: {self.token}, subExpr: {self.subExpr}}}"

class Parser():
    def __init__(self, program):
        tokenize = Tokenizer(program)
        self.tokens = tokenize.tokens
        self.current = 0
        self.parse()

    def advance(self):
        self.current += 1
        return self.tokens[self.current-1]

    def peek(self):
        if self.current == len(self.tokens):
            raise Exception("Unexpected EOF")
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def check(self, tokenType):
        return self.peek().type == tokenType

    def match(self, tokenType):
        if self.check(tokenType):
            self.advance()
            return True
        return False

    def asser(self, token):
        if self.peek().type != token:
            raise Exception("Expected '" + str(token.value) + "' at line " + str(self.peek().lineNum) + " instead got '" + str(self.peek().type.value) + "'")

    def parseBlock(self):
        self.match(TokenType.INDENT)
        block = []
        while not self.match(TokenType.DEDENT):
            block.append(self.parseExpr())
        return block

    def parseFunc(self): #consumes a type, literal, type literal, type literal, until end alseo needs to add number of arguments to litConsumeCount
        numArgs = 0
        args = []

        funcType = self.parseExpr()
        linenum = self.peek().lineNum
        self.asser(TokenType.LIT)
        funcName = self.advance().literal

        while not self.match(TokenType.END):
            first = DataType(self.parseExpr())
            self.asser(TokenType.LIT)
            second = self.advance().literal
            args.append((first, second))
            numArgs += 1

        litConsumeCount[funcName] = numArgs
        
        if self.check(TokenType.INDENT):
            body = self.parseBlock()
        else:
            body = self.parseExpr()

        return Function(funcName, funcType, args, body, linenum)

    def parseExpr(self):
        if self.match(TokenType.FUNC):
            return self.parseFunc()

        token = self.advance()
        if token.type == TokenType.LIT:
            if token.literal in litConsumeCount:
                 count = litConsumeCount[token.literal]
            else:
                count = 0
        else:
            assert token.type in tokenConsumeCount, f"{token.type} is not in TokenConsumeCount, please add how many arguments it has"
            count = tokenConsumeCount[token.type]

        subExpr = []
        for _ in range(count):
            if self.check(TokenType.INDENT):
                subExpr.append(self.parseBlock())
            else:
                subExpr.append(self.parseExpr())
        return Expr(token, subExpr)
    
    def parse(self):
        self.program = self.parseBlock()





