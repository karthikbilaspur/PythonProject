import ast
import re

class CodeReview(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.imports = set()
        self.used_names = set()
        self.defined_names = set()
        self.function_defs = {}
        self.class_defs = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.function_defs[node.name] = {
            'lineno': node.lineno,
            'end_lineno': node.end_lineno,
            'complexity': self.calculate_complexity(node)
        }
        if not re.match("^[a-z_][a-z0-9_]*$", node.name):
            print(f"Function name '{node.name}' in {self.filename} does not follow PEP 8 conventions")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.class_defs.add(node.name)
        if not re.match("^[A-Z][a-zA-Z0-9]*$", node.name):
            print(f"Class name '{node.name}' in {self.filename} does not follow PEP 8 conventions")
        self.generic_visit(node)

    def calculate_complexity(self, node):
        complexity = 0
        for sub_node in ast.walk(node):
            if isinstance(sub_node, (ast.If, ast.IfExp, ast.For, ast.While)):
                complexity += 1
        return complexity

    def report(self):
        unused_imports = self.imports - self.used_names
        undefined_variables = self.used_names - self.defined_names

        if unused_imports:
            print(f"Unused imports in {self.filename}: {', '.join(unused_imports)}")
        if undefined_variables:
            print(f"Undefined variables in {self.filename}: {', '.join(undefined_variables)}")

        for var in self.defined_names:
            if not re.match("^[a-z_][a-z0-9_]*$", var):
                print(f"Variable name '{var}' in {self.filename} does not follow PEP 8 conventions")

        for func_name, func_data in self.function_defs.items():
            func_length = func_data['end_lineno'] - func_data['lineno']
            if func_length > 10:
                print(f"Function '{func_name}' in {self.filename} is too long ({func_length} lines)")
            if func_data['complexity'] > 5:
                print(f"Function '{func_name}' in {self.filename} is too complex ({func_data['complexity']} conditional statements)")


def review_code(code, filename):
    try:
        tree = ast.parse(code)
        review = CodeReview(filename)
        review.visit(tree)
        review.report()
    except SyntaxError as e:
        print(f"Syntax error in {filename}: {e}")


# Example usage
code = """
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

class MyClass:
    pass

x = 5
y = x + z
"""
review_code(code, "example.py")