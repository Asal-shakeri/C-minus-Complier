from anytree import Node, RenderTree, PreOrderIter



class NoTokenLeftException(Exception):
    pass


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

    def add_error(self, error_root, error_type):
        if error_type.lower() == "missing":
            self.errors.append((error_root[2], f"{error_type} {error_root.name}"))
        elif error_type.lower() == "illegal":
            token_type, token_value, line_no = error_root
            if token_type == 'EOF':
                self.errors.append((line_no, f"unexpected {token_type}"))
            elif token_type in ['NUM', 'ID']:
                self.errors.append((line_no, f"{error_type} {token_type}"))
            else:
                self.errors.append((line_no, f"{error_type} {token_value}"))

    def generate_parse_tree(self):
        self.stack = [self.root]
        token = self.get_next_valid_token()
        statement = None
        try:
            while len(self.stack):
                statement = self.get_next_valid_statement()
                statement.token = token

                # if statement.name == "#return":
                #     print("taskali")
                # code generation
                if statement.name.startswith("#"):
                    self.code_gen.call(statement.name, statement.token)
                    self.remove_statement(statement)
                    continue
                if self.grammar.is_terminal(statement.name):  # terminal
                    print(f"statement.name is {statement.name} but self.get_token_key(token) is {self.get_token_key(token)}")
                    if statement.name != self.get_token_key(token):  # not matching
                        self.add_error(statement, "missing")
                        self.remove_statement(statement)
                    elif len(self.stack):
                        token = self.get_next_valid_token()
                else:  # none_terminal
                    key = (statement.name, self.get_token_key(token))
                    if key in self.p_table and self.p_table[key] != "synch":
                        self.update_stack(statement, key)
                    else:
                        token = self.panic(statement, key, token)
        except NoTokenLeftException:
            self.remove_statement(statement)
            [self.remove_statement(g) for g in self.stack]

        return self.root

    def update_stack(self, statement, key):
        self.stack.extend([Node(g, parent=statement) for g in self.p_table[key]][::-1])

    def panic(self, statement, key, token):
        print("key is : ",key)
        print("self.p_table",self.p_table)
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

    def get_next_valid_token(self):
        try:
            token = self.token_generator.get_next_token()
            while token[0] in ['COMMENT', 'WHITE_SPACE', 'ERROR']:
                token = self.token_generator.get_next_token()
            return token
        except Exception:
            raise NoTokenLeftException()

    def get_next_valid_statement(self):
        statement = self.stack.pop()
        while len(self.stack) and statement.name == "ε":
            statement = self.stack.pop()
        return statement

    @staticmethod
    def get_token_key(token):
        token_type, token_value, _ = token
        if token_type in ['NUM', 'ID']:
            return token_type
        return token_value

    @staticmethod
    def remove_statement(statement):
        if statement.parent:
            children = list(statement.parent.children)
            children.remove(statement)
            statement.parent.children = tuple(children)

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
                except:
                    pass