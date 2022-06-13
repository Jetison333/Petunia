from parser import TokenType, Parser

from enum import Enum, auto
from itertools import chain
import sys

def is_int(x):
    try:
        int(x)
        return True
    except:
        return False

def is_float(x):
    try:
        float(x)
        return True
    except:
        return False


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

class Variable():
    def __init__(self, type_, lit, lineNum = -1):
        self.type = type_
        self.lit = lit
        match self.type:
            case TokenType.INT:
                assert is_int(self.lit), f'Error: invalid literal for type int at line {lineNum}'

    def __repr__(self):
        return f'<Variable object, type = {self.type}, literal = {self.lit}>'

    def builtinOp(self, token, second, lineNum):
        #print(token,self,second)
        match self.type:
            case TokenType.INT:
                if second[0].type == TokenType.FLOAT:
                    return second[0].builtinOp(token, [self], lineNum)
                assert second[0].type == TokenType.INT, f"Error: second operand of {token} can't be of type {second[0].type} at line {lineNum}"
                match token:
                    case TokenType.PLUS:
                        return Variable(TokenType.INT, self.lit + second[0].lit)
                    case TokenType.MUL:
                        return Variable(TokenType.INT, self.lit * second[0].lit)
                    case TokenType.DIV:
                        assert second[0].lit != 0, f"Error: Can't divide by zero at line {lineNum}"
                        return Variable(TokenType.INT, self.lit // second[0].lit)
                    case TokenType.GT:
                        return Variable(TokenType.BOOL, self.lit > second[0].lit)
                    case TokenType.LT:
                        return Variable(TokenType.BOOL, self.lit < second[0].lit)
                    
            case TokenType.FLOAT:
                assert second[0].type == TokenType.INT or second[0].type == TokenType.FLOAT, f"Error: second operand of {token} can't be of type {second[0].type} at line {lineNum}"
                match token:
                    case TokenType.PLUS:
                        return Variable(TokenType.FLOAT, self.lit + second[0].lit)
                    case TokenType.MUL:
                        return Variable(TokenType.FLOAT, self.lit * second[0].lit)
                    case TokenType.DIV:
                        assert second[0].lit != 0, f"Error: Can't divide by zero at line {lineNum}"
                        return Variable(TokenType.FLOAT, self.lit / second[0].lit)
                    case TokenType.GT:
                        return Variable(TokenType.BOOL, self.lit > second[0].lit)
                    case TokenType.LT:
                        return Variable(TokenType.BOOL, self.lit < second[0].lit)
            case other:
                raise NotImplementedError(f'The type {other} does not have implemented operations')

    def isTrue(self, lineNum):
        if self.type == TokenType.BOOL:
            return self.lit
        else:
            assert False, f"Error: Can't implicitly cast {self.type} to bool at line {lineNum}"
        
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
                    print(evalExpr(expr.subExpr[0], enviroment).lit)
                case varName:
                    return enviroment[varName]

        case (TokenType.PLUS | TokenType.MUL | TokenType.DIV | TokenType.GT | TokenType.LT) as tokenType, _: #maybe change to [tokentype, _] if tokentype in operations syntax
            return evalExpr(expr.subExpr[0], enviroment).builtinOp(tokenType, [evalExpr(x, enviroment) for x in expr.subExpr[1:]], expr.token.lineNum)

        case TokenType.INT, lit:
            return Variable(TokenType.INT, lit)

        case TokenType.FLOAT, lit:
            return Variable(TokenType.FLOAT, lit)

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
            value = evalExpr(expr.subExpr[1], enviroment)
            assert key in enviroment, f'Error: tried setting an uninitialized variable at {expr.token.lineNum}'
            assert enviroment[key].type == value.type, f"Error: Can't implicitly cast {enviroment[key].type} to {value.type} at line {expr.token.lineNum}"
            enviroment[key] = value

        case TokenType.NEW, _:
            vartype = expr.subExpr[0].token.type
            assert vartype != TokenType.LIT, f'Error: {vartype} is not a valid type at {expr.token.lineNum}'
            key = expr.subExpr[1].token.literal
            value = Variable(vartype, expr.subExpr[2].token.literal, expr.token.lineNum)
            enviroment[key] = value
        
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



