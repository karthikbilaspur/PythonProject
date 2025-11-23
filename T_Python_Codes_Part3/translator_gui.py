from tkinter import *
import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from tkinter import messagebox

class LanguageTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Language Translator')
        self.root.geometry('530x330')
        self.root.maxsize(530, 330)
        self.root.minsize(530, 330)

        self.translator = Translator()

        self.language_selected = tk.StringVar()
        self.choose_langauge = ttk.Combobox(self.root,
                                           width=20,
                                           textvariable=self.language_selected,
                                           state='readonly',
                                           font=('verdana', 10, 'bold'))

        self.choose_langauge['values'] = (
            'Afrikaans', 'Albanian', 'Arabic', 'Armenian', 'Azerbaijani',
            'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Bulgarian',
            'Catalan', 'Cebuano', 'Chichewa', 'Chinese', 'Corsican',
            'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto',
            'Estonian', 'Filipino', 'Finnish', 'French', 'Frisian', 'Galician',
            'Georgian', 'German', 'Greek', 'Gujarati', 'Haitian Creole',
            'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian',
            'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese',
            'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean',
            'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lithuanian',
            'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam',
            'Maltese', 'Maori', 'Marathi', 'Mongolian', 'Myanmar', 'Nepali',
            'Norwegian', 'Odia', 'Pashto', 'Persian', 'Polish', 'Portuguese',
            'Punjabi', 'Romanian', 'Russian', 'Samoan', 'Scots Gaelic',
            'Serbian', 'Sesotho', 'Shona', 'Sindhi', 'Sinhala', 'Slovak',
            'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili', 'Swedish',
            'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Turkish', 'Turkmen',
            'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh',
            'Xhosa', 'Yiddish', 'Yoruba', 'Zulu'
        )

        self.choose_langauge.place(x=290, y=70)
        self.choose_langauge.current(0)

        self.t1 = Text(self.root, width=30, height=10, borderwidth=5, relief=RIDGE)
        self.t1.place(x=10, y=100)

        self.t2 = Text(self.root, width=30, height=10, borderwidth=5, relief=RIDGE)
        self.t2.place(x=260, y=100)

        self.button = Button(self.root,
                             text="Translate",
                             relief=RIDGE,
                             borderwidth=3,
                             font=('verdana', 10, 'bold'),
                             cursor="hand2",
                             foreground='Green',
                             command=self.translate)
        self.button.place(x=150, y=280)

        self.clear_button = Button(self.root,
                                   text="Clear",
                                   relief=RIDGE,
                                   borderwidth=3,
                                   font=('verdana', 10, 'bold'),
                                   cursor="hand2",
                                   foreground='Red',
                                   command=self.clear)
        self.clear_button.place(x=280, y=280)

    def translate(self):
        language_1 = self.t1.get("1.0", "end-1c")
        cl = self.language_selected.get()

        if language_1 == '':
            messagebox.showerror('Language Translator', 'please fill the box')
        else:
            self.t2.delete(1.0, 'end')
            output = self.translator.translate(language_1, dest=cl)
            self.t2.insert('end', output.text)

    def clear(self):
        self.t1.delete(1.0, 'end')
        self.t2.delete(1.0, 'end')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    translator = LanguageTranslator()
    translator.run()