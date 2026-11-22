 

import base64
import getpass
import hashlib
import json
import math
import os
import re
import secrets
import string
import sys
from typing import Protocol, TypedDict, cast


class FernetCipher(Protocol):
    def encrypt(self, data: bytes) -> bytes: ...
    def decrypt(self, token: bytes | str, ttl: int | None = None) -> bytes: ...


COMMON_PASSWORDS = {
    "password", "password123", "password1", "123456", "12345678", "123456789",
    "qwerty", "abc123", "letmein", "admin", "welcome", "monkey", "dragon",
    "1234567890", "111111", "123123", "iloveyou", "football", "princess",
    "password123!", "passw0rd", "p@ssw0rd", "p@ssword123",
}


class PasswordStrength(TypedDict):
    label: str
    score: int
    entropy_bits: float
    suggestions: list[str]

def _has_sequence(pw: str) -> bool:
    lowered = pw.lower()
    for i in range(len(lowered) - 2):
        a, b, c = map(ord, lowered[i:i+3])
        if b == a + 1 and c == b + 1:  # abc, 123
            return True
        if b == a - 1 and c == b - 1:  # cba, 321
            return True
    return False

def check_password_strength(password: str) -> PasswordStrength:
    """Return {label, score 0-100, entropy_bits, suggestions}."""
    suggestions: list[str] = []
    if not password:
        return {"label": "Weak", "score": 0, "entropy_bits": 0.0,
                "suggestions": ["Password cannot be empty."]}

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    # FIX: any non-alphanumeric = special, not a hand-picked subset.
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    # Pool size -> entropy estimate
    pool = 0
    if has_lower: pool += 26
    if has_upper: pool += 26
    if has_digit: pool += 10
    if has_special: pool += 33  # printable punctuation
    entropy = length * math.log2(pool) if pool else 0.0

    score = 0
    # Length: graduated, not a single >=8 cliff.
    if length >= 16: score += 40
    elif length >= 12: score += 30
    elif length >= 8:  score += 15
    else: suggestions.append(f"Make it at least 12 characters (currently {length}).")
    # Variety
    for present, name in [(has_lower, "lowercase letter"),
                          (has_upper, "uppercase letter"),
                          (has_digit, "number"),
                          (has_special, "special character")]:
        if present: score += 10
        else: suggestions.append(f"Add at least one {name}.")

    # Penalties for guessable patterns (the part the old checker missed)
    lowered = password.lower()
    if lowered in COMMON_PASSWORDS or lowered.rstrip("!1") in COMMON_PASSWORDS:
        score = min(score, 10)
        suggestions.append("This is a very common password - pick something unique.")
    if re.search(r"(.)\\1{2,}", password):
        score -= 10
        suggestions.append("Avoid 3+ repeated characters (e.g. 'aaa').")
    if _has_sequence(password):
        score -= 10
        suggestions.append("Avoid sequences like 'abc' or '123'.")
    if re.search(r"(19|20)\\d\\d", password):
        suggestions.append("Avoid years / birth years - they are easy to guess.")

    score = max(0, min(100, score))
    if score >= 80: label = "Strong"
    elif score >= 50: label = "Medium"
    else: label = "Weak"
    return {"label": label, "score": score, "entropy_bits": round(entropy, 1),
            "suggestions": suggestions}

# Backwards-compatible wrapper (old code expected a plain string).
def check_password_strength_label(password: str) -> str:
    return check_password_strength(password)["label"]


SAFE_PUNCTUATION = "!@#$%^&*()-_=+[]{};:,.<>?"

