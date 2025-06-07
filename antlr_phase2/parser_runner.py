from antlr4 import *
from CMinusLexer import CMinusLexer
from CMinusParser import CMinusParser
from antlr4.error.DiagnosticErrorListener import DiagnosticErrorListener
import sys

# فایل ورودی input.txt رو بخون
input_stream = FileStream("input.txt", encoding="utf-8")

# ساخت lexer و parser
lexer = CMinusLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = CMinusParser(token_stream)

# ذخیره خطاها در فایل
with open("syntax_errors.txt", "w", encoding="utf-8") as err_file:
    parser.removeErrorListeners()
    parser.addErrorListener(DiagnosticErrorListener())
    sys.stderr = err_file  # ارورها بره تو فایل
    tree = parser.program()

# ساخت درخت نحوی
def write_tree(tree, parser, indent=0):
    output = "  " * indent + tree.getText() + "\n"
    for child in tree.getChildren():
        if isinstance(child, TerminalNode):
            output += "  " * (indent + 1) + child.getText() + "\n"
        else:
            output += write_tree(child, parser, indent + 1)
    return output

with open("parse_tree.txt", "w", encoding="utf-8") as tree_file:
    tree_str = write_tree(tree, parser)
    tree_file.write(tree_str)

print("✅ تجزیه کامل شد. خروجی‌ها در syntax_errors.txt و parse_tree.txt ذخیره شدن.")
