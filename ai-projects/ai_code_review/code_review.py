import ast
import builtins
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set
import re

# --- Core Models ---

@dataclass
class Config:
    max_func_length: int = 40
    max_complexity: int = 8
    max_args: int = 5
    max_line_length: int = 88
    require_docstring: bool = True
    require_type_hints: bool = False

@dataclass
class Issue:
    path: str
    line: int
    col: int
    code: str
    severity: str # ERROR, WARN, STYLE
    message: str
    fixable: bool = False

    def __str__(self):
        return f"{self.path}:{self.line}:{self.col} [{self.severity}/{self.code}] {self.message}"

# --- Constants ---
PEP8_FUNC_VAR = re.compile(r"^[a-z_][a-z0-9_]*$")
PEP8_CLASS = re.compile(r"^[A-Z][a-zA-Z0-9]+$")
BUILTINS = set(dir(builtins))
DANGEROUS_NODES = {
    'eval': 'Use of eval() is a security risk',
    'exec': 'Use of exec() is a security risk',
    'pickle': 'pickle can execute arbitrary code',
}

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.defs: Dict[str, ast.AST] = {}
        self.uses: Set[str] = set()

class AdvancedReviewer(ast.NodeVisitor):
    def __init__(self, path: str, config: Config):
        self.path = path
        self.config = config
        self.issues: List[Issue] = []
        self.scope = Scope()
        self.imports: Dict[str, ast.AST] = {}
        self.scopes_stack = [self.scope]

    def _current(self): return self.scopes_stack[-1]

    def _push(self):
        s = Scope(self._current())
        self.scopes_stack.append(s)

    def _pop(self): return self.scopes_stack.pop()

    def issue(self, node, code, severity, msg, fixable=False):
        self.issues.append(Issue(
            self.path, getattr(node, 'lineno', 1),
            getattr(node, 'col_offset', 0), code, severity, msg, fixable
        ))

    # -- Visits --

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split('.')[0]
            self.imports[name] = node
            self._current().defs[name] = node
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name == '*': continue
            name = alias.asname or alias.name
            self.imports[name] = node
            self._current().defs[name] = node
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not PEP8_FUNC_VAR.match(node.name):
            self.issue(node, "N02", "STYLE", f"Function '{node.name}' should be snake_case")

        # Metrics
        length = (node.end_lineno - node.lineno) if node.end_lineno else len(node.body)
        if length > self.config.max_func_length:
            self.issue(node, "C01", "WARN", f"Function '{node.name}' too long ({length} > {self.config.max_func_length})")

        if len(node.args.args) > self.config.max_args:
            self.issue(node, "C03", "WARN", f"Too many args in '{node.name}' ({len(node.args.args)})")

        comp = self._complexity(node)
        if comp > self.config.max_complexity:
            self.issue(node, "C02", "WARN", f"Function '{node.name}' too complex (complexity={comp})")

        if self.config.require_docstring and not ast.get_docstring(node):
            self.issue(node, "D01", "STYLE", f"Missing docstring in '{node.name}'")

        if self.config.require_type_hints:
            for arg in node.args.args:
                if arg.annotation is None and arg.arg!= 'self':
                    self.issue(arg, "T01", "STYLE", f"Missing type hint for arg '{arg.arg}' in '{node.name}'")

        self._current().defs[node.name] = node
        self._push()
        for arg in node.args.args:
            self._current().defs[arg.arg] = arg
            if not PEP8_FUNC_VAR.match(arg.arg):
                self.issue(arg, "N01", "STYLE", f"Argument '{arg.arg}' should be snake_case")
        self.generic_visit(node)
        self._pop()

    def visit_ClassDef(self, node):
        if not PEP8_CLASS.match(node.name):
            self.issue(node, "N03", "STYLE", f"Class '{node.name}' should be CapWords")
        if self.config.require_docstring and not ast.get_docstring(node):
            self.issue(node, "D02", "STYLE", f"Missing docstring in class '{node.name}'")
        self._current().defs[node.name] = node
        self._push()
        self.generic_visit(node)
        self._pop()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self._current().uses.add(node.id)
            # Security / builtin shadowing
            if node.id in DANGEROUS_NODES and not self._is_defined(node.id):
                self.issue(node, "S01", "ERROR", f"{DANGEROUS_NODES[node.id]}")
        else: # Store, Del
            self._current().defs[node.id] = node
            if isinstance(node.ctx, ast.Store) and not PEP8_FUNC_VAR.match(node.id):
                 if node.id not in BUILTINS and not node.id.isupper(): # allow CONSTANTS
                    self.issue(node, "N01", "STYLE", f"Variable '{node.id}' should be snake_case")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detect eval/exec even as attribute: pickle.loads
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ('loads', 'load') and isinstance(node.func.value, ast.Name):
                if node.func.value.id == 'pickle':
                    self.issue(node, "S02", "ERROR", "Unsafe pickle usage")
        self.generic_visit(node)

    def _is_defined(self, name):
        s = self._current()
        while s:
            if name in s.defs: return True
            s = s.parent
        return name in BUILTINS

    def _complexity(self, node):
        c = 1
        for n in ast.walk(node):
            if isinstance(n, (ast.If, ast.For, ast.While, ast.With, ast.ExceptHandler, ast.Assert)):
                c += 1
            if isinstance(n, ast.BoolOp):
                c += len(n.values) - 1
        return c

    def finalize(self):
        # Unused imports
        all_uses = set()
        for s in self.scopes_stack:
            all_uses.update(s.uses)
        # also collect from nested scopes that were popped - we need to track globally
        # Simple approach: walk again for uses
        for name, imp_node in self.imports.items():
            if name not in all_uses:
                # check file-level uses via ast
                if name not in getattr(self, '_all_used_names', set()):
                    self.issue(imp_node, "F01", "WARN", f"Unused import '{name}'", fixable=True)

    def collect_uses(self, tree):
        self._all_used_names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}

