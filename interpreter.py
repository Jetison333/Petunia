from parser import TokenType, Parser

from enum import Enum, auto
from itertools import chain
import sys

class Enviroment():
    def __init__(self, parent = None, vars_ = None):
        if vars_ != None:
            self.vars = vars_
        else:
            self.vars = {}
        self.parent = parent

    def __iter__(self):
        if self.parent != None:
            return iter(chain(self.vars, self.parent.__iter__()))
        else:
            return iter(self.vars)

    def __getitem__(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            assert self.parent != None, f'Error {key} has not been defined'
            return self.parent[key]

    def __setitem__(self, key, val):
        if self.parent != None and key in self.parent:
            self.parent[key] = val
        else:
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

    def builtinOp(self, token, second, lineNum):
        match self.type:
            case VariableType.INT:
                assert second[0].type == VariableType.INT, f"Error: second operand of {token} can't be of type {second[0].type} at line {lineNum}"
                match token:
                    case TokenType.PLUS:
                        return Variable(VariableType.INT, self.lit + second[0].lit)
                    case TokenType.MUL:
                        return Variable(VariableType.INT, self.lit * second[0].lit)
                    case TokenType.DIV:
                        assert second[0].lit != 0, f"Error: Can't divide by zero at line {lineNum}"
                        return Variable(VariableType.INT, self.lit / second[0].lit)
                    case TokenType.GT:
                        return Variable(VariableType.BOOL, self.lit > second[0].lit)
                    case TokenType.LT:
                        return Variable(VariableType.BOOL, self.lit < second[0].lit)

    def isTrue(self, lineNum):
        if self.type == VariableType.BOOL:
            return self.lit
        else:
            assert False, f"Error: Can't implicitly case {self.type} to bool at line {lineNum}"
        
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

        case (TokenType.PLUS | TokenType.MUL | TokenType.DIV | TokenType.GT | TokenType.LT) as tokenType, _: #maybe change to [tokentype, _] if tokentype in operations syntax
            return evalExpr(expr.subExpr[0], enviroment).builtinOp(tokenType, [evalExpr(x, enviroment) for x in expr.subExpr[1:]], expr.token.lineNum)

        case TokenType.NUM, lit:
            return Variable(VariableType.INT, lit)

        case TokenType.IF, _:
            if evalExpr(expr.subExpr[0], enviroment).isTrue(expr.token.lineNum):
                return evalExpr(expr.subExpr[1], enviroment)
            else:
                return evalExpr(expr.subExpr[2], enviroment)

        case TokenType.WHILE, _:
            while evalExpr(expr.subExpr[0], enviroment).isTrue(expr.token.lineNum):
                returnVal = evalExpr(expr.subExpr[1], enviroment)
            return returnVal
        
        case TokenType.SET, _:
            key = expr.subExpr[0].token.literal
            enviroment[key] = evalExpr(expr.subExpr[1], enviroment)
        
        case _, _:
            raise NotImplementedError(f'{expr.token.type} is not implemented')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            program = f.read()
        try:
            interpret(program)
        except AssertionError as error:
            print(error)



