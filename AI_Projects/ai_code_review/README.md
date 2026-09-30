# A  lightweight, zero-dependency static analysis tool for Python. Catches style issues, complexity, security risks, and dead code — without needing flake8, pylint, or radon

Inspired by merging two naive AST reviewers into one production-ready linter.

Features
Correct Scope Tracking - No false positives for print, range, self, or function args
PEP 8 Naming - N01/N02/N03 for variables (snake_case), functions (snake_case), classes (CapWords)
Code Health
C01 Function too long (default: > 40 lines)
C02 Too complex (counts if/for/while/with/except/and/or)
C03 Too many arguments (default: > 5)
Dead Code
F01 Unused imports (with auto-fix)
Documentation & Types
D01/D02 Missing docstring in function/class
T01 Missing type hints
Security
S01 Dangerous eval() / exec() usage
S02 Unsafe pickle.loads()
CLI Ready - Scan single files or entire projects, JSON output, CI-friendly exit codes
Installation
No dependencies. Just Python 3.8+

bash
git clone <your-repo>
cd advanced-reviewer

Usage
1.As a module

python
from reviewer import review_file, Config

code = open("example.py").read()
issues = review_file(code, "example.py", Config(max_func_length=30))

for issue in issues:
    print(issue)

example.py:2:0 [WARN/F01] Unused import 'sys'

2.CLI
Scan a file:

bash
python reviewer.py example.py
Scan a whole project:

bash
python reviewer.py ./my_project
JSON output for CI:

bash
python reviewer.py ./src --json > report.json
Auto-fix unused imports (single file only):

bash
python reviewer.py example.py --fix
Exit code is 1 if any ERROR severity issue is found, 0 otherwise.

Configuration
Edit Config dataclass:

python
config = Config(
    max_func_length=40,      # max lines per function
    max_complexity=8,        # max cyclomatic complexity
    max_args=5,              # max function args
    max_line_length=88,      # (reserved for future line-length check)
    require_docstring=True,  # require docstrings
    require_type_hints=False # require type hints
)

Project Structure.
├── reviewer.py   # The main reviewer logic
├── README.md
└── examples/
    └── example.py
Roadmap
 Line length check (E501)
 Unused variable detection (F02)
 GitHub Action
 Pre-commit hook
License
MIT
