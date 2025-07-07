import ast
import re

class CodeReview:
    def __init__(self, code, language):
        self.code = code
        self.language = language

    def review(self):
        if self.language == 'python':
            return self.review_python()
        elif self.language == 'java':
            return self.review_java()
        else:
            return "Unsupported language"

    def review_python(self):
        issues = []
        try:
            tree = ast.parse(self.code)
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
            return issues

        # Check for unused imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
        unused_imports = [import_ for import_ in imports if import_ not in used_names]
        if unused_imports:
            issues.append(f"Unused imports: {', '.join(unused_imports)}")

        # Check for function length
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 10:
                    issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines)")

        # Check for variable naming conventions
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if not re.match("^[a-z_][a-z0-9_]*$", node.id):
                    issues.append(f"Variable '{node.id}' does not follow PEP 8 naming conventions")

        return issues

    def review_java(self):
        issues = []
        lines = self.code.split('\n')

        # Check for syntax errors
        if not self.code.strip().startswith('public class'):
            issues.append("Java code should start with 'public class'")

        # Check for line length
        for i, line in enumerate(lines):
            if len(line) > 120:
                issues.append(f"Line {i+1} is too long ({len(line)} characters)")

        # Check for method length
        method_start = None
        method_lines = 0
        for i, line in enumerate(lines):
            if re.match(r'\s*(public|private|protected)\s+.*\(', line):
                method_start = i
                method_lines = 1
            elif method_start is not None and re.match(r'\s*\}', line):
                if method_lines > 10:
                    issues.append(f"Method starting at line {method_start+1} is too long ({method_lines} lines)")
                method_start = None
                method_lines = 0
            elif method_start is not None:
                method_lines += 1

        # Check for variable naming conventions
        for line in lines:
            match = re.search(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', line)
            if match:
                var_name = match.group(1)
                if not re.match("^[a-z_][a-zA-Z0-9_]*$", var_name):
                    issues.append(f"Variable '{var_name}' does not follow Java naming conventions")

        return issues


def review_code(code, language):
    review = CodeReview(code, language)
    issues = review.review()
    if isinstance(issues, str):
        print(issues)
    else:
        if issues:
            print("Issues found:")
            for issue in issues:
                print(issue)
        else:
            print("No issues found")


# Example usage
python_code = """
import os
import sys

def my_function():
    x = 5
    if x > 10:
        print("x is greater than 10")
    elif x == 5:
        print("x is equal to 5")
    else:
        print("x is less than 10")
    for i in range(10):
        print(i)
    while x > 0:
        print(x)
        x -= 1
"""

java_code = """
public class MyClass {
    public static void main(String[] args) {
        int x = 5;
        if (x > 10) {
            System.out.println("x is greater than 10");
        } else if (x == 5) {
            System.out.println("x is equal to 5");
        } else {
            System.out.println("x is less than 10");
        }
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }
        while (x > 0) {
            System.out.println(x);
            x--;
        }
    }
}
"""

review_code(python_code, 'python')
review_code(java_code, 'java')