from parser import TokenType, Parser
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
            assert parent != None, f'Error {key} has not been defined'
            return parent[key]

    def __setitem__(self, key, val):
        env = self
        while env != None and not key in env.vars:
            env = env.parent
        if env != None:
            env.vars[key] = val
        else:
            self.vars[key] = val

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
                case literal:
                    return enviroment[literal]
                

        case TokenType.PLUS, _:
            return evalExpr(expr.subExpr[0], enviroment) + evalExpr(expr.subExpr[1], enviroment)

        case TokenType.MUL, _:
            return evalExpr(expr.subExpr[0], enviroment) * evalExpr(expr.subExpr[1], enviroment)
        

        case TokenType.NUM, lit:
            return lit

        case TokenType.LIST, lit:
            lst = []
            for item in expr.subExpr:
                lst.append(evalExpr(item, enviroment))
            return lst
                    
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


