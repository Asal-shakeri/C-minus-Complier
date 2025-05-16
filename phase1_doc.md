# Phase 1 Documentation

## Overview

This Python program(`test.py`) implements a lexical scanner (or lexer) that reads an input file containing source code and breaks it into a list of tokens. It also detects lexical errors and creates a symbol table for identifiers. The results are written to three output files:

* `tokens.txt`: contains the list of recognized tokens.
* `lexical_errors.txt`: contains any lexical errors found.
* `table.txt`: contains the symbol table with all keywords and identifiers.

---

## Class: `Scanner`

### `__init__(self, input_file)`

This is the constructor for the `Scanner` class. It:

* Reads the content of the input file.
* Initializes the position (`self.pos`), current line number (`self.lineno`), list of keywords, symbol table, a set to track seen identifiers, a list to store errors, and a list to store tokens.

---

### `get_next_token(self)`

This function returns the next token found in the input. It:

* Skips whitespace and tracks line numbers.
* Detects and processes comments.
* Recognizes numbers and validates them.
* Identifies keywords or user-defined identifiers.
* Recognizes symbols such as `+`, `-`, `*`, `==`, etc.
* Records invalid characters as lexical errors.

---

### `handle_comment(self)`

This function handles multi-line comments starting with `/*` and ending with `*/`. If a comment is not properly closed, it records an "Unclosed comment" error.

---

### `handle_num(self)`

This function reads sequences of digits and returns a `NUM` token. If a number is immediately followed by letters (e.g., `123abc`), it is marked as an invalid number and recorded as an error.

---

### `handle_id_or_keyword(self)`

This function reads sequences that start with a letter and may include letters or digits. If the sequence matches a keyword, it returns a `KEYWORD` token. Otherwise, it is treated as an identifier (`ID`) and added to the symbol table if not already present.

---

## Main Scanning Process

### `scan(self)`

This function repeatedly calls `get_next_token()` until the end of the file is reached. It then calls:

* `write_tokens()`: to save the tokens.
* `write_errors()`: to save lexical errors.
* `write_symbol_table()`: to save the symbol table.

---

## Output Methods

### `write_tokens(self)`

This function groups tokens by their line numbers and writes them to `tokens.txt` in the format:

```
line_number (TOKEN_TYPE, VALUE) (TOKEN_TYPE, VALUE) ...
```

---

### `write_errors(self)`

This function writes lexical errors to `lexical_errors.txt`, grouped by line number. If no errors are found, it writes:

```
There is no lexical error.
```

---

### `write_symbol_table(self)`

This function writes the symbol table to `table.txt`. It first writes the keywords, then the unique identifiers, each with a line number and lexeme.

---

## Entry Point

```python
if __name__ == '__main__':
    scanner = Scanner('input.txt')
    scanner.scan()
```

This block ensures that when the script is run directly, it creates a `Scanner` object using `input.txt` and starts the scanning process.

---
