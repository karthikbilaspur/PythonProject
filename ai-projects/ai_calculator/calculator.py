 
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportMissingParameterType=false, reportUnknownParameterType=false
# pyright: reportMissingTypeArgument=false, reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false, reportUnknownReturnType=false
# pyright: reportUnknownListItemType=false, reportUnknownArgumentType=false

import ast
import math
import operator
import re
import tkinter as tk
from tkinter import ttk

# --------------------------------------------------------------------------- #
# Safe expression evaluator
# --------------------------------------------------------------------------- #
BIN_OPS: dict[type[ast.operator], object] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
UNARY_OPS: dict[type[ast.operator], object] = {ast.UAdd: operator.pos, ast.USub: operator.neg}
CONSTANTS: dict[str, float] = {"pi": math.pi, "e": math.e}
MAX_EXPONENT = 1000  # stops things like 9**9**9 from freezing the app


def make_functions(angle_mode: str) -> dict[str, object]:
    """Whitelisted functions; trig respects the degrees/radians setting."""
    to_rad = math.radians if angle_mode == "deg" else (lambda x: x)
    return {
        "sin": lambda x: math.sin(to_rad(x)),
        "cos": lambda x: math.cos(to_rad(x)),
        "tan": lambda x: math.tan(to_rad(x)),
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "exp": math.exp,
        "abs": abs,
    }


def safe_eval(expr: str, angle_mode: str = "deg") -> float:
    """Evaluate a math expression without eval(). Raises ValueError if unsafe."""
    funcs = make_functions(angle_mode)
    expr = expr.replace("^", "**").replace("×", "*").replace("÷", "/")

    def ev(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            left, right = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
                raise ValueError("Exponent too large")
            op = BIN_OPS[type(node.op)]
            assert callable(op)
            return op(left, right)  # type: ignore[operator]  # pyright: ignore[reportUnknownMemberType]
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            op = UNARY_OPS[type(node.op)]
            assert callable(op)
            return op(ev(node.operand))  # type: ignore[operator]  # pyright: ignore[reportUnknownMemberType]
        if isinstance(node, ast.Name) and node.id in CONSTANTS:
            return CONSTANTS[node.id]
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in funcs
            and len(node.args) == 1
            and not node.keywords
        ):
            func = funcs[node.func.id]
            assert callable(func)
            return func(ev(node.args[0]))  # type: ignore[operator]  # pyright: ignore[reportUnknownMemberType]
        raise ValueError("Unsupported expression")

    return ev(ast.parse(expr.strip(), mode="eval"))
 
 
def fmt(value) -> str:
    """Nicely format a number (hides float noise like 1.2e-16)."""
    if isinstance(value, float):
        value = round(value, 12)
        if value.is_integer() and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"
    return str(value)
 
 
def friendly_error(exc: Exception) -> str:
    if isinstance(exc, ZeroDivisionError):
        return "Cannot divide by zero"
    if isinstance(exc, OverflowError):
        return "Number too large"
    if isinstance(exc, ValueError) and str(exc) and "math domain" not in str(exc):
        return str(exc)
    if isinstance(exc, ValueError):
        return "Math domain error"
    return "Invalid expression"
 
 
