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

    def __bool__(self):
        match self.type:
            case VariableType.BOOL:
                return self.lit
            case other:
                assert False, f"{other} can't be implicitly casted to bool"

    def __add__(self, other):
        match self.type:
            case VariableType.INT:
                return Variable(VariableType.INT, self.lit + other.lit)
            case other:
                assert False, f"{other} is unimplemented"

    def __mul__(self, other):
        match self.type:
            case VariableType.INT:
                return Variable(VariableType.INT, self.lit * other.lit)
            case other:
                assert False, f"{other} is unimplemented"

    def __gt__(self, other):
        match self.type:
            case VariableType.INT:
                return Variable(VariableType.BOOL, self.lit > other.lit)
            case other:
                assert False, f"{other} is unimplemented"

    def __lt__(self, other):
        match self.type:
            case VariableType.INT:
                return Variable(VariableType.BOOL, self.lit < other.lit)
            case other:
                assert False, f"{other} is unimplemented"


        
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
                

        case TokenType.PLUS, _:
            return evalExpr(expr.subExpr[0], enviroment) + evalExpr(expr.subExpr[1], enviroment)

        case TokenType.MUL, _:
            return evalExpr(expr.subExpr[0], enviroment) * evalExpr(expr.subExpr[1], enviroment)
        

        case TokenType.NUM, lit:
            return Variable(VariableType.INT, lit)

        case TokenType.IF, _:
            if evalExpr(expr.subExpr[0], enviroment):
                return evalExpr(expr.subExpr[1], enviroment)
            else:
                return evalExpr(expr.subExpr[2], enviroment)
            
        case TokenType.SET, _:
            key = expr.subExpr[0].token.literal
            enviroment[key] = evalExpr(expr.subExpr[1], enviroment)
            

        case TokenType.GT, _:
            return evalExpr(expr.subExpr[0], enviroment) > evalExpr(expr.subExpr[1], enviroment)

        case TokenType.LT, _:
            return evalExpr(expr.subExpr[0], enviroment) < evalExpr(expr.subExpr[1], enviroment)
        
        case _, _:
            raise NotImplementedError(f'{expr.token.type} is not implemented')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            program = f.read()
        interpret(program)


