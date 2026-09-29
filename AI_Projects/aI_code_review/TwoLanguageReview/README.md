# Code Review Tool — Python & Java

A lightweight, zero-dependency static analysis tool for quick code quality checks. Detects style violations, complexity issues, and common mistakes for Python and Java without needing external linters.

Features
Python Review
Syntax validation using ast.parse
Unused import detection (import os but never used)
Function length check — flags functions with > 10 statements in body
PEP 8 naming convention check — snake_case for variables
Java Review
Basic structure validation — ensures file starts with public class
Line length check — flags lines > 120 characters
Method length check — flags methods > 10 lines
Java naming convention check — camelCase / snake_case validation
Common
Unified API: review_code(code, language)
Extensible design — add new languages by adding a method
Returns list of human-readable issues
Installation
No external packages. Python 3.8+ only.

bash
git clone <your-repo-url>

cd code-review-tool
python --version  # 3.8+
Usage

1. Import as a library
python
from code_review import review_code

Python
python_code = """
import os
import sys
def my_function():
    x = 5
    y = x + 1
"""
review_code(python_code, 'python')

Issues found: Unused imports: os, sys

Java
java_code = """
public class MyClass {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
"""
review_code(java_code, 'java')
No issues found

2.Direct Class Usage
python
from code_review import CodeReview
reviewer = CodeReview(code_string, language='python')
issues = reviewer.review()
for issue in issues:
    print(issue)

3.Quick file check
python
def review_file(path, language):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    review_code(code, language)

review_file("example.py", "python")
review_file("MyClass.java", "java")

API Reference
CodeReview(code: str, language: str)
review() -> dispatches to correct reviewer
review_python() -> Python-specific checks
review_java() -> Java-specific checks
review_code(code: str, language: str)
Prints results: "Unsupported language", "No issues found", or "Issues found:" + list.

Example Output
Python:

Issues found:
Unused imports: os, sys
Variable 'MyVar' does not follow PEP 8 naming conventions
Function 'my_function' is too long (15 lines)
Java:

Issues found:
Line 12 is too long (135 characters)
Method starting at line 2 is too long (22 lines)
How It Works
Python: ast.parse() builds AST -> walks for Import/Name nodes -> set difference for unused imports -> checks FunctionDef body length.

Java: Regex-based line checks: public|private|protected detection for method start, brace counting for length, line length check.

Limitations
Python: No from X import Y support, no builtins allowlist, flat scope
Java: Regex not a true parser, only checks public class start, basic naming check