# --------------------------------------------------------------------------- #
# Calculator tabs (Basic + Scientific share one class, only the layout differs)
# --------------------------------------------------------------------------- #
BASIC_LAYOUT = [
    ["C", "Del", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]
 
SCI_LAYOUT = [
    ["sin", "cos", "tan", "log", "ln"],
    ["sqrt", "x²", "1/x", "eˣ", "^"],
    ["π", "e", "(", ")", "Del"],
    ["7", "8", "9", "/", "C"],
    ["4", "5", "6", "*", "%"],
    ["1", "2", "3", "-", "="],
    ["0", ".", "+"],
]
 
INSERT_TEXT = {
    "x²": "**2", "^": "**", "π": "pi", "eˣ": "exp(",
    "sin": "sin(", "cos": "cos(", "tan": "tan(",
    "log": "log(", "ln": "ln(", "sqrt": "sqrt(",
}
 
 
class CalculatorTab(ttk.Frame):
    def __init__(self, parent, app, layout):
        super().__init__(parent, padding=10)
        self.app = app
        self.var = tk.StringVar()
        self.error = tk.StringVar()
        cols = max(len(row) for row in layout)
 
        entry = ttk.Entry(self, textvariable=self.var, font=("Consolas", 18), justify="right")
        entry.grid(row=0, column=0, columnspan=cols, sticky="ew", pady=(0, 4))
        entry.bind("<Return>", lambda e: self.press("="))
        entry.bind("<Escape>", lambda e: self.press("C"))
 
        ttk.Label(self, textvariable=self.error, foreground="#d33").grid(
            row=1, column=0, columnspan=cols, sticky="w"
        )
 
        for r, row in enumerate(layout, start=2):
            for c, label in enumerate(row):
                ttk.Button(self, text=label, command=lambda l=label: self.press(l)).grid(
                    row=r, column=c, sticky="nsew", padx=2, pady=2, ipady=8
                )
        for c in range(cols):
            self.columnconfigure(c, weight=1)
 
    def press(self, key: str) -> None:
        self.error.set("")
        if key == "C":
            self.var.set("")
        elif key == "Del":
            self.var.set(self.var.get()[:-1])
        elif key == "=":
            self.calculate()
        elif key == "1/x":
            self.calculate("1/({})")
        else:
            self.var.set(self.var.get() + INSERT_TEXT.get(key, key))
 
    def calculate(self, template: str = "{}") -> None:
        expr = self.var.get().strip()
        if not expr:
            return
        try:
            result = fmt(safe_eval(template.format(expr), self.app.angle.get()))
        except Exception as exc:  # show a friendly message instead of crashing
            self.error.set(friendly_error(exc))
            return
        self.app.add_history(f"{expr} = {result}")
        self.var.set(result)
 
 
# --------------------------------------------------------------------------- #
# Unit converter (data-driven: add a unit by adding one dict entry)
# --------------------------------------------------------------------------- #
UNITS = {  # factors are relative to the base unit (meter / kilogram)
    "Length": {
        "Meter": 1, "Centimeter": 0.01, "Millimeter": 0.001, "Kilometer": 1000,
        "Inch": 0.0254, "Foot": 0.3048, "Mile": 1609.344,
    },
    "Weight": {
        "Kilogram": 1, "Gram": 0.001, "Pound": 0.45359237, "Ounce": 0.028349523125,
    },
    "Temperature": {"Celsius": None, "Fahrenheit": None, "Kelvin": None},
}
 
 
def convert_temperature(value: float, src: str, dst: str) -> float:
    celsius = {"Celsius": value, "Fahrenheit": (value - 32) * 5 / 9, "Kelvin": value - 273.15}[src]
    return {"Celsius": celsius, "Fahrenheit": celsius * 9 / 5 + 32, "Kelvin": celsius + 273.15}[dst]
 
 
class ConverterTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=15)
        self.app = app
        self.category = tk.StringVar(value="Length")
        self.src = tk.StringVar()
        self.dst = tk.StringVar()
        self.result = tk.StringVar()
 
        ttk.Label(self, text="Category").grid(row=0, column=0, sticky="w")
        cat_box = ttk.Combobox(self, textvariable=self.category, values=list(UNITS), state="readonly")
        cat_box.grid(row=0, column=1, columnspan=3, sticky="ew", pady=4)
        cat_box.bind("<<ComboboxSelected>>", lambda e: self.refresh_units())
 
        self.entry = ttk.Entry(self, font=("Consolas", 14))
        self.entry.grid(row=1, column=0, sticky="ew", pady=8)
        self.entry.bind("<Return>", lambda e: self.convert())
        self.src_box = ttk.Combobox(self, textvariable=self.src, state="readonly", width=12)
        self.src_box.grid(row=1, column=1, padx=4)
        ttk.Button(self, text="⇄", width=3, command=self.swap).grid(row=1, column=2)
        self.dst_box = ttk.Combobox(self, textvariable=self.dst, state="readonly", width=12)
        self.dst_box.grid(row=1, column=3, padx=4)
 
        ttk.Button(self, text="Convert", command=self.convert).grid(row=2, column=0, columnspan=4, pady=8)
        ttk.Label(self, textvariable=self.result, font=("Segoe UI", 12, "bold")).grid(
            row=3, column=0, columnspan=4
        )
        self.columnconfigure(0, weight=1)
        self.refresh_units()
 
    def refresh_units(self) -> None:
        names = list(UNITS[self.category.get()])
        self.src_box["values"] = self.dst_box["values"] = names
        self.src.set(names[0])
        self.dst.set(names[1])
        self.result.set("")
 
    def swap(self) -> None:
        a, b = self.src.get(), self.dst.get()
        self.src.set(b)
        self.dst.set(a)
 
    def convert(self) -> None:
        try:
            value = float(self.entry.get())
        except ValueError:
            self.result.set("Enter a valid number")
            return
        cat, src, dst = self.category.get(), self.src.get(), self.dst.get()
        if cat == "Temperature":
            out = convert_temperature(value, src, dst)
        else:
            out = value * UNITS[cat][src] / UNITS[cat][dst]
        text = f"{fmt(value)} {src} = {fmt(out)} {dst}"
        self.result.set(text)
        self.app.add_history(text)
 
 
# --------------------------------------------------------------------------- #
# Word-problem calculator: turns plain English into an expression
# --------------------------------------------------------------------------- #
NUM = r"(\d+(?:\.\d+)?)"
WORD_RULES = [
    (rf"square root of\s*{NUM}", r"sqrt(\1)"),
    (rf"{NUM}\s*(?:percent|%)\s*of\s*{NUM}", r"(\1/100*\2)"),
    (rf"{NUM}\s*squared", r"(\1**2)"),
    (r"to the power of|raised to", "**"),
    (r"multiplied by|times|\bx\b", "*"),
    (r"divided by|over", "/"),
    (r"plus", "+"),
    (r"minus|less", "-"),
    (r"modulo|\bmod\b", "%"),
]
FILLER = r"what is|what's|whats|how much is|calculate|compute|\?|="
 
 
def words_to_expression(text: str) -> str:
    text = re.sub(FILLER, " ", text.lower())
    for pattern, repl in WORD_RULES:
        text = re.sub(pattern, repl, text)
    return text.strip()
 
 
