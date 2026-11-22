import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

phonenumbers: Any = None
carrier: Any = None
geocoder: Any = None
phonenumberutil: Any = None
_has_phonenumbers = False

try:
    import phonenumbers as _phonenumbers
    from phonenumbers import carrier as _carrier
    from phonenumbers import geocoder as _geocoder
    from phonenumbers import phonenumberutil as _phonenumberutil

    phonenumbers = _phonenumbers
    carrier = _carrier
    geocoder = _geocoder
    phonenumberutil = _phonenumberutil
    _has_phonenumbers = True
except ImportError:
    pass

HAS_PHONENUMBERS = _has_phonenumbers

pyfiglet: Any = None
has_pyfiglet = False

try:
    import pyfiglet as _pyfiglet

    pyfiglet = _pyfiglet
    has_pyfiglet = True
except ImportError:
    pass


# -------------------- Tab 1: Validate --------------------
def validate_phone(raw: str) -> dict[str, str | bool]:
    """Validate + describe a phone number, offline. Raises ValueError on bad input."""
    if not HAS_PHONENUMBERS:
        raise RuntimeError("Missing dependency: pip install phonenumbers")
    raw = raw.strip()
    if not raw:
        raise ValueError("Please enter a phone number.")
    if len(raw) > 25:
        raise ValueError("Phone number looks too long (max 25 characters).")
    # Keep only digits, +, spaces, dashes, parentheses - reject letters etc.
    if any(c.isalpha() for c in raw):
        raise ValueError("Phone number should not contain letters.")

    try:
        # None = no default region: user must include +country code.
        # If they type a local number without +, try IN as a fallback
        # (change this to your own region if you prefer).
        try:
            num = phonenumbers.parse(raw, None)
        except phonenumberutil.NumberParseException:
            num = phonenumbers.parse(raw, "IN")
    except phonenumberutil.NumberParseException as e:
        raise ValueError(f"Could not parse number: {e}. Try with country code, e.g. +919876543210.") from None

    is_possible = phonenumbers.is_possible_number(num)
    is_valid = phonenumbers.is_valid_number(num)
    region = phonenumbers.region_code_for_number(num) or "Unknown"
    return {
        "e164": phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164),
        "international": phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "national": phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL),
        "country_code": f"+{num.country_code}",
        "region": region,
        "region_name": geocoder.description_for_number(num, "en") or "Unknown",
        "carrier": carrier.name_for_number(num, "en") or "Unknown",
        "type": _number_type_name(num),
        "is_possible": is_possible,
        "is_valid": is_valid,
    }


def _number_type_name(num: Any) -> str:
    t = phonenumbers.number_type(num)
    names = {
        phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed line",
        phonenumbers.PhoneNumberType.MOBILE: "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "Shared cost",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal number",
        phonenumbers.PhoneNumberType.PAGER: "Pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    }
    return names.get(t, "Unknown")


class ValidateTab(ttk.Frame):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent, padding=12)
        ttk.Label(self, text="Enter Phone Number (with country code, e.g. +919876543210):").pack(anchor="w")
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(fill="x", pady=(4, 8))
        self.entry.bind("<Return>", lambda _e: self.on_validate())
        ttk.Button(self, text="Validate", command=self.on_validate).pack(anchor="w")
        ttk.Label(self, text="This validates format / carrier / region. It does NOT track a live location.",
                  wraplength=420, foreground="gray").pack(anchor="w", pady=(6, 4))
        self.result = tk.Text(self, height=12, width=55)
        self.result.pack(fill="both", expand=True)

    def on_validate(self):
        self.result.delete("1.0", tk.END)
        try:
            info = validate_phone(self.entry.get())
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))
            return
        if not info["is_valid"]:
            msg = (
                f"Number: {info['international']}\n"
                f"Status: NOT a valid number"
                + (" (but possible format)" if info["is_possible"] else "")
                + "\nCheck the country code and digits."
            )
            self.result.insert(tk.END, msg)
            return
        lines = [
            f"Status: Valid ✓",
            f"E.164: {info['e164']}",
            f"International: {info['international']}",
            f"National: {info['national']}",
            f"Country code: {info['country_code']}  (Region: {info['region']})",
            f"Region (from prefix): {info['region_name']}",
            f"Carrier: {info['carrier']}",
            f"Type: {info['type']}",
        ]
        self.result.insert(tk.END, "\n".join(lines))


# -------------------- Tab 2: ASCII --------------------
def phone_to_ascii(text: str, font: str) -> str:
    if not has_pyfiglet:
        raise RuntimeError("Missing dependency: pip install pyfiglet")
    text = text.strip()
    if not text:
        raise ValueError("Please enter a phone number.")
    if len(text) > 20:
        raise ValueError("Keep it under 20 characters for ASCII art.")
    # Only allow characters that render sensibly in ASCII art.
    allowed = set("0123456789+ -()")
    if any(c not in allowed for c in text):
        raise ValueError("ASCII art only supports digits, +, spaces, dashes and parentheses.")
    try:
        return pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        return pyfiglet.figlet_format(text, font="standard")


class AsciiTab(ttk.Frame):
    # Fonts that exist in most pyfiglet installs. Verified at startup,
    # missing ones are dropped so selecting one can never crash.
    WANTED_FONTS = ["standard", "slant", "script", "digital", "bubble", "big", "mini"]

    def __init__(self, parent: tk.Misc):
        super().__init__(parent, padding=12)
        ttk.Label(self, text="Enter Phone Number:").pack(anchor="w")
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(fill="x", pady=(4, 8))
        self.entry.bind("<Return>", lambda _e: self.on_convert())

        available = [f for f in self.WANTED_FONTS if has_pyfiglet and f in pyfiglet.FigletFont.getFonts()]
        if not available:
            available = ["standard"]
        self.font_var = tk.StringVar(value=available[0])
        row = ttk.Frame(self)
        row.pack(fill="x", pady=(0, 8))
        ttk.Label(row, text="Font:").pack(side="left")
        ttk.OptionMenu(row, self.font_var, available[0], *available).pack(side="left", padx=6)
        ttk.Button(self, text="Convert to ASCII", command=self.on_convert).pack(anchor="w", pady=(0, 8))
        self.result = tk.Text(self, height=16, width=60, font=("Consolas", 10))
        self.result.pack(fill="both", expand=True)

    def on_convert(self):
        self.result.delete("1.0", tk.END)
        try:
            art = phone_to_ascii(self.entry.get(), self.font_var.get())
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))
            return
        self.result.insert(tk.END, art)


# -------------------- Main window --------------------
class PhoneTools:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Phone Tools - Validator + ASCII Art")
        self.window.geometry("500x560")
        if not HAS_PHONENUMBERS:
            messagebox.showwarning("Missing dependency",
                "phonenumbers is not installed.\nRun: pip install phonenumbers pyfiglet")
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True)
        notebook.add(ValidateTab(notebook), text="Validate Number")
        notebook.add(AsciiTab(notebook), text="Phone to ASCII")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    PhoneTools().run()