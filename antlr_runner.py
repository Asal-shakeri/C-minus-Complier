from antlr4 import *
from MyLexer import MyLexer
from collections import defaultdict

def run_antlr_tokenizer(input_file='input.txt', output_file='ANTLR_p1.txt'):
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = MyLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()

    lines = defaultdict(list)
    for token in token_stream.tokens:
        ttype = lexer.symbolicNames[token.type]
        if ttype in {'WS', 'COMMENT'}:
            continue
        lines[token.line].append(f'({ttype}, {token.text})')

    with open(output_file, 'w', encoding='utf-8') as f:
        for lineno in sorted(lines.keys()):
            f.write(f'{lineno} {" ".join(lines[lineno])}\n')