class AITab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=15)
        self.app = app
        self.result = tk.StringVar()
 
        ttk.Label(self, text="Ask a math question in plain English:").pack(anchor="w")
        self.entry = ttk.Entry(self, font=("Consolas", 14))
        self.entry.pack(fill="x", pady=8)
        self.entry.bind("<Return>", lambda e: self.ask())
        ttk.Button(self, text="Calculate", command=self.ask).pack()
        ttk.Label(self, textvariable=self.result, font=("Segoe UI", 12, "bold")).pack(pady=10)
        ttk.Label(
            self,
            text="Try: 5 plus 3 times 2  |  20 percent of 150  |  square root of 81  |  7 squared",
            wraplength=420,
        ).pack()
 
    def ask(self) -> None:
        question = self.entry.get().strip()
        if not question:
            return
        try:
            answer = fmt(safe_eval(words_to_expression(question), self.app.angle.get()))
        except Exception as exc:
            self.result.set(friendly_error(exc) if isinstance(exc, ZeroDivisionError)
                            else "Sorry, I couldn't understand that")
            return
        self.result.set(f"= {answer}")
        self.app.add_history(f"{question} = {answer}")
 
 
# --------------------------------------------------------------------------- #
# Main application window
# --------------------------------------------------------------------------- #
THEMES = {
    "light": {"bg": "#f3f3f3", "fg": "#111111", "field": "#ffffff", "btn": "#e1e1e1", "hover": "#cfd8e6"},
    "dark": {"bg": "#2b2b2b", "fg": "#f0f0f0", "field": "#3c3c3c", "btn": "#484848", "hover": "#5a6b85"},
}
 
 
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("520x680")
        self.root.minsize(460, 600)
 
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.theme = "light"
        self.angle = tk.StringVar(value="deg")
 
        # Top bar: angle mode + theme toggle
        bar = ttk.Frame(root, padding=(10, 8, 10, 0))
        bar.pack(fill="x")
        ttk.Label(bar, text="Angles:").pack(side="left")
        ttk.Radiobutton(bar, text="Degrees", variable=self.angle, value="deg").pack(side="left", padx=4)
        ttk.Radiobutton(bar, text="Radians", variable=self.angle, value="rad").pack(side="left")
        ttk.Button(bar, text="Light / Dark", command=self.toggle_theme).pack(side="right")
 
        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=8)
        self.notebook.add(CalculatorTab(self.notebook, self, BASIC_LAYOUT), text="Basic")
        self.notebook.add(CalculatorTab(self.notebook, self, SCI_LAYOUT), text="Scientific")
        self.notebook.add(ConverterTab(self.notebook, self), text="Converter")
        self.notebook.add(AITab(self.notebook, self), text="Word Problems")
 
        # History panel
        hist_frame = ttk.LabelFrame(root, text="History (double-click to copy result)", padding=5)
        hist_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.history = tk.Listbox(hist_frame, height=6, font=("Consolas", 10), relief="flat")
        scroll = ttk.Scrollbar(hist_frame, command=self.history.yview)
        self.history.configure(yscrollcommand=scroll.set)
        self.history.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")
        ttk.Button(hist_frame, text="Clear", command=lambda: self.history.delete(0, tk.END)).pack(
            side="left", padx=(6, 0), anchor="n"
        )
        self.history.bind("<Double-Button-1>", self.copy_result)
 
        self.apply_theme()
 
    def add_history(self, line: str) -> None:
        self.history.insert(0, line)
 
    def copy_result(self, _event=None) -> None:
        selection = self.history.curselection()
        if selection:
            result = self.history.get(selection[0]).rsplit("=", 1)[-1].strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
 
    def toggle_theme(self) -> None:
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
 
    def apply_theme(self) -> None:
        t = THEMES[self.theme]
        self.root.configure(bg=t["bg"])
        s = self.style
        s.configure(".", background=t["bg"], foreground=t["fg"])
        s.configure("TEntry", fieldbackground=t["field"], foreground=t["fg"])
        s.configure("TCombobox", fieldbackground=t["field"], foreground=t["fg"])
        s.configure("TButton", background=t["btn"], foreground=t["fg"])
        s.map("TButton", background=[("active", t["hover"])])
        s.configure("TNotebook.Tab", background=t["btn"], foreground=t["fg"], padding=(12, 6))
        s.configure("TLabelframe", background=t["bg"])
        s.configure("TLabelframe.Label", background=t["bg"], foreground=t["fg"])
        self.history.configure(bg=t["field"], fg=t["fg"])
 
 
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()