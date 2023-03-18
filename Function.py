from DataType import DataType
from TokenType import TokenType
from token_petunia import Token
#from interpreter_petunia import evalExpr, Enviroment

class Function():
    def __init__(self, name, type, params, body, linenum):
        self.name = name
        self.type = DataType(type)
        self.params = params
        self.body = body
        self.token = Token(TokenType.FUNC, linenum)

    def bindArgs(self, enviroment, args):
        for i, arg in enumerate(args):
            assert self.params[i][0] == arg.type, f"Type of {arg.type} does not match {self.params[i][0]} in function call to {self.name} at line {self.token.lineNum}"
            enviroment.additem(self.params[i][1], arg)
        return enviroment

    def __repr__(self):
        return f"{{Funciton object, name: {self.name}, type: {self.type}, args: {self.params}, body: {self.body}, token: {self.token}}}"
        
        