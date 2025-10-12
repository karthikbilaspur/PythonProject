import tkinter as tk
from tkinter import ttk
from google.cloud import translate_v2 as translate

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation App")

        self.lang_codes = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko"
        }

        self.src_lang = tk.StringVar()
        self.src_lang.set("English")

        self.dest_lang = tk.StringVar()
        self.dest_lang.set("Spanish")

        self.src_text = tk.Text(self.root, height=10, width=40)
        self.src_text.pack(padx=10, pady=10)

        self.dest_text = tk.Text(self.root, height=10, width=40)
        self.dest_text.pack(padx=10, pady=10)

        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate_text)
        self.translate_button.pack(pady=10)

        self.src_lang_label = tk.Label(self.root, text="Source Language:")
        self.src_lang_label.pack()
        self.src_lang_menu = ttk.Combobox(self.root, textvariable=self.src_lang)
        self.src_lang_menu["values"] = list(self.lang_codes.keys())
        self.src_lang_menu.pack()

        self.dest_lang_label = tk.Label(self.root, text="Destination Language:")
        self.dest_lang_label.pack()
        self.dest_lang_menu = ttk.Combobox(self.root, textvariable=self.dest_lang)
        self.dest_lang_menu["values"] = list(self.lang_codes.keys())
        self.dest_lang_menu.pack()

    def translate_text(self):
        try:
            translate_client = translate.Client()
            src_text = self.src_text.get("1.0", tk.END)
            src_lang = self.lang_codes[self.src_lang.get()]
            dest_lang = self.lang_codes[self.dest_lang.get()]
            result = translate_client.translate(src_text, target_language=dest_lang, source_language=src_lang)
            self.dest_text.delete("1.0", tk.END)
            self.dest_text.insert("1.0", result["translatedText"])
        except Exception as e:
            self.dest_text.delete("1.0", tk.END)
            self.dest_text.insert("1.0", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()