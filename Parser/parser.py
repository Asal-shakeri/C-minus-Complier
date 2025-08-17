from anytree import Node, RenderTree, PreOrderIter
from scanner.tokens import TokenType
import os
import json


class NoTokenLeftException(Exception):
    pass


# =========================
# ===== AST STRUCTURE =====
# =========================
class AstNode:
    """
    A node in the Abstract Syntax Tree.
    Compatible with the JSON shape used by the downstream phases.
    """
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type  # E.g., 'FunDecl', 'Assign', 'IfStmt', 'ID', 'NUM'
        self.value = value          # E.g., a variable name 'x', a number '10'
        self.children = children if children is not None else []

    def to_dict(self):
        valid_children = [child for child in self.children if child is not None]
        return {
            "NodeType": self.node_type,
            "Value": self.value,
            "Children": [child.to_dict() for child in valid_children]
        }


# ============================================
# ===== A minimal RD parser to build AST =====
# =====  (ported from your code #2)       =====
# ============================================
class AstParser:
    def __init__(self, tokens):
        """
        tokens: list of tuples (line_no: int, type_name: str, lexeme: str)
        Example: (12, "ID", "foo") or (34, "NUM", "123") or (56, "EOF", "$")
        """
        self.tokens = tokens
        self.current_index = 0
        self.current_token = self.tokens[self.current_index] if self.tokens else (0, "EOF", "$")
        self.syntax_errors = []
        self.error_encountered = False
        self.error_line = None
        self.ast_root = None

    # -------------------- util --------------------
    def _advance(self):
        if self.current_index < len(self.tokens) - 1:
            self.current_index += 1
            self.current_token = self.tokens[self.current_index]
        else:
            last_line = self.current_token[0]
            self.current_token = (last_line, "EOF", "$")

    def match(self, expected_lexeme):
        if self.current_token[2] == expected_lexeme:
            node = AstNode(self.current_token[1], self.current_token[2])
            self._advance()
            return node
        else:
            self._record_syntax_error(f"Unexpected token '{self.current_token[2]}', expected '{expected_lexeme}'")
            return None

    def _record_syntax_error(self, message):
        if not self.error_encountered or self.error_line != self.current_token[0]:
            self.error_line = self.current_token[0]
            self.syntax_errors.append(f"#{self.current_token[0]} : syntax error, {message}")
            self.error_encountered = True
            self._panic_mode()

    def _panic_mode(self):
        synchronization_tokens = [";", "{", "}", "if", "repeat", "return", "int", "void", "$", "else", "until"]
        while self.current_token[2] not in synchronization_tokens and self.current_token[2] != "$":
            self._advance()
        if self.current_token[2] in [";", "}"]:
            self._advance()  # consume to prevent infinite loops
        self.error_encountered = False

    # -------------------- entry --------------------
    def parse_program(self):
        declarations = self._handle_declaration_list()
        self.ast_root = AstNode("Program", children=declarations)
        if self.current_token[2] != "$":
            self._record_syntax_error(f"Unexpected token '{self.current_token[2]}' at end of file.")
        return self.ast_root

    # -------------- grammar handlers --------------
    def _handle_declaration_list(self):
        nodes = []
        while self.current_token[2] in ["int", "void"]:
            declaration_node = self._handle_declaration()
            if declaration_node:
                nodes.append(declaration_node)
        return nodes

    def _handle_declaration(self):
        type_node = self._handle_type_specifier()
        if self.current_token[1] != "ID":
            self._record_syntax_error("missing ID")
            return None
        id_node = AstNode("ID", self.current_token[2])
        self._advance()

        if self.current_token[2] == "(":
            return self._handle_fun_declaration(type_node, id_node)
        else:
            return self._handle_var_declaration(type_node, id_node)

    def _handle_var_declaration(self, type_node, id_node):
        if self.current_token[2] == "[":
            self.match("[")
            if self.current_token[1] != "NUM":
                self._record_syntax_error("Expected NUM in array declaration")
                return None
            num_node = AstNode("NUM", self.current_token[2])
            self._advance()
            self.match("]")
            self.match(";")
            return AstNode("ArrayDecl", children=[type_node, id_node, num_node])
        else:
            self.match(";")
            return AstNode("VarDecl", children=[type_node, id_node])

    def _handle_fun_declaration(self, type_node, id_node):
        self.match("(")
        params_node = self._handle_params()
        self.match(")")
        compound_stmt_node = self._handle_compound_stmt()
        return AstNode("FunDecl", children=[type_node, id_node, params_node, compound_stmt_node])

    def _handle_type_specifier(self):
        if self.current_token[2] in ["int", "void"]:
            node = AstNode("TypeSpecifier", self.current_token[2])
            self._advance()
            return node
        else:
            self._record_syntax_error("illegal type specifier")
            return None

    def _handle_params(self):
        param_nodes = []
        if self.current_token[2] == "void":
            void_node = AstNode("TypeSpecifier", self.current_token[2])
            self._advance()
            if self.current_token[2] == ")":
                param_nodes.append(AstNode("Param", children=[void_node]))
            else:  # void ID, ...
                param_nodes.append(self._handle_param(void_node))
                while self.current_token[2] == ",":
                    self.match(",")
                    type_node = self._handle_type_specifier()
                    param_nodes.append(self._handle_param(type_node))
        elif self.current_token[2] == "int":
            type_node = self._handle_type_specifier()
            param_nodes.append(self._handle_param(type_node))
            while self.current_token[2] == ",":
                self.match(",")
                type_node = self._handle_type_specifier()
                param_nodes.append(self._handle_param(type_node))

        return AstNode("Params", children=param_nodes)

    def _handle_param(self, type_node):
        if self.current_token[1] != "ID":
            self._record_syntax_error("missing ID in parameter")
            return None
        id_node = AstNode("ID", self.current_token[2])
        self._advance()

        if self.current_token[2] == "[":
            self.match("[")
            self.match("]")
            return AstNode("ArrayParam", children=[type_node, id_node])
        else:
            return AstNode("Param", children=[type_node, id_node])

    def _handle_compound_stmt(self):
        self.match("{")
        local_declarations = self._handle_declaration_list()
        statements = self._handle_statement_list()
        self.match("}")
        return AstNode("CompoundStmt", children=local_declarations + statements)

    def _handle_statement_list(self):
        nodes = []
        follow_set = ["}"]
        first_set = ["if", "repeat", "return", "break", ";", "{", "(", "ID", "NUM"]
        while self.current_token[2] not in follow_set and (self.current_token[2] in first_set or self.current_token[1] in first_set):
            stmt_node = self._handle_statement()
            if stmt_node:
                nodes.append(stmt_node)
        return nodes

    def _handle_statement(self):
        if self.current_token[2] == "{":
            return self._handle_compound_stmt()
        elif self.current_token[2] == "if":
            return self._handle_selection_stmt()
        elif self.current_token[2] == "repeat":
            return self._handle_iteration_stmt()
        elif self.current_token[2] == "return":
            return self._handle_return_stmt()
        else:
            return self._handle_expression_stmt()

    def _handle_expression_stmt(self):
        if self.current_token[2] == "break":
            node = AstNode("BreakStmt")
            self._advance()
            self.match(";")
            return node
        elif self.current_token[2] == ";":
            self.match(";")
            return AstNode("EmptyStmt")
        else:
            expr_node = self._handle_expression()
            self.match(";")
            return expr_node

    def _handle_selection_stmt(self):
        self.match("if")
        self.match("(")
        condition = self._handle_expression()
        self.match(")")
        then_stmt = self._handle_statement()
        else_stmt = None
        if self.current_token[2] == "else":
            self.match("else")
            else_stmt = self._handle_statement()
        return AstNode("IfStmt", children=[condition, then_stmt, else_stmt])

    def _handle_iteration_stmt(self):
        self.match("repeat")
        body = self._handle_statement()
        self.match("until")
        self.match("(")
        condition = self._handle_expression()
        self.match(")")
        return AstNode("RepeatStmt", children=[body, condition])

    def _handle_return_stmt(self):
        self.match("return")
        expr = None
        if self.current_token[2] != ";":
            expr = self._handle_expression()
        self.match(";")
        return AstNode("ReturnStmt", children=[expr] if expr else [])

    def _handle_expression(self):
        # assignment: ID = expression
        if self.current_token[1] == "ID":
            if self.current_index + 1 < len(self.tokens) and self.tokens[self.current_index + 1][2] == "=":
                var_node = self._handle_var()
                self.match("=")
                expr_node = self._handle_expression()
                return AstNode("Assign", children=[var_node, expr_node])
        return self._handle_simple_expression()

    def _handle_simple_expression(self):
        node = self._handle_additive_expression()
        if self.current_token[2] in ["<=", "==", "<"]:
            op_node = self._handle_relop()
            right_node = self._handle_additive_expression()
            op_node.children = [node, right_node]
            return op_node
        return node

    def _handle_relop(self):
        if self.current_token[2] in ["<=", "==", "<"]:
            node = AstNode("RelOp", self.current_token[2])
            self._advance()
            return node
        return None

    def _handle_additive_expression(self):
        node = self._handle_term()
        while self.current_token[2] in ["+", "-"]:
            op_node = self._handle_addop()
            right_node = self._handle_term()
            op_node.children = [node, right_node]
            node = op_node
        return node

    def _handle_addop(self):
        if self.current_token[2] in ["+", "-"]:
            node = AstNode("AddOp", self.current_token[2])
            self._advance()
            return node
        return None

    def _handle_term(self):
        node = self._handle_factor()
        while self.current_token[2] == "*":
            op_node = AstNode("MulOp", self.current_token[2])
            self.match("*")
            right_node = self._handle_factor()
            op_node.children = [node, right_node]
            node = op_node
        return node

    def _handle_factor(self):
        if self.current_token[2] == "(":
            self.match("(")
            node = self._handle_expression()
            self.match(")")
            return node
        elif self.current_token[1] == "ID":
            id_node = AstNode("ID", self.current_token[2])
            self._advance()
            if self.current_token[2] == "(":
                return self._handle_call(id_node)
            else:
                return self._handle_var(id_node)
        elif self.current_token[1] == "NUM":
            node = AstNode("NUM", self.current_token[2])
            self._advance()
            return node
        else:
            self._record_syntax_error("Expected '(', ID, or NUM")
            return None

    def _handle_var(self, id_node=None):
        if not id_node:
            if self.current_token[1] != "ID":
                self._record_syntax_error("Expected ID for variable")
                return None
            id_node = AstNode("ID", self.current_token[2])
            self._advance()
        if self.current_token[2] == "[":
            self.match("[")
            index_expr = self._handle_expression()
            self.match("]")
            return AstNode("ArrayVar", children=[id_node, index_expr])
        return AstNode("SimpleVar", children=[id_node])

    def _handle_call(self, id_node):
        self.match("(")
        args_node = self._handle_args()
        self.match(")")
        return AstNode("Call", children=[id_node, args_node])

    def _handle_args(self):
        arg_nodes = []
        if self.current_token[2] != ")":
            arg_nodes.append(self._handle_expression())
            while self.current_token[2] == ",":
                self.match(",")
                arg_nodes.append(self._handle_expression())
        return AstNode("Args", children=arg_nodes)

    # -------------------- outputs --------------------
    def write_outputs(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "syntax_errors.txt"), "w", encoding="utf-8") as f:
            if not self.syntax_errors:
                f.write("There is no syntax error.\n")
            else:
                sorted_errors = sorted(self.syntax_errors, key=lambda e: int(e.split(' ')[0][1:]))
                for error in sorted_errors:
                    f.write(error + "\n")
        ast_file_path = os.path.join(output_dir, "ast.json")
        with open(ast_file_path, "w", encoding="utf-8") as f:
            if self.ast_root and not self.syntax_errors:
                json.dump(self.ast_root.to_dict(), f, indent=2)
            else:
                f.write("{}\n")


