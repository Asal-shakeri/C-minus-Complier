# Code Generation Documentation
## C-Minus Compiler - Phase 3

### Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Code Generation Process](#code-generation-process)
5. [Instruction Set](#instruction-set)
6. [Memory Management](#memory-management)
7. [Scope Management](#scope-management)
8. [Function Handling](#function-handling)
9. [Control Flow](#control-flow)
10. [API Reference](#api-reference)
11. [Usage Examples](#usage-examples)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The Code Generation module is the final phase of the C-Minus compiler that translates the parse tree into executable assembly-like code. It implements a stack-based virtual machine architecture with support for variables, functions, control structures, and scope management.

### Key Features
- **Stack-based architecture**: Uses a semantic stack for expression evaluation
- **Memory management**: Automatic allocation and deallocation of variables
- **Scope handling**: Nested scope support with proper cleanup
- **Function calls**: Complete function call/return mechanism
- **Control flow**: Support for if-else, while loops, and switch statements
- **Register management**: Virtual register file for optimization

---

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

---

## Core Components

### 1. CodeGen Class (`code_gen.py`)
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

### 2. RegisterFile Class (`register.py`)
Manages the virtual register file for the target machine.

**Registers:**
- `sp`: Stack Pointer (points to top of stack)
- `fp`: Frame Pointer (points to current function frame)
- `ra`: Return Address (stores return address for function calls)
- `rv`: Return Value (stores function return values)

### 3. Assembler Class (`assembler.py`)
Handles assembly code generation and memory management.

**Key Attributes:**
- `program_block`: List of generated instructions
- `data_address`: Current data segment address
- `temp_address`: Current temporary variable address
- `stack_address`: Stack segment base address
- `arg_pointer`: Function argument management

### 4. ScopeManager Class (`scope.py`)
Manages nested scopes and variable lifetime.

**Scope Types:**
- `f`: Function scope
- `c`: Container scope (blocks)
- `s`: Simple scope
- `t`: Temporary scope

### 5. StackManager Class (`stack.py`)
Handles stack operations and memory allocation.

**Key Operations:**
- `push()`: Push value onto stack
- `pop()`: Pop value from stack
- `new_scope()`: Create new function scope
- `del_scope()`: Clean up function scope
- `reserve()`: Allocate stack space

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

## Conclusion

The Code Generation module provides a robust foundation for translating C-Minus programs into executable code. Its modular architecture, comprehensive scope management, and efficient memory handling make it suitable for educational purposes and can serve as a base for more advanced compiler implementations.

The system successfully handles the complexity of modern programming language features while maintaining simplicity and clarity in the generated code. 