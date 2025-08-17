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
  - [Code Generation and Semantic Analysis](https://www.google.com/search?q=%23code-generation-and-semantic-analysis-documentation)
      - [Overview](https://www.google.com/search?q=%23overview-1)
      - [Architecture](https://www.google.com/search?q=%23architecture)
      - [Core Components](https://www.google.com/search?q=%23core-components)
      - [Code Generation Process](https://www.google.com/search?q=%23code-generation-process)
      - [Instruction Set](https://www.google.com/search?q=%23instruction-set)
      - [Memory Management](https://www.google.com/search?q=%23memory-management)
      - [Scope Management](https://www.google.com/search?q=%23scope-management)
      - [Function Handling](https://www.google.com/search?q=%23function-handling)
      - [Control Flow](https://www.google.com/search?q=%23control-flow)
      - [API Reference](https://www.google.com/search?q=%23api-reference)
      - [Usage Examples](https://www.google.com/search?q=%23usage-examples)
      - [Integration with Parser](https://www.google.com/search?q=%23integration-with-parser)
      - [Memory Layout Details](https://www.google.com/search?q=%23memory-layout-details)
      - [Error Handling](https://www.google.com/search?q=%23error-handling)
      - [Performance Considerations](https://www.google.com/search?q=%23performance-considerations)
      - [Testing and Validation](https://www.google.com/search?q=%23testing-and-validation)
      - [Future Enhancements](https://www.google.com/search?q=%23future-enhancements)
      - [Semantic Analysis](https://www.google.com/search?q=%23semantic-analysis)
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

---

# Code Generation and Semantic Analysis Documentation

## Overview

The C-Minus compiler has been extended to include **Code Generation** (Phase 3) and **Semantic Analysis** capabilities. This phase translates the parse tree into executable assembly-like code and performs semantic validation.

### Key Features
- **Stack-based architecture**: Uses a semantic stack for expression evaluation
- **Memory management**: Automatic allocation and deallocation of variables
- **Scope handling**: Nested scope support with proper cleanup
- **Function calls**: Complete function call/return mechanism
- **Control flow**: Support for if-else, while loops, and switch statements
- **Register management**: Virtual register file for optimization

## Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Parse Tree    │───▶│   CodeGen       │───▶│   Assembly      │
│                 │    │   Engine        │    │   Output        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Symbol Table  │
                       │   Integration   │
                       └─────────────────┘
```

### Memory Layout
```
Memory Addresses:
├── 500-899:    Data segment (global variables)
├── 900-999:    Temporary variables
├── 1000+:      Stack segment (local variables, function calls)
└── Registers:  SP, FP, RA, RV (Stack Pointer, Frame Pointer, Return Address, Return Value)
```

## Core Components

### 1. CodeGen Class (`code_gen/code_gen.py`)
The main code generation engine that orchestrates the entire process.

**Key Responsibilities:**
- Semantic stack management
- Instruction generation
- Routine dispatching
- Memory allocation

**Core Attributes:**
- `semantic_stack`: Stack for expression evaluation
- `jail`: Break statement management
- `assembler`: Assembly code generator
- `rf`: Register file
- `stack`: Stack manager
- `scope`: Scope manager

### 2. RegisterFile Class (`code_gen/register.py`)
Manages the virtual register file for the target machine.

**Registers:**
- `sp`: Stack Pointer (points to top of stack)
- `fp`: Frame Pointer (points to current function frame)
- `ra`: Return Address (stores return address for function calls)
- `rv`: Return Value (stores function return values)

### 3. Assembler Class (`code_gen/assembler.py`)
Handles assembly code generation and memory management.

**Key Attributes:**
- `program_block`: List of generated instructions
- `data_address`: Current data segment address
- `temp_address`: Current temporary variable address
- `stack_address`: Stack segment base address
- `arg_pointer`: Function argument management

### 4. ScopeManager Class (`code_gen/scope.py`)
Manages nested scopes and variable lifetime.

**Scope Types:**
- `f`: Function scope
- `c`: Container scope (blocks)
- `s`: Simple scope
- `t`: Temporary scope

### 5. StackManager Class (`code_gen/stack.py`)
Handles stack operations and memory allocation.

**Key Operations:**
- `push()`: Push value onto stack
- `pop()`: Pop value from stack
- `new_scope()`: Create new function scope
- `del_scope()`: Clean up function scope
- `reserve()`: Allocate stack space

## Code Generation Process

### 1. Initialization
```python
code_gen = CodeGen()
```
- Sets up memory addresses (data: 500, temp: 900, stack: 1000)
- Initializes register file
- Applies template code (stack initialization)

### 2. Parse Tree Traversal
The parser calls code generation routines during parse tree traversal:
```python
code_gen.call(routine_name, token)
```

### 3. Instruction Generation
Each routine generates specific assembly instructions:
```python
# Example: Variable assignment
def assign(self, token=None):
    self.assembler.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, )")
```

### 4. Output Generation
```python
code_gen.export("output.txt")
```

## Instruction Set

The code generator produces a simple assembly-like language with the following instructions:

### Arithmetic Operations
- `(ADD, src1, src2, dest)`: Addition
- `(SUB, src1, src2, dest)`: Subtraction  
- `(MULT, src1, src2, dest)`: Multiplication

### Memory Operations
- `(ASSIGN, src, dest, )`: Assignment
- `(JP, address, , )`: Unconditional jump
- `(JPF, condition, address, )`: Conditional jump

### Comparison Operations
- `(LT, src1, src2, dest)`: Less than
- `(EQ, src1, src2, dest)`: Equality

### I/O Operations
- `(PRINT, value, , )`: Print value

### Memory Addressing
- `@{address}`: Indirect addressing
- `#{value}`: Immediate value

## Memory Management

### Variable Allocation
```python
def get_data_var(self, chunk_size=1):
    self.assembler.data_address += self.MLD.WORD_SIZE * chunk_size
    return self.assembler.data_address - self.MLD.WORD_SIZE * chunk_size

def get_temp_var(self):
    self.assembler.temp_address += self.MLD.WORD_SIZE
    return self.assembler.temp_address - self.MLD.WORD_SIZE
```

### Array Handling
```python
def parr(self, token=None):
    offset = self.semantic_stack.pop()
    temp = self.get_temp_var()
    self.assembler.program_block.append(f"(MULT, #{self.MLD.WORD_SIZE}, {offset}, {temp})")
    self.assembler.program_block.append(f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})")
    self.semantic_stack.append(f"@{temp}")
```

## Scope Management

### Scope Creation
```python
def scope_start(self, token=None):
    tables.get_symbol_table().new_scope()
    self.scope.new_scope()
```

### Scope Cleanup
```python
def scope_stop(self, token=None):
    tables.get_symbol_table().remove_scope()
    self.scope.del_scope()
```

### Break Statement Handling
```python
def prison(self, token=None):
    self.scope.prison()

def prison_break(self, token=None):
    self.scope.prison_break()
```

## Function Handling

### Function Declaration
```python
def declare_func(self, token=None):
    self.assembler.data_pointer = self.assembler.data_address
    self.assembler.temp_pointer = self.assembler.temp_address
    id_record = self.find_var(self.assembler.last_id.lexeme)
    id_record.address = len(self.assembler.program_block)
```

### Function Call
```python
def func_call(self, token=None):
    self.store()           # Save current state
    self.push_args()       # Push arguments
    # Set return address
    self.assembler.program_block.append(f"(ASSIGN, #{len(self.assembler.program_block) + 2}, {self.rf.ra}, )")
    # Jump to function
    self.assembler.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
    self.restore()         # Restore state
    self.collect()         # Get return value
```

### Function Return
```python
def func_return(self, token=None):
    self.assembler.program_block.append(f"(JP, @{self.rf.ra}, , )")
```

### State Management
```python
def store(self):
    # Store data variables
    for data in range(self.assembler.data_pointer, self.assembler.data_address, self.MLD.WORD_SIZE):
        self.stack.push(data)
    # Store temporary variables
    for temp in range(self.assembler.temp_pointer, self.assembler.temp_address, self.MLD.WORD_SIZE):
        self.stack.push(temp)
    # Store registers
    self.stack.store_registers()

def restore(self):
    # Restore registers
    self.stack.load_registers()
    # Restore temporary variables
    for temp in range(self.assembler.temp_address, self.assembler.temp_pointer, -self.MLD.WORD_SIZE):
        self.stack.pop(temp - self.MLD.WORD_SIZE)
    # Restore data variables
    for data in range(self.assembler.data_address, self.assembler.data_pointer, -self.MLD.WORD_SIZE):
        self.stack.pop(data - self.MLD.WORD_SIZE)
```

## Control Flow

### If-Else Statements
```python
def decide(self, token=None):
    address = self.semantic_stack.pop()
    self.assembler.program_block[address] = f"(JPF, {self.semantic_stack.pop()}, {len(self.assembler.program_block)}, )"
```

### While Loops
```python
def jump_while(self, token=None):
    head1 = self.semantic_stack.pop()
    head2 = self.semantic_stack.pop()
    self.assembler.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
    self.semantic_stack.append(head2)
    self.semantic_stack.append(head1)
```

### Switch Statements
```python
def case(self, token=None):
    result = self.get_temp_var()
    self.assembler.program_block.append(f"(EQ, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, {result})")
    self.semantic_stack.append(result)
```

## API Reference

### CodeGen Class Methods

#### Core Methods
- `call(routine, token)`: Execute a code generation routine
- `export(path)`: Export generated code to file
- `execute_from(func_name)`: Set entry point to main function

#### Expression Handling
- `pnum(token)`: Push number literal
- `pid(token)`: Push variable identifier
- `parr(token)`: Handle array access
- `op_push(token)`: Push operator
- `op_exec(token)`: Execute binary operation

#### Variable Management
- `declare_id(token)`: Declare identifier
- `declare_arr(token)`: Declare array
- `declare_func(token)`: Declare function
- `assign(token)`: Handle assignment

#### Control Flow
- `label(token)`: Create label
- `decide(token)`: Handle conditional jumps
- `jump_while(token)`: Handle while loop jumps
- `case(token)`: Handle switch case

#### Function Management
- `func_call(token)`: Handle function calls
- `func_return(token)`: Handle function returns
- `arg_pass(token)`: Handle argument passing

#### Scope Management
- `scope_start(token)`: Start new scope
- `scope_stop(token)`: End current scope
- `prison(token)`: Handle break statements
- `prison_break(token)`: Handle break statement resolution

## Usage Examples

### Basic Usage
```python
from code_gen import CodeGen

# Initialize code generator
code_gen = CodeGen()

# Generate code for a simple assignment
code_gen.call("#pnum", Token(TokenType.NUM, "5"))
code_gen.call("#pid", Token(TokenType.ID, "x"))
code_gen.call("#assign")

# Export generated code
code_gen.export("output.txt")
```

### Function Definition
```python
# Function declaration
code_gen.call("#declare_func", func_token)

# Function parameters
code_gen.call("#arg_init")
code_gen.call("#declare_id", param_token)
code_gen.call("#arg_finish")

# Function body
code_gen.call("#scmod_f")
code_gen.call("#sc_start")
# ... function body code ...
code_gen.call("#sc_stop")
```

### Control Structures
```python
# If statement
code_gen.call("#label")  # Create label for else part
# ... condition evaluation ...
code_gen.call("#decide") # Conditional jump

# While loop
code_gen.call("#label")  # Loop start
# ... condition evaluation ...
code_gen.call("#label")  # Loop end
code_gen.call("#jump_while")
```

## Integration with Parser

The code generator integrates with the parser through semantic actions:

```python
# In parser.py
class LL1:
    def __init__(self, token_generator, grammar, code_generator):
        self.code_gen = code_generator
    
    def generate_parse_tree(self):
        # During parsing, semantic actions call code generation routines
        self.code_gen.call(statement.name, statement.token)
```

### Semantic Action Mapping
The parser maps grammar rules to code generation routines:
- Variable declarations → `#declare_id`, `#declare_arr`
- Function calls → `#func_call`
- Control structures → `#decide`, `#jump_while`
- Expressions → `#op_exec`, `#pnum`, `#pid`

## Memory Layout Details

### Address Allocation
```
Data Segment (500-899):
├── Global variables
├── Function addresses
└── Static data

Temporary Segment (900-999):
├── Expression temporaries
├── Array calculations
└── Intermediate results

Stack Segment (1000+):
├── Local variables
├── Function parameters
├── Return addresses
└── Frame pointers
```

### Register Usage
- **SP (Stack Pointer)**: Points to top of stack
- **FP (Frame Pointer)**: Points to current function frame
- **RA (Return Address)**: Stores return address for function calls
- **RV (Return Value)**: Stores function return values

## Error Handling

### Common Issues
1. **Undefined variables**: Checked through symbol table lookup
2. **Scope violations**: Handled by scope manager
3. **Memory overflow**: Prevented by address bounds checking
4. **Type mismatches**: Handled during semantic analysis

### Debugging
```python
# Enable step-by-step debugging
# Uncomment in code_gen.py:
# self.export("output.txt")
```

## Performance Considerations

### Optimization Techniques
1. **Register allocation**: Efficient use of virtual registers
2. **Memory reuse**: Temporary variable recycling
3. **Scope optimization**: Minimal stack operations
4. **Instruction selection**: Optimal instruction sequences

### Memory Efficiency
- Temporary variables are reused when possible
- Stack space is allocated only when needed
- Scope cleanup frees unused memory immediately

## Testing and Validation

### Test Cases
The code generator can be tested with various C-Minus programs:
- Simple arithmetic expressions
- Variable declarations and assignments
- Function definitions and calls
- Control structures (if-else, while, switch)
- Array operations
- Nested scopes

### Output Validation
Generated code should:
- Be syntactically correct
- Maintain proper memory layout
- Handle all control flow correctly
- Preserve variable scope rules
- Execute function calls properly

## Future Enhancements

### Potential Improvements
1. **Code optimization**: Constant folding, dead code elimination
2. **Register allocation**: More sophisticated register assignment
3. **Instruction scheduling**: Better instruction ordering
4. **Target-specific optimizations**: Platform-specific code generation

### Extensibility
The modular design allows for:
- New instruction types
- Different target architectures
- Enhanced optimization passes
- Additional language features

## Semantic Analysis

### Overview
The semantic analysis phase works in conjunction with code generation to ensure semantic correctness of the C-Minus program. It performs type checking, scope validation, and semantic error detection.

### Key Features
- **Type checking**: Ensures type compatibility in expressions and assignments
- **Scope validation**: Verifies variable declarations and usage within proper scopes
- **Function validation**: Checks function declarations, calls, and return types
- **Array validation**: Ensures proper array access and bounds checking

### Integration with Code Generation
Semantic analysis is integrated into the code generation process:
- Symbol table integration for variable lookup
- Scope management for nested scopes
- Type checking during expression evaluation
- Error reporting for semantic violations

### Error Types Handled
1. **Undefined variables**: Variables used before declaration
2. **Type mismatches**: Incompatible types in expressions
3. **Scope violations**: Variables accessed outside their scope
4. **Function errors**: Incorrect function calls or return types
5. **Array errors**: Invalid array access or bounds

## Conclusion

The Code Generation and Semantic Analysis modules provide a robust foundation for translating C-Minus programs into executable code. The modular architecture, comprehensive scope management, and efficient memory handling make it suitable for educational purposes and can serve as a base for more advanced compiler implementations.

The system successfully handles the complexity of modern programming language features while maintaining simplicity and clarity in the generated code, making it an excellent tool for understanding compiler construction principles.