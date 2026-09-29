# A lightweight static analysis tool built with Python's ast module to automatically review Python code for common quality issues, style violations, and complexity problems

Features
Unused Import Detection - Flags imports that are never used
Undefined Variable Detection - Finds variables that are used but never defined
PEP 8 Naming Convention Checks
Functions & variables: snake_case
Classes: PascalCase
Complexity & Size Analysis
Flags functions longer than 10 lines
Calculates cyclomatic complexity (counts if, for, while, ternary)
Flags functions with complexity > 5
Syntax Error Handling - Gracefully reports SyntaxError with location

Installation
No external dependencies required. Uses only Python standard library.

bash
Clone or download
git clone <your-repo-url>
cd python-code-review

Requires Python 3.8+
python3 --version
Usage
As a module
python
from code_review import review_code

code = """
import os
import sys

def my_function():
    x = 5
    y = x + z  # z is undefined
"""

review_code(code, "example.py")
2. As a standalone script
Modify the code variable at the bottom of the file or adapt it to read from a file:

python
def review_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    review_code(code, filepath)

review_file("example.py")
Example Output
For the included example:

Unused imports in example.py: sys, os
Undefined variables in example.py: z
Function 'my_function' in example.py is too long (15 lines)
Function 'my_function' in example.py is too complex (6 conditional statements)
How It Works
The tool uses ast.NodeVisitor to traverse the Abstract Syntax Tree:

Visitor Method What It Does
visit_Import Collects all imported modules
visit_Name Tracks Load vs Store to find used/defined names
visit_FunctionDef Validates function naming, records length & complexity
visit_ClassDef Validates class naming
calculate_complexity Counts branching nodes (If, IfExp, For, While)
Report phase compares sets:

unused_imports = imports - used_names
undefined_variables = used_names - defined_names
Project Structure
.
├── code_review.py   # Main CodeReview class and review_code() function
├── README.md
└── examples/
    └── example.py
Limitations
Built-in functions (print, range) are currently flagged as undefined - needs a builtins allowlist
Import detection is module-level only (import os), doesn't handle from X import Y
Scope handling is flat - doesn't handle local vs global scope correctly
Complexity metric is simplified, not full McCabe complexity
Roadmap
 Support ImportFrom nodes
 Add builtins whitelist
 Proper scope tracking (function / class scope)
 CLI support: python code_review.py path/to/file.py
 Output as JSON / SARIF for CI integration
 Auto-fix suggestions
