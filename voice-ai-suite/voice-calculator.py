import os, tkinter as tk
from typing import Any
from tkinter import messagebox
try:
 import speech_recognition as sr  # type: ignore[reportMissingTypeStubs]
 import wolframalpha  # type: ignore[reportMissingTypeStubs]
except ImportError: sr=None; wolframalpha=None
HISTORY="maths_history.txt"
def calc_expr(q: str, token: str) -> str:
 if wolframalpha is None: raise RuntimeError("pip install wolframalpha")
 client: Any = wolframalpha.Client(token); res=client.query(q); ans=next(res.results).text
 open(HISTORY,"a",encoding="utf-8").write(f"Q: {q}\nA: {ans}\n---\n"); return ans
class VoiceCalculator:
 def __init__(self, parent: tk.Misc | None = None):
  self.window=tk.Toplevel(parent) if parent else tk.Tk(); self.window.title("Voice Calculator"); self.window.geometry("460x360")
  tk.Label(self.window,text="Voice Calculator",font=("Arial",14,"bold")).pack(pady=10)
  tk.Label(self.window,text="WolframAlpha API Token:").pack(); self.token_entry=tk.Entry(self.window,width=50); self.token_entry.pack()
  tk.Label(self.window,text="Or type expression (e.g. 7 + 8):").pack(pady=5); self.expr_entry=tk.Entry(self.window,width=50); self.expr_entry.pack()
  tk.Button(self.window,text="Calculate Typed",bg="#2196F3",fg="white",command=self.calc_typed).pack(pady=5)
  tk.Button(self.window,text="Speak & Calculate",bg="#4CAF50",fg="white",command=self.calc_voice).pack(pady=5)
  tk.Button(self.window,text="Show History",command=self.show_history).pack(pady=3)
  tk.Button(self.window,text="Clear History",command=self.clear_history).pack(pady=3)
  self.result=tk.Label(self.window,text="",wraplength=420,font=("Arial",11),fg="green"); self.result.pack(pady=10)
 def calc_typed(self):
  t=self.token_entry.get().strip(); q=self.expr_entry.get().strip()
  if not t or not q: messagebox.showwarning("Missing","Enter token and expression"); return
  try: self.result.config(text="Answer: "+calc_expr(q,t))
  except Exception as e: messagebox.showerror("Error",str(e))
 def calc_voice(self):
  t=self.token_entry.get().strip()
  if not t: messagebox.showwarning("Missing","Enter token first"); return
  if sr is None: messagebox.showerror("Missing","pip install SpeechRecognition pyaudio"); return
  r=sr.Recognizer()
  with sr.Microphone() as src:
   self.result.config(text="Listening..."); self.window.update(); r.adjust_for_ambient_noise(src,duration=0.5); audio=r.listen(src,timeout=10,phrase_time_limit=8)
  try:
   spoken: str = getattr(r, "recognize_google")(audio, language="en-IN"); q: str = spoken.lower().replace("calculate"," ").strip()
   self.expr_entry.delete(0,tk.END); self.expr_entry.insert(0,q); self.result.config(text=f"Heard: {q}\nAnswer: "+calc_expr(q,t))
  except Exception as e: messagebox.showerror("Error",str(e))
 def show_history(self):
  messagebox.showinfo("History", open(HISTORY,encoding="utf-8").read()[-2000:] if os.path.exists(HISTORY) else "No history yet")
 def clear_history(self):
  if os.path.exists(HISTORY): open(HISTORY,"w").close()
  self.result.config(text="History cleared")
 def run(self): self.window.mainloop()
def open_window(parent: tk.Misc | None = None) -> VoiceCalculator: return VoiceCalculator(parent)
if __name__=="__main__": VoiceCalculator().run()
