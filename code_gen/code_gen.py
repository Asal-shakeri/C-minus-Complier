import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# ---- AST & Deserialisation ---
# -----------------------------
class AstNode:
    def __init__(self, node_type: Optional[str] = None, value: Optional[str] = None, children: Optional[List['AstNode']] = None):
        self.NodeType: Optional[str] = node_type
        self.Value: Optional[str] = value
        self.Children: List[AstNode] = children or []

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> 'AstNode':
        node_type = d.get("NodeType")
        value = d.get("Value")
        raw_children = d.get("Children", []) or []
        children = [AstNode.from_dict(c) for c in raw_children]
        return AstNode(node_type, value, children)


# -----------------------------
# ------ Symbolic Plumbing -----
# -----------------------------
@dataclass
class SymbolInfo:
    Address: int
    Type: Optional[str] = None


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: Dict[str, SymbolInfo] = {}

    def add(self, name: str, address: int, typ: Optional[str]) -> bool:
        if name in self._symbols:
            return False
        self._symbols[name] = SymbolInfo(Address=address, Type=typ)
        return True

    def lookup(self, name: str) -> Optional[SymbolInfo]:
        return self._symbols.get(name)


# -----------------------------
# -------- TAC Entity ----------
# -----------------------------
@dataclass
class ThreeAddressCode:
    Line: int
    Operation: str
    Arg1: Optional[str] = None
    Arg2: Optional[str] = None
    Result: Optional[str] = None

    def __str__(self) -> str:
        a1 = self.Arg1 or ""
        a2 = self.Arg2 or ""
        res = self.Result or ""
        return f"{self.Line}\t({self.Operation}, {a1}, {a2}, {res})"


