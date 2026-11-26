import tkinter as tk
from typing import Callable
import nltk  # type: ignore[reportMissingTypeStubs]
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # type: ignore[reportMissingTypeStubs]
def _ensure():
    try: nltk.data.find("sentiment/vader_lexicon.zip")  # type: ignore[reportUnknownMemberType]
    except LookupError: nltk.download("vader_lexicon", quiet=True)  # type: ignore[reportUnknownMemberType]
class SentimentAnalyzer:
    def __init__(self):
        _ensure(); self.sia=SentimentIntensityAnalyzer()
        self.root=tk.Tk(); self.root.title("Sentiment Analyzer"); self.root.configure(background="#dbeafe"); self.root.geometry("620x520")
        bg="#dbeafe"
        tk.Label(self.root,text="Enter Your Sentence:",bg=bg,font=("Helvetica",13,"bold")).pack(pady=10)
        self.text_area=tk.Text(self.root,height=7,width=65,font=("Helvetica",12)); self.text_area.pack(pady=5,padx=15)
        btns=tk.Frame(self.root,bg=bg); btns.pack(pady=10)
        actions: list[tuple[str, Callable[[], None]]] = [("Check Sentiment",self.detect_sentiment),("Clear",self.clear_all),("Exit",self.root.destroy)]
        for txt,cmd in actions:
            tk.Button(btns,text=txt,fg="black",bg="#fef9c3",command=cmd).pack(side=tk.LEFT,padx=8)
        self.result_frame=tk.Frame(self.root,bg=bg); self.result_frame.pack(pady=8); self.entries: dict[str, tk.Entry] = {}
        for key,label in [("positive","Positive:"),("neutral","Neutral:"),("negative","Negative:"),("overall","Overall:"),("compound","Compound score:")]:
            row=tk.Frame(self.result_frame,bg=bg); row.pack(fill="x",pady=3)
            tk.Label(row,text=label,bg=bg,width=18,anchor="w").pack(side=tk.LEFT)
            e=tk.Entry(row,width=30,font=("Helvetica",11)); e.pack(side=tk.LEFT); self.entries[key]=e
    def detect_sentiment(self):
        s_txt=self.text_area.get("1.0",tk.END).strip()
        if not s_txt: self.clear_all(); self.entries["overall"].insert(0,"Enter a sentence first."); return
        s=self.sia.polarity_scores(s_txt)  # type: ignore[reportUnknownMemberType]
        for key,code in [("positive","pos"),("neutral","neu"),("negative","neg")]:
            self.entries[key].delete(0,tk.END); self.entries[key].insert(0,f"{s[code]*100:.2f}%")
        self.entries["compound"].delete(0,tk.END); self.entries["compound"].insert(0,f"{s['compound']:.3f} (-1=very negative, +1=very positive)")
        overall="Positive" if s["compound"]>=0.05 else "Negative" if s["compound"]<=-0.05 else "Neutral"
        self.entries["overall"].delete(0,tk.END); self.entries["overall"].insert(0,overall)
    def clear_all(self):
        self.text_area.delete("1.0",tk.END)
        for e in self.entries.values(): e.delete(0,tk.END)
    def run(self): self.root.mainloop()
if __name__=="__main__": SentimentAnalyzer().run()