# ==============================================
# ===== Original LL(1) parser — augmented  =====
# ===== to capture tokens & export an AST  =====
# ==============================================
class LL1:
    def __init__(self, token_generator, grammar, code_generator):
        self.token_generator = token_generator
        self.grammar = grammar
        self.code_gen = code_generator
        self.p_table = {}
        self.stack = []
        self.errors = []
        self.create_parse_table()
        self.root = Node(self.grammar.rules[0].left.name)

        # --- NEW: keep a linear snapshot of the significant tokens for AST ---
        # shape: (line_no, type_name, lexeme)
        self._ast_tokens = []

    # ---------------- parse table ----------------
    def create_parse_table(self):
        self.update_productions()
        self.update_synchs()

    def update_synchs(self):
        for nt in self.grammar.non_terminals:
            for item in nt.follow:
                if (nt.name, item.name) not in self.p_table:
                    self.p_table[(nt.name, item.name)] = "synch"

    def update_productions(self):
        for rule in self.grammar.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left.name, predict.name)] = [p.name for p in rule.right]

    # ----------------- errors -----------------
    def add_error(self, error_root, error_type):
        line_no = self.token_generator.get_line_no()
        if error_type.lower() == "missing":
            self.errors.append((line_no, f"{error_type} {error_root.name}"))
        elif error_type.lower() == "illegal":
            if getattr(error_root, 'type', None) is TokenType.EOF:
                self.errors.append((line_no, f"unexpected {error_root.type.name}"))
            elif getattr(error_root, 'type', None) in [TokenType.NUM, TokenType.ID]:
                self.errors.append((line_no, f"{error_type} {error_root.type.name}"))
            else:
                lex = getattr(error_root, 'lexeme', None)
                self.errors.append((line_no, f"{error_type} {lex}"))

    # ---------------- main parse ----------------
    def generate_parse_tree(self):
        self.stack = [self.root]
        token = self.get_next_valid_token()
        statement = None
        try:
            while len(self.stack):
                statement = self.get_next_valid_statement()
                statement.token = token

                # semantic actions (code-gen hooks)
                # if statement.name.startswith("#"):
                #     self.code_gen.call(statement.name, statement.token)
                #     self.remove_statement(statement)
                #     continue

                if self.grammar.is_terminal(statement.name):  # terminal
                    if statement.name != self.get_token_key(token):  # not matching
                        self.add_error(statement, "missing")
                        self.remove_statement(statement)
                    elif len(self.stack):
                        token = self.get_next_valid_token()
                else:  # non-terminal
                    key = (statement.name, self.get_token_key(token))
                    if key in self.p_table and self.p_table[key] != "synch":
                        self.update_stack(statement, key)
                    else:
                        token = self.panic(statement, key, token)
        except NoTokenLeftException:
            self.remove_statement(statement)
            [self.remove_statement(g) for g in list(self.stack)]

        return self.root

    def update_stack(self, statement, key):
        self.stack.extend([Node(g, parent=statement) for g in self.p_table[key]][::-1])

    def panic(self, statement, key, token):
        while key not in self.p_table:
            self.add_error(token, "illegal")
            token = self.get_next_valid_token()
            key = (statement.name, self.get_token_key(token))
        if self.p_table[key] != 'synch':
            self.update_stack(statement, key)
            return token

        self.add_error(statement, "missing")
        self.remove_statement(statement)
        return token

    # ------------- token handling --------------
    def get_next_valid_token(self):
        try:
            token = self.token_generator.get_next_token()
            # skip trivia / errors
            while token.type in [TokenType.COMMENT, TokenType.WHITE_SPACE, TokenType.ERROR]:
                token = self.token_generator.get_next_token()

            # snapshot for AST: (line, type_name, lexeme)
            line_no = self.token_generator.get_line_no()
            type_name = token.type.name
            lexeme = token.lexeme
            self._ast_tokens.append((line_no, type_name, lexeme))

            return token
        except Exception:
            # ensure EOF token is present for AST stage
            if self._ast_tokens:
                last_line = self._ast_tokens[-1][0]
            else:
                last_line = 0
            if not self._ast_tokens or self._ast_tokens[-1][1] != "EOF":
                self._ast_tokens.append((last_line, "EOF", "$"))
            raise NoTokenLeftException()

    def get_next_valid_statement(self):
        statement = self.stack.pop()
        while len(self.stack) and statement.name == "ε":
            statement = self.stack.pop()
        return statement

    @staticmethod
    def get_token_key(token):
        return (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]]

    @staticmethod
    def remove_statement(statement):
        if statement.parent:
            children = list(statement.parent.children)
            children.remove(statement)
            statement.parent.children = tuple(children)

    # ------------- exports (existing) -------------
    def export_syntax_error(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            if not self.errors:
                f.write("There is no syntax error.\n")
            for line_no, error in self.errors:
                f.write(f"#{line_no} : syntax error, {error}\n")

    def export_parse_tree(self, path):
        self.reformat_tree()
        with open(path, 'w', encoding='utf-8') as f:
            for pre, _, node in RenderTree(self.root):
                f.write("%s%s\n" % (pre, node.name))

    def export_code(self, path):
        self.code_gen.export(path)

    def reformat_tree(self):
        for node in PreOrderIter(self.root):
            if node.name == "ε":
                node.name = "epsilon"
            elif node.name != "$" and self.grammar.is_terminal(node.name):
                try:
                    index = node.token.type.name.find("_")
                    token_type = (node.token.type.name[:index], node.token.type.name)[index == -1]
                    node.name = f"({token_type}, {node.token.lexeme}) "
                except Exception:
                    pass

    # ------------- NEW: AST API -------------
    def build_ast(self):
        """
        Build an AST *after* LL(1) parsing by feeding a clean token stream
        (captured during parsing) into the RD AstParser that mirrors your code #2.
        Returns the AstParser instance (so you can inspect .ast_root / .syntax_errors).
        """
        # Ensure EOF sentinel exists
        if not self._ast_tokens or self._ast_tokens[-1][1] != "EOF":
            last_line = self._ast_tokens[-1][0] if self._ast_tokens else 0
            self._ast_tokens.append((last_line, "EOF", "$"))

        ast_parser = AstParser(self._ast_tokens)
        ast_parser.parse_program()
        return ast_parser

    def export_ast(self, output_dir):
        """Convenience: build AST and dump ast.json + syntax_errors.txt (like code #2)."""
        ast_parser = self.build_ast()
        ast_parser.write_outputs(output_dir)
        return ast_parser
