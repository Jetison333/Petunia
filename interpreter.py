from parser import TokenType, Parser

from enum import Enum, auto
import sys

class Enviroment():
    def __init__(self, parent = None, vars_ = None):
        if vars_ != None:
            self.vars = vars_
        else:
            self.vars = {}
        self.parent = parent

    def __getitem__(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            assert self.parent != None, f'Error {key} has not been defined'
            return self.parent[key]

    def __setitem__(self, key, val):
        self.vars[key] = val

class VariableType(Enum):
    INT = auto()
    BOOL = auto()

class Variable():
    def __init__(self, type_, lit):
        self.type = type_
        self.lit = lit

    def __repr__(self):
        return str(self.lit)

    def builtinOp(self, token, second):
        match self.type:
            case VariableType.INT:
                match token:
                    case TokenType.PLUS:
                        return Variable(VariableType.INT, self.lit + second[0].lit)
                    case TokenType.MUL:
                        return Variable(VariableType.INT, self.lit * second[0].lit)
                    case TokenType.GT:
                        return Variable(VariableType.BOOL, self.lit > second[0].lit)
                    case TokenType.LT:
                        return Variable(VariableType.BOOL, self.lit < second[0].lit)

    def isTrue(self):
        if self.type == VariableType.BOOL:
            return self.lit
        else:
            assert false, f"Error: Can't implicitly case {self.type} to bool"
        
def interpret(program):
    program = Parser(program).program
    global_env = Enviroment()
    for ins in program:
        evalExpr(ins, global_env)
        
def evalExpr(expr, enviroment):
    if isinstance(expr, list):
        subenv = Enviroment(enviroment)
        for ins in expr:
            res = evalExpr(ins, subenv)
        return res
    
    match expr.token.type, expr.token.literal:
        case TokenType.LIT, literal: #eventually change to look up the literal in the enviroment
            match literal:
                case 'print':
                    print(evalExpr(expr.subExpr[0], enviroment))
                case varName:
                    return enviroment[varName]

        case (TokenType.PLUS | TokenType.MUL | TokenType.GT | TokenType.LT) as tokenType, _: #maybe change to [tokentype, _] if tokentype in operations syntax
            return evalExpr(expr.subExpr[0], enviroment).builtinOp(tokenType, [evalExpr(x, enviroment) for x in expr.subExpr[1:]])

        case TokenType.NUM, lit:
            return Variable(VariableType.INT, lit)

        case TokenType.IF, _:
            if evalExpr(expr.subExpr[0], enviroment).isTrue():
                return evalExpr(expr.subExpr[1], enviroment)
            else:
                return evalExpr(expr.subExpr[2], enviroment)
            
        case TokenType.SET, _:
            key = expr.subExpr[0].token.literal
            enviroment[key] = evalExpr(expr.subExpr[1], enviroment)
        
        case _, _:
            raise NotImplementedError(f'{expr.token.type} is not implemented')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            program = f.read()
        interpret(program)


