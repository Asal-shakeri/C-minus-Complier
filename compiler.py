from Parser import init_grammar
from Parser.parser import LL1
from code_gen.code_gen import Helper
from scanner.default_scanner import build_scanner
from scanner.tokens import Token, TokenType
from tables import tables
from code_gen import CodeGen

def run_code_gen() -> None:

    try:
        ast = Helper.deserialize_ast('ast.json')
        if ast is None:
            print("ast.json is empty or not found. Skipping code generation.")
            print("--------------------------------------\n")
            return
        gen = CodeGen(ast)
        code = gen.generate()
        with open('output.txt', "w", encoding="utf-8") as w:
            for line in code:
                w.write(str(line) + "\n")
        print(f"Successfully generated code to {'output.txt'}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
    print("--------------------------------------\n")

tables.symbol_table.add_symbol(Token(TokenType.ID, "output"))
tables.symbol_table.fetch("output").address = 5
tables.symbol_table.export("symbol_table.txt")
parser = LL1(build_scanner("input.txt"), init_grammar(),None)
parser.generate_parse_tree()
parser.export_ast('.')
parser.export_parse_tree("parse_tree.txt")
parser.export_syntax_error("syntax_errors.txt")

run_code_gen()
# parser.code_gen.execute_from("main")
# parser.export_code("output.txt")


