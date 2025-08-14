from Parser import init_grammar
from Parser.parser import LL1
from scanner.default_scanner import build_scanner
from scanner.tokens import Token, TokenType
from tables import tables
from code_gen import CodeGen



tables.symbol_table.add_symbol(Token(TokenType.ID, "output"))
tables.symbol_table.fetch("output").address = 5
tables.symbol_table.export("symbol_table.txt")
parser = LL1(build_scanner("input.txt"), init_grammar(),CodeGen())
parser.generate_parse_tree()
parser.export_parse_tree("parse_tree.txt")
parser.export_syntax_error("syntax_errors.txt")



parser.code_gen.execute_from("main")
parser.export_code("output.txt")
