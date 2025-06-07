lexer grammar MyLexer;

// Keywords
IF      : 'if';
ELSE    : 'else';
VOID    : 'void';
INT     : 'int';
REPEAT  : 'repeat';
BREAK   : 'break';
UNTIL   : 'until';
RETURN  : 'return';

// Symbols
SEMI    : ';';
COMMA   : ',';
LBRACK  : '[';
RBRACK  : ']';
LPAREN  : '(';
RPAREN  : ')';
LBRACE  : '{';
RBRACE  : '}';
PLUS    : '+';
MINUS   : '-';
STAR    : '*';
EQUAL   : '=';
EQ      : '==';
NEQ     : '!=';

// Identifiers and numbers
ID      : [a-zA-Z] [a-zA-Z0-9]*;
NUM     : [0-9]+;

// Comments and whitespace
COMMENT : '/*' .*? '*/' -> skip;
WS      : [ \t\r\n]+ -> skip;

// Invalid
INVALID : . ;

