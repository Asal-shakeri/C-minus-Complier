from Parser import init_grammar
from Parser.parser import LL1
from scanner.default_scanner import build_scanner
from scanner.tokens import Token, TokenType
from tables import tables




tables.symbol_table.add_symbol(Token(TokenType.ID, "output"))
tables.symbol_table.fetch("output").address = 5
parser = LL1(build_scanner("input.txt"), init_grammar())
parser.generate_parse_tree()
parser.export_parse_tree("parse_tree.txt")
parser.export_syntax_error("syntax_errors.txt")
