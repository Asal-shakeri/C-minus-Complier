from Parser import init_grammar
from Parser.parser import LL1
from scanner.default_scanner import build_scanner
from scanner.tokens import Token, TokenType
from tables import tables




tables.symbol_table.add_symbol(Token(TokenType.ID, "output"))
tables.symbol_table.fetch("output").address = 5
parser = LL1(build_scanner("input.txt"), init_grammar())
parser.generate_parse_tree()
if parser.semantic_analyzer.errors:
    with open("semantic_errors.txt", "w") as f:
        for err in parser.semantic_analyzer.errors:
            f.write(err + "\n")
    with open("output.txt", "w") as f:
        f.write("The output code has not been generated\n")
else:
    with open("semantic_errors.txt", "w") as f:
        f.write("The input program is semantically correct.\n")

parser.export_parse_tree("parse_tree.txt")e
parser.export_syntax_error("syntax_errors.txt")
