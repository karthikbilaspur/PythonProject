import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from random import randint
from typing import Any, Callable, Literal

# ============================================================
# 1. FIBONACCI - Matrix Exponentiation
# ============================================================

def _multiply(F: list[list[int]], M: list[list[int]]) -> None:
    x = F[0][0] * M[0][0] + F[0][1] * M[1][0]
    y = F[0][0] * M[0][1] + F[0][1] * M[1][1]
    z = F[1][0] * M[0][0] + F[1][1] * M[1][0]
    w = F[1][0] * M[0][1] + F[1][1] * M[1][1]
    F[0][0], F[0][1], F[1][0], F[1][1] = x, y, z, w

def _power(F: list[list[int]], n: int) -> None:
    if n == 0 or n == 1:
        return
    M = [[1, 1], [1, 0]]
    _power(F, n // 2)
    _multiply(F, F)
    if n % 2 != 0:
        _multiply(F, M)

def fib(n: int) -> int:
    """nth Fibonacci number using matrix exponentiation - O(log n)"""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    F = [[1, 1], [1, 0]]
    _power(F, n - 1)
    return F[0][0]

def fibonacci_sequence(n: int) -> list[int]:
    return [fib(i) for i in range(n)]

def fibonacci_fast_sequence(n: int) -> list[int]:
    """Faster iterative version for generating first n numbers."""
    seq: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

def run_fibonacci_cli():
    print("\n--- Fibonacci (Matrix Exponentiation) ---")
    try:
        n = int(input("How many terms? (e.g. 10): "))
        print("Sequence:", fibonacci_sequence(n))
        print(f"fib({n-1}) = {fib(n-1) if n>0 else 0}")
    except ValueError as e:
        print("Invalid input:", e)
    input("\nPress Enter to return...")

# ============================================================
# 2. NUMBER SYSTEM CONVERTER
# ============================================================

def decimal_to_binary(n: int) -> str: return bin(n)[2:]
def decimal_to_octal(n: int) -> str: return oct(n)[2:]
def decimal_to_hexadecimal(n: int) -> str: return hex(n)[2:]
def binary_to_decimal(n: str) -> int: return int(n, 2)
def octal_to_decimal(n: str) -> int: return int(n, 8)
def hexadecimal_to_decimal(n: str) -> int: return int(n, 16)
def binary_to_octal(n: str) -> str: return decimal_to_octal(binary_to_decimal(n))
def binary_to_hexadecimal(n: str) -> str: return decimal_to_hexadecimal(binary_to_decimal(n))
def octal_to_binary(n: str) -> str: return decimal_to_binary(octal_to_decimal(n))
def octal_to_hexadecimal(n: str) -> str: return decimal_to_hexadecimal(octal_to_decimal(n))
def hexadecimal_to_binary(n: str) -> str: return decimal_to_binary(hexadecimal_to_decimal(n))
def hexadecimal_to_octal(n: str) -> str: return decimal_to_octal(hexadecimal_to_decimal(n))

CONVERTER_OPTIONS: list[tuple[str, Callable[[str], int | str]]] = [
    ("Decimal to Binary", lambda num: decimal_to_binary(int(num))),
    ("Decimal to Octal", lambda num: decimal_to_octal(int(num))),
    ("Decimal to Hexadecimal", lambda num: decimal_to_hexadecimal(int(num))),
    ("Binary to Decimal", lambda num: binary_to_decimal(num)),
    ("Octal to Decimal", lambda num: octal_to_decimal(num)),
    ("Hexadecimal to Decimal", lambda num: hexadecimal_to_decimal(num)),
    ("Binary to Octal", lambda num: binary_to_octal(num)),
    ("Binary to Hexadecimal", lambda num: binary_to_hexadecimal(num)),
    ("Octal to Binary", lambda num: octal_to_binary(num)),
    ("Octal to Hexadecimal", lambda num: octal_to_hexadecimal(num)),
    ("Hexadecimal to Binary", lambda num: hexadecimal_to_binary(num)),
    ("Hexadecimal to Octal", lambda num: hexadecimal_to_octal(num)),
]

def run_converter_cli():
    while True:
        print("\n--- Number Conversion Menu ---")
        for i, (name, _) in enumerate(CONVERTER_OPTIONS, 1):
            print(f"{i}. {name}")
        print("13. Back to Main Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "13":
            return
        if not choice.isdigit() or not (1 <= int(choice) <= 12):
            print("Invalid choice. Try again.")
            continue
        num = input("Enter the number: ").strip()
        try:
            name, func = CONVERTER_OPTIONS[int(choice)-1]
            print(f"Result ({name}): {func(num)}")
        except Exception as e:
            print(f"Error: {e} - Check the number format for that base.")

# ============================================================
# 3. NUMBER GUESSING GAME (Tkinter)
# ============================================================

class NumberGuessingGame:
    def __init__(self, parent: tk.Misc | None = None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Number Guessing Game")
        self.window.geometry("350x220")
        self.window.resizable(False, False)
        self.number_to_guess = randint(1, 100)
        self.guesses = 0
        tk.Label(self.window, text="Guess a number between 1 and 100", font=("Arial", 11, "bold")).pack(pady=10)
        self.entry = tk.Entry(self.window, font=("Arial", 12), justify="center")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda _event: self.guess_number())
        self.result_label = tk.Label(self.window, text="", font=("Arial", 10))
        self.result_label.pack(pady=5)
        tk.Button(self.window, text="Guess", width=15, command=self.guess_number).pack(pady=3)
        tk.Button(self.window, text="Reset", width=15, command=self.reset_game).pack(pady=3)
        self.entry.focus()

    def guess_number(self):
        try:
            guess = int(self.entry.get())
            self.guesses += 1
            if guess < self.number_to_guess:
                self.result_label.config(text="Too low! Try again.", fg="blue")
            elif guess > self.number_to_guess:
                self.result_label.config(text="Too high! Try again.", fg="red")
            else:
                self.result_label.config(text=f"🎉 Correct in {self.guesses} guesses!", fg="green")
                self.guess_button_state('disabled')
        except ValueError:
            self.result_label.config(text="Invalid input. Enter a number.", fg="orange")

    def guess_button_state(self, state: Literal["normal", "active", "disabled"]) -> None:
        # Find Guess button - stored via children traversal
        for w in self.window.winfo_children():
            if isinstance(w, tk.Button) and w.cget("text") == "Guess":
                w.config(state=state)

    def reset_game(self):
        self.number_to_guess = randint(1, 100)
        self.guesses = 0
        self.result_label.config(text="")
        self.guess_button_state('normal')
        self.entry.delete(0, tk.END)
        self.entry.focus()

def run_guessing_game(parent: tk.Misc | None = None) -> None:
    NumberGuessingGame(parent)

# ============================================================
# 4. LICENSE PLATE DETECTOR (OpenCV)
# ============================================================

def detect_number_plate_image(image_path: str) -> str:
    """Detect plate from image file. Returns text or message."""
    try:
        import cv2
        import pytesseract  # type: ignore[reportMissingTypeStubs]
    except ImportError as e:
        return f"Missing dependency: {e}. Run: pip install opencv-python pytesseract"
    image = cv2.imread(image_path)
    if image is None:
        return "Could not load image."
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect = float(w) / h if h else 0
        if area > 1000 and 2 < aspect < 6:
            plate = image[y:y+h, x:x+w]
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            pytesseract_api: Any = pytesseract
            text = str(pytesseract_api.image_to_string(
                plate, lang='eng', config='--psm 11'
            )).strip()
            cv2.imshow('License Plate', plate)
            cv2.imshow('Detected', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return text or "(Plate found, but no text recognized)"
    return "License plate not detected"

def run_plate_webcam():
    try:
        import cv2
    except ImportError:
        messagebox.showerror("Missing Dependency", "Install opencv-python:\n pip install opencv-python")
        return
    cascade_path = os.path.join("res", "haarcascade_russian_plate_number.xml")
    if not os.path.exists(cascade_path):
        messagebox.showerror("Cascade Missing",
            f"File not found:\n{cascade_path}\n\nDownload it from OpenCV GitHub and place it in res/")
        return
    nPlateCascade = cv2.CascadeClassifier(cascade_path)
    cap = cv2.VideoCapture(0)
    cap.set(3, 640); cap.set(4, 480); cap.set(10, 150)
    count = 0
    print("Webcam started - Press 's' to save, 'q' to quit")
    while True:
        success, img = cap.read()
        if not success:
            break
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)
        imgRoi = None
        for (x, y, w, h) in plates:
            if w*h > 500:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
                cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                imgRoi = img[y:y+h, x:x+w]
                cv2.imshow("ROI", imgRoi)
        cv2.imshow("Result", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and imgRoi is not None:
            os.makedirs("res/scanned", exist_ok=True)
            cv2.imwrite(f'res/scanned/NoPlate_{count}.jpg', imgRoi)
            count += 1
            print(f"Saved NoPlate_{count-1}.jpg")
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def run_plate_detector_menu() -> None:
    choice = input("\n--- License Plate Detector ---\n1. Detect from Image File\n2. Live Webcam Detection\n3. Back\nChoice: ").strip()
    if choice == "1":
        path = input("Enter image path (e.g. image.jpg): ").strip() or "image.jpg"
        print("Result:", detect_number_plate_image(path))
    elif choice == "2":
        run_plate_webcam()
    input("\nPress Enter to return...")

# ============================================================
# 5. NUMBER TO WORDS CONVERTER (Tkinter + num2words)
# ============================================================

class NumberToWordsConverter:
    def __init__(self, parent: tk.Misc | None = None):
        try:
            import num2words  # type: ignore[reportMissingTypeStubs]
            self.num2words: Any = num2words
        except ImportError:
            messagebox.showerror("Missing Dependency", "Install num2words:\n pip install num2words")
            return
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Number to Words Converter")
        self.window.geometry("380x220")
        tk.Label(self.window, text="Enter a number:").pack(pady=5)
        self.entry = tk.Entry(self.window, width=25, font=("Arial", 11))
        self.entry.pack()
        # Language
        f1 = tk.Frame(self.window); f1.pack(pady=5)
        tk.Label(f1, text="Language:").pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value="en")
        tk.OptionMenu(f1, self.language_var, "en", "es", "fr", "de", "it").pack(side=tk.LEFT, padx=5)
        # Type
        f2 = tk.Frame(self.window); f2.pack(pady=5)
        tk.Label(f2, text="Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="cardinal")
        tk.OptionMenu(f2, self.type_var, "cardinal", "ordinal", "currency").pack(side=tk.LEFT, padx=5)
        tk.Button(self.window, text="Convert", width=15, command=self.convert_number).pack(pady=5)
        tk.Button(self.window, text="Clear", width=15, command=self.clear_fields).pack()
        self.result_label = tk.Label(self.window, text="", wraplength=340, font=("Arial", 10, "bold"))
        self.result_label.pack(pady=10)

    def convert_number(self):
        try:
            num = int(self.entry.get())
            lang = self.language_var.get()
            typ = self.type_var.get()
            if typ == "cardinal":
                words = self.num2words.num2words(num, lang=lang)
            elif typ == "ordinal":
                words = self.num2words.num2words(num, lang=lang, to="ordinal")
            else:
                words = self.num2words.num2words(num, lang=lang, to="currency")
            self.result_label.config(text=words)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")

# ============================================================
# MAIN LAUNCHER - Tkinter Hub + CLI fallback
# ============================================================

class MainHub:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("All-in-One Python Project")
        self.root.geometry("420x480")
        self.root.resizable(False, False)
        tk.Label(self.root, text="ALL-IN-ONE PYTHON PROJECT", font=("Arial", 14, "bold")).pack(pady=15)
        tk.Label(self.root, text="5 tools in one app", font=("Arial", 10), fg="gray").pack()
        buttons: list[tuple[str, Callable[[], None]]] = [
            ("1. Fibonacci Sequence", self.open_fib_gui),
            ("2. Number System Converter", self.open_converter_gui),
            ("3. Number Guessing Game", lambda: run_guessing_game(self.root)),
            ("4a. License Plate - From Image", self.open_plate_image),
            ("4b. License Plate - Live Webcam", run_plate_webcam),
            ("5. Number to Words Converter", self.open_number_words_converter),
        ]
        for text, cmd in buttons:
            tk.Button(self.root, text=text, width=35, height=2, command=cmd).pack(pady=5)
        tk.Label(self.root, text="Tip: Run 'python main.py --cli' for terminal mode", font=("Arial", 8), fg="gray").pack(pady=10)
        tk.Button(self.root, text="Exit", width=15, command=self.root.quit).pack()

    def open_fib_gui(self):
        win = tk.Toplevel(self.root)
        win.title("Fibonacci"); win.geometry("400x260")
        tk.Label(win, text="How many terms?").pack(pady=10)
        e = tk.Entry(win, font=("Arial", 12), justify="center"); e.pack()
        out = tk.Label(win, text="", wraplength=360, font=("Arial", 10)); out.pack(pady=10)
        def calc():
            try:
                n = int(e.get())
                out.config(text=", ".join(map(str, fibonacci_sequence(n))))
            except ValueError:
                out.config(text="Enter a valid number")
        tk.Button(win, text="Generate", command=calc).pack()

    def open_converter_gui(self):
        win = tk.Toplevel(self.root)
        win.title("Number Converter"); win.geometry("420x300")
        tk.Label(win, text="Enter number:").pack(pady=5)
        e = tk.Entry(win, font=("Arial", 12), justify="center"); e.pack()
        var = tk.StringVar(value=CONVERTER_OPTIONS[0][0])
        tk.OptionMenu(win, var, *[n for n,_ in CONVERTER_OPTIONS]).pack(pady=8)
        out = tk.Label(win, text="", font=("Arial", 11, "bold"), wraplength=380); out.pack(pady=10)
        def convert():
            try:
                name = var.get()
                func = dict(CONVERTER_OPTIONS)[name]
                out.config(text=f"{name}: {func(e.get().strip())}")
            except Exception as ex:
                out.config(text=f"Error: {ex}")
        tk.Button(win, text="Convert", command=convert).pack()

    def open_plate_image(self):
        path = filedialog.askopenfilename(title="Select Car Image", filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            result = detect_number_plate_image(path)
            messagebox.showinfo("Plate Result", str(result))

    def open_number_words_converter(self) -> None:
        NumberToWordsConverter(self.root)

    def run(self):
        self.root.mainloop()

def run_cli():
    while True:
        print("\n" + "="*45)
        print("  ALL-IN-ONE PYTHON PROJECT - CLI MODE")
        print("="*45)
        print("1. Fibonacci Sequence")
        print("2. Number System Converter")
        print("3. Number Guessing Game (GUI)")
        print("4. License Plate Detector")
        print("5. Number to Words Converter (GUI)")
        print("6. Launch GUI Hub")
        print("7. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1": run_fibonacci_cli()
        elif choice == "2": run_converter_cli()
        elif choice == "3": run_guessing_game(); 
        elif choice == "4": run_plate_detector_menu()
        elif choice == "5": NumberToWordsConverter()
        elif choice == "6": MainHub().run()
        elif choice == "7": print("Goodbye!"); break
        else: print("Invalid choice.")

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        try:
            MainHub().run()
        except tk.TclError:
            print("No display found - falling back to CLI mode")
            run_cli()
