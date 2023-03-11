from token import Tokenizer, TokenType


TokenConsumeCount = {'print' : 1, TokenType.IF : 3, TokenType.WHILE : 2, TokenType.SET : 2, TokenType.LT : 2, TokenType.GT : 2, TokenType.EQUAL : 2, TokenType.PLUS : 2, TokenType.MUL : 2, TokenType.DIV : 2, TokenType.NUM : 0, TokenType.INDENT : 0, TokenType.DEDENT : 1, TokenType.APPEND : 2, TokenType.NEW : 3, TokenType.INT : 0, TokenType.FLOAT : 0}

class Expr():
    def __init__(self, token, subExpr):
        self.token = token
        self.subExpr = subExpr

    def __repr__(self):
        return f"<Expr Object, token: {self.token}, subExpr: {self.subExpr}>"

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

    def parseList(self):
        loc = self.peek().loc
        lst = []
        while not self.match(TokenType.SQCLOSE):
            list.append(self.parseExpr())
        return Expr(Token(TokenType.LIST, loc, lst), [])

    def parseBlock(self):
        self.match(TokenType.INDENT)
        block = []
        while not self.match(TokenType.DEDENT):
            block.append(self.parseExpr())
        return block

    def parseExpr(self):
        token = self.advance()
        if token.type == TokenType.LIT:
            if token.literal in TokenConsumeCount:
                 count = TokenConsumeCount[token.literal]
            else:
                count = 0
        else:
            assert token.type in TokenConsumeCount, f"{token.type} is not in TokenConsumeCount, please add how many arguments it has"
            count = TokenConsumeCount[token.type]

        subExpr = []
        for _ in range(count):
            if self.check(TokenType.INDENT):
                subExpr.append(self.parseBlock())
            else:
                subExpr.append(self.parseExpr())
        return Expr(token, subExpr)
    
    def parse(self):
        self.program = self.parseBlock()





