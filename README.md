-----

# C-Minus Compiler

A Python-based compiler for the C-Minus language, built as a term project for the Compiler Design course at the Iran University of Science and Technology.

This compiler performs the first two major phases of compilation:

1.  **Lexical Analysis (Scanning):** Converts the C-Minus source code into a stream of tokens.
2.  **Syntax Analysis (Parsing):** Verifies the code against the language grammar and generates a parse tree.

-----

## Table of Contents

  - [Overview](https://www.google.com/search?q=%23overview)
  - [Features](https://www.google.com/search?q=%23features)
  - [Compiler Architecture](https://www.google.com/search?q=%23compiler-architecture)
      - [Scanner (Lexical Analyzer)](https://www.google.com/search?q=%23scanner-lexical-analyzer)
      - [Parser (Syntax Analyzer)](https://www.google.com/search?q=%23parser-syntax-analyzer)
  - [Supported C-Minus Subset](https://www.google.com/search?q=%23supported-c-minus-subset)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Project File Structure](https://www.google.com/search?q=%23project-file-structure)
  - [Acknowledgements](https://www.google.com/search?q=%23acknowledgements)

-----

## Overview

This project implements a classic two-phase compiler design. It takes a single C-Minus source file (`input.txt`) and processes it to produce several artifacts, including a list of tokens, a symbol table, a parse tree, and detailed error reports for both the lexical and syntax analysis phases.

The primary goal is to validate the syntactic correctness of the input code according to a predefined LL(1) grammar.

## Features

✨ **DFA-based Scanner:** A custom-built scanner uses a Deterministic Finite Automaton (DFA) to efficiently recognize tokens.
✨ **LL(1) Parser:** A table-driven LL(1) parser ensures syntactical correctness and handles error recovery using `synch` tokens.
✨ **Parse Tree Generation:** Automatically generates and visualizes the complete parse tree using the `anytree` library.
✨ **Detailed Error Reporting:** Produces separate, easy-to-read files for lexical errors (`lexical_errors.txt`) and syntax errors (`syntax_errors.txt`), including line numbers.
✨ **Symbol Table Management:** Creates and exports a symbol table (`symbol_table.txt`) containing all keywords and identifiers found in the source code.

## Compiler Architecture

### Scanner (Lexical Analyzer)

The scanner is implemented in the `scanner/` directory. It reads the source code from an input file character by character and groups them into meaningful lexemes.

  - It uses a DFA defined in `scanner/default_scanner.py` to recognize patterns for **Numbers**, **IDs/Keywords**, **Symbols**, and **Comments**.
  - Whitespace is recognized and discarded.
  - If an invalid pattern is found, it is reported as a lexical error.
  - Recognized lexemes are converted into tokens and passed to the parser.

### Parser (Syntax Analyzer)

The parser is an **LL(1) parser** implemented in `Parser/parser.py`.

  - It uses a parsing stack and a parse table to process the token stream from the scanner.
  - The grammar rules, along with the pre-computed `FIRST`, `FOLLOW`, and `PREDICT` sets, are loaded from the `Parser/data/` directory.
  - As rules are successfully matched, a **Parse Tree** is constructed, with non-terminals as internal nodes and terminals (tokens) as leaf nodes.
  - If a token does not match the expected input, the parser enters a panic mode for error recovery and reports a syntax error.

## Supported C-Minus Subset

The compiler supports the following language constructs based on `Parser/data/grammar.txt`:

  - **Data Types:** `int`, `void`
  - **Declarations:**
      - Variable declaration: `int c;`
      - Array declaration: `int a[100];`
  - **Function Declaration:**
      - A `void main(void)` function is required as the entry point.
  - **Comments:**
      - Multi-line comments: `/* this is a comment */`
  - **Statements:**
      - Assignment: `var = expression;`
      - `break;` statement.
  - **Expressions:**
      - **Operators:** `=`, `+`, `-`, `*`, `<`, `==`
      - **Operands:** `ID`, `NUM`, Array access `ID[expression]`

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

  - Python 3.6+
  - pip (Python package installer)

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/Asal-shakeri/C-minus-Complier.git
    cd C-minus-Complier
    ```

2.  **Create a `requirements.txt` file:**
    This project depends on the `anytree` library.

    ```
    anytree
    ```

3.  **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1.  **Prepare the Input:**
    Open the `input.txt` file and write or paste the C-Minus code you want to compile. For example:

    ```c
    /* sample 2 */

    void main(void){
        int a[100];
        int b[100];
        int c;

        c = a[21] * 2 - 1;
        b[12] = c + 2 - a[1];
    }
    ```

2.  **Run the Compiler:**
    Execute the main compiler script from the terminal.

    ```sh
    python compiler.py
    ```

3.  **Check the Output:**
    The compiler will generate (or overwrite) the following files in the root directory:

      - `tokens.txt`: A list of all tokens identified by the scanner, grouped by line number.
      - `lexical_errors.txt`: A report of all lexical errors. If none exist, it will state so.
      - `symbol_table.txt`: A list of all keywords and identifiers used in the program.
      - `parse_tree.txt`: A structured, indented representation of the complete parse tree.
      - `syntax_errors.txt`: A report of all syntax errors. If the code is valid, it will state that no errors were found.

## Project File Structure

```
.
├── C-minus-Complier/
│
├── compiler.py             # Main script to run the compiler
├── input.txt               # Input C-Minus source code
├── README.md               # This README file
│
├── scanner/                # Lexical Analyzer module
│   ├── scanner.py          # Core scanner class
│   ├── default_scanner.py  # DFA definitions for C-Minus
│   ├── actions.py          # Functions executed on token recognition
│   ├── tokens.py           # TokenType enumerations
│   └── ...
│
├── Parser/                 # Syntax Analyzer module
│   ├── parser.py           # LL(1) parser implementation
│   ├── grammar.py          # Grammar class to load rules
│   └── data/               # Grammar definition files
│       ├── grammar.txt     # The C-Minus grammar rules
│       ├── Firsts.txt      # The computed FIRST sets
│       ├── Follows.txt     # The computed FOLLOW sets
│       └── Predicts.csv    # The computed PREDICT sets
│
└── tables/                 # Symbol table and error table handling
    └── ...
```

## Acknowledgements

  - This project was created by Mohammad Yousefian, Roghaye atayee, Maryam Shakeri as a term project for the Compiler Design course.
  - The structure and logic are based on fundamental compiler construction principles.