# -----------------------------
# ------- Code Generator -------
# -----------------------------
class CodeGen:
    def __init__(self, root: AstNode) -> None:
        self._root = root
        self._symtab = SymbolTable()
        self._code: List[ThreeAddressCode] = []
        # Memory model
        self._next_var_addr: int = 500
        self._next_tmp_addr: int = 1000

    # Public API
    def generate(self) -> List[ThreeAddressCode]:
        self._gen(self._root)
        return self._code

    # ------------- Core dispatcher -------------
    def _gen(self, node: Optional[AstNode]) -> Optional[str]:
        if node is None or node.NodeType is None:
            return None

        nt = node.NodeType

        # Structural
        if nt == "Program":
            for ch in node.Children:
                self._gen(ch)
            return None

        if nt == "FunDecl":
            # assume void main(void) is our entry point
            # children: [TypeSpecifier, ID, Params, CompoundStmt]
            body = self._find_child(node, "CompoundStmt")
            self._gen(body)
            return None

        if nt == "CompoundStmt":
            for ch in node.Children:
                self._gen(ch)
            return None

        # Declarations
        if nt in ("VarDecl", "ArrayDecl"):
            self._gen_decl(node)
            return None

        # Statements
        if nt == "Assign":
            self._gen_assign(node)
            return None

        if nt == "IfStmt":
            self._gen_if(node)
            return None

        if nt == "RepeatStmt":
            self._gen_repeat(node)
            return None

        if nt == "ReturnStmt":
            # not producing code in this simple model
            if node.Children:
                self._gen(node.Children[0])
            return None

        if nt == "Call":
            # specifically handle builtin output(x)
            callee = node.Children[0].Value if node.Children else None
            if callee == "output":
                self._gen_output(node)
            return None

        # Expressions (return address string)
        if nt == "AddOp" or nt == "MulOp" or nt == "RelOp" or nt == "SubOp":
            return self._gen_binary(node)

        if nt == "SimpleVar":
            # child[0] is ID
            name = node.Children[0].Value if node.Children else None
            if name is None:
                return None
            info = self._symtab.lookup(name)
            return str(info.Address) if info else None

        if nt == "ArrayVar":
            return self._gen_array_access(node)

        if nt == "NUM":
            return f"#{node.Value}"

        # Like ExpressionStmt: just evaluate child
        if node.Children:
            return self._gen(node.Children[0])

        return None

    # ------------- Helpers -------------
    def _find_child(self, node: AstNode, kind: str) -> Optional[AstNode]:
        for ch in node.Children:
            if ch.NodeType == kind:
                return ch
        return None

    def _alloc_var(self) -> int:
        addr = self._next_var_addr
        self._next_var_addr += 4
        return addr

    def _alloc_tmp(self) -> str:
        addr = self._next_tmp_addr
        self._next_tmp_addr += 4
        return str(addr)

    def _emit(self, op: str, a1: Optional[str] = None, a2: Optional[str] = None, res: Optional[str] = None) -> int:
        line = len(self._code)
        self._code.append(ThreeAddressCode(Line=line, Operation=op, Arg1=a1, Arg2=a2, Result=res))
        return line

    def _backpatch(self, line: int, target: str) -> None:
        instr = self._code[line]
        instr.Result = target

    # ------------- Decls -------------
    def _gen_decl(self, node: AstNode) -> None:
        # VarDecl: [TypeSpecifier, ID]
        # ArrayDecl: [TypeSpecifier, ID, NUM]
        typ = node.Children[0].Value if node.Children else None
        ident = node.Children[1].Value if len(node.Children) > 1 else None
        if ident is None:
            return
        addr = self._alloc_var()
        self._symtab.add(ident, addr, typ)
        # arrays ignored capacity-wise in this simple flat memory model

    # ------------- Assign -------------
    def _gen_assign(self, node: AstNode) -> None:
        # Assign: [Var, Expr]
        lhs_addr = self._gen(node.Children[0])
        rhs_addr = self._gen(node.Children[1])
        self._emit("ASSIGN", rhs_addr, None, lhs_addr)

    # ------------- Binary Ops -------------
    def _gen_binary(self, node: AstNode) -> Optional[str]:
        op = node.NodeType
        # Map to TAC mnemonics
        if op == "AddOp":
            tac_op = "ADD" if (node.Value == "+" or node.Value is None) else "SUB"
        elif op == "SubOp":
            tac_op = "SUB"
        elif op == "MulOp":
            tac_op = "MULT"
        elif op == "RelOp":
            if node.Value == "==":
                tac_op = "EQ"
            elif node.Value == "<":
                tac_op = "LT"
            elif node.Value == "<=":
                tac_op = "LE"
            else:
                tac_op = "REL"  # generic fallback
        else:
            tac_op = op

        left = self._gen(node.Children[0])
        right = self._gen(node.Children[1])
        tmp = self._alloc_tmp()
        self._emit(tac_op, left, right, tmp)
        return tmp

    # ------------- If / Repeat -------------
    def _gen_if(self, node: AstNode) -> None:
        # IfStmt: [cond, then, else?]
        cond = self._gen(node.Children[0])
        jpf_line = self._emit("JPF", cond, None, "PLACEHOLDER")
        # then
        self._gen(node.Children[1])
        if len(node.Children) > 2 and node.Children[2] is not None:
            jp_line = self._emit("JP", None, None, "PLACEHOLDER")
            else_start = len(self._code)
            self._backpatch(jpf_line, str(else_start))
            self._gen(node.Children[2])
            end_addr = len(self._code)
            self._backpatch(jp_line, str(end_addr))
        else:
            end_addr = len(self._code)
            self._backpatch(jpf_line, str(end_addr))

    def _gen_repeat(self, node: AstNode) -> None:
        # RepeatStmt: [body, condition]
        loop_start = len(self._code)
        self._gen(node.Children[0])
        cond = self._gen(node.Children[1])
        # jump if false back to start
        self._emit("JPF", cond, None, str(loop_start))

    # ------------- Arrays & Calls -------------
    def _gen_array_access(self, node: AstNode) -> Optional[str]:
        # ArrayVar: [ID, indexExpr]
        array_id = node.Children[0].Value if node.Children else None
        info = self._symtab.lookup(array_id) if array_id else None
        if not info:
            return None
        idx = self._gen(node.Children[1])
        offset = self._alloc_tmp()
        self._emit("MULT", idx, "#4", offset)
        final = self._alloc_tmp()
        self._emit("ADD", f"#{info.Address}", offset, final)
        return f"@{final}"

    def _gen_output(self, node: AstNode) -> None:
        # Call: [ID, Args]
        args = self._find_child(node, "Args")
        if args and args.Children:
            arg_addr = self._gen(args.Children[0])
            self._emit("PRINT", arg_addr, None, None)


# -----------------------------
# ------------- CLI -----------
# -----------------------------
class Helper:
    @staticmethod
    def deserialize_ast(file_path: str) -> Optional[AstNode]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not data:
                return None
            return AstNode.from_dict(data)
        except FileNotFoundError:
            return None


def _discover_outputs_dir() -> Optional[str]:
    # Heuristic similar to the C# sample: walk up a few parents and look for "Outputs"
    here = os.path.abspath(os.path.dirname(__file__))
    candidates = [here]
    # up to 6 parents, just in case your repo is nested like a Matryoshka doll
    cur = here
    for _ in range(6):
        cur = os.path.dirname(cur)
        candidates.append(cur)
    for base in candidates:
        out = os.path.join(base, "Outputs")
        if os.path.isdir(out):
            return out
    return None


