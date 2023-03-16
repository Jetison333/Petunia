from token_petunia import TokenType

tokenConsumeCount = {
    TokenType.INT : 0,
    TokenType.FLOAT : 0,
    TokenType.ARRAY : 1,

    TokenType.AT : 2,

    TokenType.IF : 3,
    TokenType.WHILE : 2,

    TokenType.NEW : 3,
    TokenType.SET : 2, 
    TokenType.SETAT : 3,

    TokenType.LT : 2,
    TokenType.GT : 2,
    TokenType.EQUAL : 2,

    TokenType.PLUS : 2,
    TokenType.MUL : 2,
    TokenType.DIV : 2,
    TokenType.NUM : 0,

    TokenType.INDENT : 0,
    TokenType.DEDENT : 1,

    TokenType.APPEND : 2,
}

litConsumeCount = {
    'print' : 1,
    'make_array' : 2,
}