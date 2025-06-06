import re

from grammar import init_grammar
from parser import LL1

class Scanner:
    def __init__(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            self.input = f.read()
        self.pos = 0
        self.lineno = 1
        self.keywords = {'if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return'}
        self.symbol_table = set(self.keywords)
        self.errors = []
        self.tokens = []

    def get_next_token(self):
        if self.pos >= len(self.input):
            return ('EOF', '', self.lineno)

        current_char = self.input[self.pos]

        # Skip whitespace
        if current_char in {' ', '\t', '\r', '\v', '\f'}:
            self.pos += 1
            return self.get_next_token()
        elif current_char == '\n':
            self.lineno += 1
            self.pos += 1
            return self.get_next_token()

        # Comments
        if self.input.startswith('/*', self.pos):
            return self.handle_comment()
        if self.input.startswith('*/', self.pos):
            self.errors.append((self.lineno, '*/', 'Unmatched comment'))
            self.pos += 2
            return self.get_next_token()

        # Invalid single '/'
        if current_char == '/':
            self.errors.append((self.lineno, '/', 'Invalid input'))
            self.pos += 1
            return self.get_next_token()

        # NUM
        if re.match(r'\d', current_char):
            return self.handle_num()

        # ID or KEYWORD
        if re.match(r'[a-zA-Z]', current_char):
            return self.handle_id_or_keyword()

        # Symbols
        symbols = {';', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==', '!='}
        for symbol in sorted(symbols, key=lambda x: -len(x)):
            if self.input.startswith(symbol, self.pos):
                self.pos += len(symbol)
                return ('SYMBOL', symbol, self.lineno)

        # Invalid character
        self.errors.append((self.lineno, current_char, 'Invalid input'))
        self.pos += 1
        return self.get_next_token()

    def handle_comment(self):
        start_line = self.lineno
        self.pos += 2  # Skip '/*'
        while self.pos < len(self.input):
            if self.input[self.pos] == '\n':
                self.lineno += 1
            if self.input.startswith('*/', self.pos):
                self.pos += 2
                return ('COMMENT', '/*...*/', start_line)
            self.pos += 1
        # If no closing */
        self.errors.append((start_line, '/*...', 'Unclosed comment'))
        return ('COMMENT', '/*...*/', start_line)

    def handle_num(self):
        start_pos = self.pos
        while self.pos < len(self.input) and re.match(r'\d', self.input[self.pos]):
            self.pos += 1
        # Invalid number like "23apple"
        if self.pos < len(self.input) and re.match(r'[a-zA-Z]', self.input[self.pos]):
            while self.pos < len(self.input) and re.match(r'[a-zA-Z0-9]', self.input[self.pos]):
                self.pos += 1
            lexeme = self.input[start_pos:self.pos]
            self.errors.append((self.lineno, lexeme, 'Invalid number'))
            return self.get_next_token()
        return ('NUM', self.input[start_pos:self.pos], self.lineno)

    def handle_id_or_keyword(self):
        start_pos = self.pos
        while self.pos < len(self.input) and re.match(r'[a-zA-Z0-9]', self.input[self.pos]):
            self.pos += 1
        lexeme = self.input[start_pos:self.pos]
        if lexeme in self.keywords:
            return ('KEYWORD', lexeme, self.lineno)
        else:
            if lexeme not in self.symbol_table:
                self.symbol_table.add(lexeme)
            return ('ID', lexeme, self.lineno)

    def scan(self):
        while True:
            token = self.get_next_token()
            if token[0] == 'EOF':
                break
            if token[0] != 'COMMENT':
                self.tokens.append(token)
        self.write_tokens()
        self.write_errors()
        self.write_symbol_table()

    def write_tokens(self):
        tokens_by_line = {}
        for token in self.tokens:
            lineno = token[2]
            if lineno not in tokens_by_line:
                tokens_by_line[lineno] = []
            tokens_by_line[lineno].append(f'({token[0]}, {token[1]})')
        with open('tokens.txt', 'w', encoding='utf-8') as f:
            for lineno in sorted(tokens_by_line.keys()):
                f.write(f'{lineno} {" ".join(tokens_by_line[lineno])}\n')

    def write_errors(self):
        if not self.errors:
            with open('lexical_errors.txt', 'w', encoding='utf-8') as f:
                f.write('There is no lexical error.')
        else:
            with open('lexical_errors.txt', 'w', encoding='utf-8') as f:
                errors_by_line = {}
                for lineno, lexeme, desc in self.errors:
                    if lineno not in errors_by_line:
                        errors_by_line[lineno] = []
                    errors_by_line[lineno].append(f'({lexeme}, {desc})')
                for lineno in sorted(errors_by_line.keys()):
                    f.write(f'{lineno} {" ".join(errors_by_line[lineno])}\n')

    def write_symbol_table(self):
        unique_lexemes = []
        seen = set()
        for lexeme in sorted(self.symbol_table, key=lambda x: (x not in self.keywords, x)):
            if lexeme not in seen:
                unique_lexemes.append(lexeme)
                seen.add(lexeme)

        with open('table.txt', 'w', encoding='utf-8') as f:
            f.write('lineno\tlexeme\n')
            for idx, lexeme in enumerate(unique_lexemes, 1):
                f.write(f'{idx}\t{lexeme}\n')

# Usage
if __name__ == "__main__":
    scanner = Scanner('input.txt')
    scanner.scan()
    parser=LL1(scanner,init_grammar(),None)
    parser.generate_parse_tree()

    parser.export_parse_tree('parse_tree.txt')
    parser.export_syntax_error('syntax_errors.txt')