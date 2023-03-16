from TokenType import TokenType
from copy import deepcopy

class DataType:
    def __init__(self, expr):
        self.subtype = []
        if (isinstance(expr, TokenType)):
            self.type = expr
        else:
            self.type = expr.token.type
            for exp in expr.subExpr:
                self.subtype.append(DataType(exp))
    
    def __eq__(self, second):
        if (isinstance(second, TokenType)):
            if self.subtype != []:
                return False
            return self.type == second
        return self.type == second.type and self.subtype == second.subtype
    
    def __repr__(self):
        #return f"{{DataType, type: {self.type}, subtype: {self.subtype}}}" #debug print
        retString = f"{self.type.value}"
        for datatype in self.subtype:
            retString += ' ' + datatype.__repr__()
        return retString


    def addArray(self):
        self = deepcopy(self)
        self.subtype = [deepcopy(self)]
        self.type = TokenType.ARRAY
        return self
    
    def isArray(self):
        return self.type == TokenType.ARRAY