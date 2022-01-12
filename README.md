# Petunia
Petunia is an esoteric ish programming language. it uses prefix notation for everything, meaning you don't need paranthesis for precedence. Even control flow follows prefix notation, for example if statements expect three operands; something that evaluates to true or false, and then two expresions. the if statement only evaluates one of the expressions and passes on that value.

functions also use prefix notation and fit in the same places as other operations. in this way its similar to forth, so that you can define words and build them up into larger actions. 

the language is more functional than object oriented. functions can have no side effects on objects (but can have side effects like printing or modifying files) except when objects use a specific syntax (that really is just passing the object to a function and then setting that object equal to the result). In general objects work the way that I want them too, and ill make that notion more rigourous later.

some sytax examples:

```
print 'Hello World!'

def fib Int <- Int n
    if < n 1
        n
        --
        + fib - n 1 fib - n 2
```
        
some notes about the fib function: if evaluates to the branch decided by < n 1 and the function returns that value. A function definition expects one expression and returns what that expresion evaluate to, meaning there isn't a explicit return command.

An expresion can also be a block, which is a newline followed by an ident of four spaces. A block can have many expressions, and evaluates to whatever the last expression in the block evaluates too. this is useful when using variables, and allows padding things to make them more readable. A '--' seperates two blocks with the same indentation.


