grammar CMinus;

program: declaration_list ;

declaration_list
    : declaration declaration_list
    | 
    ;

declaration
    : declaration_initial declaration_prime
    ;

declaration_initial
    : type_specifier ID
    ;

declaration_prime
    : fun_declaration_prime
    | var_declaration_prime
    ;

var_declaration_prime
    : LBRACK NUM RBRACK SEMI
    | SEMI
    ;

fun_declaration_prime
    : LPAREN params RPAREN compound_stmt
    ;

type_specifier
    : INT
    | VOID
    ;

params
    : INT ID param_prime param_list
    | VOID
    ;

param_list
    : COMMA param param_list
    | 
    ;

param
    : declaration_initial param_prime
    ;

param_prime
    : LBRACK RBRACK
    | 
    ;

compound_stmt
    : LBRACE declaration_list statement_list RBRACE
    ;

statement_list
    : statement statement_list
    | 
    ;

statement
    : expression_stmt
    | compound_stmt
    | selection_stmt
    | iteration_stmt
    | return_stmt
    ;

expression_stmt
    : expression SEMI
    | BREAK SEMI
    | SEMI
    ;

selection_stmt
    : IF LPAREN expression RPAREN statement ELSE statement
    ;

iteration_stmt
    : REPEAT statement UNTIL LPAREN expression RPAREN
    ;

return_stmt
    : RETURN return_stmt_prime
    ;

return_stmt_prime
    : SEMI
    | expression SEMI
    ;

expression
    : simple_expression_zegond
    | ID b
    ;

b
    : ASSIGN expression
    | LBRACK expression RBRACK h
    | simple_expression_prime
    ;

h
    : ASSIGN expression
    | g d c
    ;

simple_expression_zegond
    : additive_expression_zegond c
    ;

simple_expression_prime
    : additive_expression_prime c
    ;

c
    : relop additive_expression
    | 
    ;

relop
    : LT
    | EQ
    ;

additive_expression
    : term d
    ;

additive_expression_prime
    : term_prime d
    ;

additive_expression_zegond
    : term_zegond d
    ;

d
    : addop term d
    | 
    ;

addop
    : PLUS
    | MINUS
    ;

term
    : factor g
    ;

term_prime
    : factor_prime g
    ;

term_zegond
    : factor_zegond g
    ;

g
    : TIMES factor g
    | 
    ;

factor
    : LPAREN expression RPAREN
    | ID var_call_prime
    | NUM
    ;

var_call_prime
    : LPAREN args RPAREN
    | var_prime
    ;

var_prime
    : LBRACK expression RBRACK
    | 
    ;

factor_prime
    : LPAREN args RPAREN
    | 
    ;

factor_zegond
    : LPAREN expression RPAREN
    | NUM
    ;

args
    : arg_list
    | 
    ;

arg_list
    : expression arg_list_prime
    ;

arg_list_prime
    : COMMA expression arg_list_prime
    | 
    ;

// -------------------- Lexer rules ------------------------

IF      : 'if' ;
ELSE    : 'else' ;
INT     : 'int' ;
VOID    : 'void' ;
RETURN  : 'return' ;
BREAK   : 'break' ;
REPEAT  : 'repeat' ;
UNTIL   : 'until' ;

ASSIGN  : '=' ;
LT      : '<' ;
EQ      : '==' ;
PLUS    : '+' ;
MINUS   : '-' ;
TIMES   : '*' ;
SEMI    : ';' ;
COMMA   : ',' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
LBRACK  : '[' ;
RBRACK  : ']' ;
LBRACE  : '{' ;
RBRACE  : '}' ;

ID      : [a-zA-Z_][a-zA-Z_0-9]* ;
NUM     : [0-9]+ ;

WS      : [ \t\r\n]+ -> skip ;