def generate_password(length: int = 16, use_uppercase: bool = True,
                      use_numbers: bool = True, use_special_chars: bool = True,
                      use_lowercase: bool = True) -> str:
    if length < 8:
        raise ValueError("Password length must be at least 8.")
    if length > 128:
        raise ValueError("Password length must be at most 128.")
    pools: list[str] = []
    if use_lowercase: pools.append(string.ascii_lowercase)
    if use_uppercase: pools.append(string.ascii_uppercase)
    if use_numbers:   pools.append(string.digits)
    if use_special_chars: pools.append(SAFE_PUNCTUATION)
    if not pools:
        raise ValueError("Select at least one character type.")
    if length < len(pools):
        raise ValueError(f"Length {length} is too short for {len(pools)} character types.")

    rng = secrets.SystemRandom()
    # Guarantee >=1 char from each chosen pool, then fill, then shuffle.
    chars = [rng.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [rng.choice(all_chars) for _ in range(length - len(chars))]
    rng.shuffle(chars)
    return "".join(chars)

# Alias kept so old call sites still work.
def generate_custom_password(length: int = 16, use_uppercase: bool = True,
                             use_numbers: bool = True, use_special_chars: bool = True) -> str:
    return generate_password(length, use_uppercase, use_numbers, use_special_chars)



try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as Pbkdf2Hmac
    from cryptography.hazmat.primitives import hashes
    has_crypto = True
except ImportError:
    has_crypto = False
    Fernet = None
    InvalidToken = Exception
    Pbkdf2Hmac = None
    hashes = None

META_FILE = "vault_meta.json"
VAULT_FILE = "vault.enc"
KDF_ITERATIONS = 600_000  # OWASP recommendation for PBKDF2-HMAC-SHA256

class PasswordManager:
    def __init__(self):
        self.passwords: dict[str, str] = {}
        self._fernet: FernetCipher | None = None

    # -- key derivation --
    @staticmethod
    def _derive_key(master: str, salt: bytes) -> bytes:
        assert Pbkdf2Hmac is not None and hashes is not None
        kdf = Pbkdf2Hmac(algorithm=hashes.SHA256(), length=32,
                         salt=salt, iterations=KDF_ITERATIONS)
        return base64.urlsafe_b64encode(kdf.derive(master.encode()))

    @staticmethod
    def _write_private(path: str, data: bytes):
        with open(path, "wb") as f:
            f.write(data)
        try: os.chmod(path, 0o600)
        except OSError: pass

    # -- setup / login --
    def create_master_password(self) -> bool:
        if not has_crypto:
            print("ERROR: 'cryptography' is required. Run: pip install cryptography")
            return False
        assert Fernet is not None
        while True:
            pw = getpass.getpass("Create a master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            if pw != confirm:
                print("Passwords do not match. Please try again.")
                continue
            if check_password_strength(pw)["label"] == "Weak":
                print("That master password is weak. Choose a longer, mixed one.")
                continue
            salt = os.urandom(16)
            key = self._derive_key(pw, salt)
            # Verifier = encrypt a known string; login checks it decrypts.
            # Never store a hash of the master password alone.
            verifier = Fernet(key).encrypt(b"vault-verifier")
            self._write_private(META_FILE, json.dumps({
                "salt": base64.b64encode(salt).decode(),
                "verifier": verifier.decode(),
            }).encode())
            self._fernet = Fernet(key)
            self.passwords = {}
            self.save_passwords()
            print("Master password created successfully!")
            return True

    def login(self, max_attempts: int = 5) -> bool:
        if not has_crypto:
            print("ERROR: 'cryptography' is required. Run: pip install cryptography")
            return False
        assert Fernet is not None
        if not os.path.exists(META_FILE):
            print("No vault found. Please create one.")
            return False
        with open(META_FILE, "r") as f:
            meta = json.load(f)
        salt = base64.b64decode(meta["salt"])
        for attempt in range(1, max_attempts + 1):
            pw = getpass.getpass("Enter master password: ")
            key = self._derive_key(pw, salt)
            try:
                Fernet(key).decrypt(meta["verifier"].encode())
            except InvalidToken:
                print(f"Incorrect password. ({max_attempts - attempt} attempts left)")
                continue
            self._fernet = Fernet(key)
            print("Login successful!")
            return True
        print("Too many failed attempts.")
        return False

    # -- vault --
    def save_passwords(self):
        assert self._fernet is not None, "Not logged in."
        fernet = cast(FernetCipher, self._fernet)
        blob: bytes = fernet.encrypt(json.dumps(self.passwords).encode())
        self._write_private(VAULT_FILE, blob)

    def load_passwords(self):
        assert self._fernet is not None, "Not logged in."
        if not os.path.exists(VAULT_FILE):
            self.passwords = {}
            return
        with open(VAULT_FILE, "rb") as f:
            blob = f.read()
        try:
            self.passwords = json.loads(self._fernet.decrypt(blob).decode())
        except InvalidToken:
            print("ERROR: Vault is corrupted or was created with a different master password.")
            self.passwords = {}

    # -- entries --
    def add_password(self):
        service = input("Enter service name: ").strip()
        if not service:
            print("Service name cannot be empty."); return
        pw = getpass.getpass("Enter password (leave blank to generate one): ")
        if not pw:
            pw = generate_password(16)
            print(f"Generated password: {pw}")
        self.passwords[service] = pw
        self.save_passwords()
        print("Password added successfully!")

    def view_passwords(self):
        if not self.passwords:
            print("(vault is empty)"); return
        for service in sorted(self.passwords):
            print(f"{service}: {self.passwords[service]}")

    def get_password(self, service: str) -> str | None:
        return self.passwords.get(service)

    def delete_password(self):
        service = input("Enter service name: ").strip()
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
            print("Password deleted successfully!")
        else:
            print("Service not found.")


def _ask_yes_no(prompt: str) -> bool:
    return input(prompt + " (yes/no): ").strip().lower() in ("yes", "y")

def _ask_length(default: int = 16) -> int:
    raw = input(f"Enter password length (default={default}): ").strip()
    if not raw: return default
    try:
        length = int(raw)
    except ValueError:
        print("Invalid length, using default."); return default
    if length < 8 or length > 128:
        print("Length must be 8-128, using default."); return default
    return length

def run_manager_cli():
    mgr = PasswordManager()
    if not os.path.exists(META_FILE):
        if not mgr.create_master_password():
            return
    if not mgr.login():
        return
    mgr.load_passwords()
    while True:
        print("\n1. Add password  2. View passwords  3. Delete password  4. Quit")
        try: choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!"); break
        if choice == "1": mgr.add_password()
        elif choice == "2": mgr.view_passwords()
        elif choice == "3": mgr.delete_password()
        elif choice == "4": break
        else: print("Invalid choice. Please try again.")

def run_cli():
    while True:
        print("\nPassword Suite")
        print("1. Check password strength")
        print("2. Generate a random password")
        print("3. Generate a custom password")
        print("4. Password manager (encrypted vault)")
        print("5. Quit")
        try: choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!"); break
        if choice == "1":
            pw = getpass.getpass("Enter a password to check: ")
            result = check_password_strength(pw)
            print(f"Strength: {result['label']} ({result['score']}/100, ~{result['entropy_bits']} bits entropy)")
            for s in result["suggestions"]:
                print(f" - {s}")
        elif choice == "2":
            print(f"Generated password: {generate_password(_ask_length())}")
        elif choice == "3":
            length = _ask_length()
            pw = generate_password(length,
                use_uppercase=_ask_yes_no("Use uppercase letters?"),
                use_numbers=_ask_yes_no("Use numbers?"),
                use_special_chars=_ask_yes_no("Use special characters?"))
            print(f"Generated password: {pw}")
        elif choice == "4":
            run_manager_cli()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def run_gui():
    import tkinter as tk
    from tkinter import messagebox
    window = tk.Tk()
    window.title("Password Suite - Generator + Strength Checker")
    window.geometry("520x380")

    # --- Generator ---
    tk.Label(window, text="Password Length:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
    length_entry = tk.Entry(window, width=10); length_entry.insert(0, "16")
    length_entry.grid(row=0, column=1, sticky="w")
    vars_: dict[str, tk.BooleanVar] = {}
    for i, (label, default) in enumerate([
        ("Lowercase", True), ("Uppercase", True),
        ("Numbers", True), ("Special Characters", True)]):
        v = tk.BooleanVar(value=default); vars_[label] = v
        tk.Checkbutton(window, text=label, variable=v).grid(row=1+i, column=0, sticky="w", padx=8)
    out = tk.Label(window, text="", font=("Consolas", 11), wraplength=480, justify="left")
    out.grid(row=5, column=0, columnspan=2, padx=8, pady=8, sticky="w")

    def on_generate():
        try: length = int(length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid password length"); return
        try:
            pw = generate_password(length,
                use_lowercase=vars_["Lowercase"].get(),
                use_uppercase=vars_["Uppercase"].get(),
                use_numbers=vars_["Numbers"].get(),
                use_special_chars=vars_["Special Characters"].get())
        except ValueError as e:
            messagebox.showerror("Error", str(e)); return
        out.config(text=pw)
        strength_label.config(text="")

    def on_copy():
        if out.cget("text"):
            window.clipboard_clear(); window.clipboard_append(out.cget("text"))
            messagebox.showinfo("Copied", "Password copied to clipboard.")
    tk.Button(window, text="Generate Password", command=on_generate).grid(row=5, column=0, padx=8, pady=4, sticky="w")
    tk.Button(window, text="Copy", command=on_copy).grid(row=5, column=1, sticky="w")

    # --- Strength checker ---
    tk.Label(window, text="Check strength:").grid(row=6, column=0, sticky="w", padx=8, pady=(12, 2))
    check_entry = tk.Entry(window, width=40, show="*")
    check_entry.grid(row=7, column=0, columnspan=2, padx=8, sticky="w")
    strength_label = tk.Label(window, text="", wraplength=480, justify="left")
    strength_label.grid(row=8, column=0, columnspan=2, padx=8, sticky="w")
    def on_check():
        r = check_password_strength(check_entry.get())
        text = f"{r['label']} ({r['score']}/100, ~{r['entropy_bits']} bits)"
        if r["suggestions"]: text += "\n" + "\n".join(f"- {s}" for s in r["suggestions"])
        strength_label.config(text=text)
    tk.Button(window, text="Check Strength", command=on_check).grid(row=9, column=0, padx=8, pady=4, sticky="w")
    window.mainloop()

def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "cli"
    if mode == "gui": run_gui()
    elif mode == "manager": run_manager_cli()
    else: run_cli()

if __name__ == "__main__":
    main()
