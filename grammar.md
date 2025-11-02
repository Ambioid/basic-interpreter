# Very Incomplete but Useful Syntax Spec

```ebnf
program ::= block* end-line
block ::= (line | for-block)*
line ::= line-number statement end-of-line
line-number ::= digit digit? digit? digit?
end-of-line ::= '\n'
end-statement ::= 'END'
statement ::= data-statement | def-statement | dimension-statement | gosub-statement | goto-statement | if-then-statement | input-statement | let-statement | on-goto-statement | option-statement | print-statement | randomize-statement | read-statement | remark-statement |restore-statement | return-statement | stop-statement

for-block ::= for-line for-body
for-body ::= block next-line
for-line ::= line-number for-statement end-of-line
next-line ::= line-number next-statement end-of-line
for-statement ::= 'FOR' control-variable equals-sign initial-value 'TO' limit ('STEP' increment)?
control-variable ::= simple-numeric-variable
initial-value ::= numeric-expression
limit ::= numeric-expression
increment ::= numeric-expression
next-statement ::= 'NEXT' control-variable

data-statement ::= 'DATA' data-list
data-list ::= datum (comma datum)*
datum ::= quoted-string | unquoted-string

def-statement ::= 'DEF' numeric-defined-function parameter-list? equals-sign numeric-expression
numeric-defined-function ::= 'FN' letter
parameter-list ::= left-parenthesis parameter right-parenthesis
parameter ::= simple-numeric-variable
simple-numeric-variable ::= letter digit?

numeric-expression ::= sign? term (sign term)*
term ::= factor (multiplier factor)*
factor ::= primary (caret primary)*
primary ::= numeric-variable | numeric-rep | numeric-function-ref | left-parenthesis numeric-expression right-parenthesis
numeric-function-ref ::= numeric-function-name argument-list?
numeric-function-name ::= numeric-defined-function | numeric-supplied-function
numeric-supplied-function ::= ABS | ATN | COS | EXP | INT | LOG | RND | SGN | SIN | SQR | TAN
argument-list ::= left-parenthesis numeric-expression right-parenthesis

numeric-variable ::= simple-numeric-variable | numeric-array-element
numeric-array-element ::= numeric-array-name subscript
numeric array-name ::= letter
subscript ::= left-parenthesis numeric-expression (comma numeric-expression)? right-parenthesis

dimension-statement ::= 'DIM' array-declaration (comma array-declaration)*
array-declaration ::= numeric-array-name left-parenthesis bounds right-parenthesis
bounds ::= integer (comma integer)?

option-statement ::= 'OPTION BASE' ('0' | '1')

gosub-statement ::= 'GO' space* 'SUB' line-number
goto-statement ::= 'GO' space* 'TO' line-number

if-then-statement ::= 'IF' relational-expression 'THEN' line-number
relational-expression ::= numeric-expression relation numeric-expression | string-expression equality-relation string-expression
relation ::= equality-relation | less-than-sign | greater-than-sign | not-less | not-greater
equality-relation ::= equals-sign | not-equals

return-statement ::= 'RETURN'
on-goto-statement ::= 'ON' numeric-expression 'GO' space* 'TO' line-number (comma line-number)*

print-statement ::= 'PRINT' print-list?
print-list ::= (print-item? print-separator)* print-item?
print-item ::= expression | tab-call
tab-call ::= 'TAB' left-parenthesis numeric-expression right-parenthesis

randomize-statement ::= 'RANDOMIZE'

read-statement ::= 'READ' variable-list

variable-list ::= variable (comma variable)*
variable ::= numeric-variable | string-variable

restore-statement ::= 'RESTORE'
stop-statement ::= 'STOP'
```
