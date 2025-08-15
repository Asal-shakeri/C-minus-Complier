class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def check(self, action, token, extra_info=None):
        if action == "ID_USAGE":
            if token.value not in self.symbol_table:
                self.errors.append(f"{token.lineno}: Semantic Error! '{token.value}' is not defined")

    def define(self, name, type_, lineno):
        if type_ == "void":
            self.errors.append(f"{lineno}: Semantic Error! Illegal type of void for '{name}'")
        return


        if name in self.symbol_table:
            self.errors.append(f"{lineno}: Semantic Error! Redeclaration of '{name}'")
        else:
            self.symbol_table[name] = type_