def review_file(code: str, path: str, config: Config = Config()) -> List[Issue]:
    try:
        tree = ast.parse(code, filename=path)
    except SyntaxError as e:
        return [Issue(path, e.lineno or 0, e.offset or 0, "E01", "ERROR", f"SyntaxError: {e}")]

    visitor = AdvancedReviewer(path, config)
    visitor.collect_uses(tree)
    visitor.visit(tree)
    visitor.finalize()
    return sorted(visitor.issues, key=lambda i: i.line)

def review_path(target: Path, config: Config = Config()) -> List[Issue]:
    all_issues = []
    files = [target] if target.is_file() else list(target.rglob("*.py"))
    for f in files:
        if "venv" in f.parts or ".git" in f.parts: continue
        try:
            code = f.read_text(encoding='utf-8')
            all_issues.extend(review_file(code, str(f), config))
        except Exception as e:
            all_issues.append(Issue(str(f), 0, 0, "E00", "ERROR", f"Could not read: {e}"))
    return all_issues

def auto_fix_unused_imports(code: str) -> str:
    """Removes unused import lines."""
    issues = review_file(code, "tmp.py")
    lines = code.splitlines()
    to_delete = {i.line for i in issues if i.code == "F01"}
    return "\n".join([l for idx, l in enumerate(lines, 1) if idx not in to_delete])

# --- CLI ---
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Upgraded Code Reviewer")
    parser.add_argument("path", nargs="?", default=".", help="File or folder to review")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Auto-fix unused imports (single file only)")
    args = parser.parse_args()

    p = Path(args.path)
    if args.fix and p.is_file():
        original = p.read_text()
        fixed = auto_fix_unused_imports(original)
        p.write_text(fixed)
        print(f"Fixed {p}")
    else:
        issues = review_path(p, Config())
        if args.json:
            print(json.dumps([i.__dict__ for i in issues], indent=2))
        else:
            if not issues:
                print("No issues found ✓")
            else:
                for iss in issues:
                    print(iss)
            sys.exit(1 if any(i.severity == "ERROR" for i in issues) else 0)