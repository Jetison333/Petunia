from token_petunia import Tokenizer
from TokenType import TokenType
from consume_count import tokenConsumeCount, litConsumeCount


class Expr():
    def __init__(self, token, subExpr):
        self.token = token
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
            raise Exception("Expected '" + token.value + "' at line " + str(self.peek().lineNum) + " instead got '" + self.peek().type.value + "'")

    def parseBlock(self):
        self.match(TokenType.INDENT)
        block = []
        while not self.match(TokenType.DEDENT):
            block.append(self.parseExpr())
        return block

    def parseExpr(self):
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





