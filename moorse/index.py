"""
Morse Code App — Enhanced
Features:
 - Full charset: A-Z, 0-9, punctuation, prosigns
 - Text <-> Morse, live conversion, copy / paste / export / clear
 - Sound (Windows winsound, fallback beep) + visual flash + timing bars
 - WPM slider + Farnsworth spacing + tone + volume (Windows)
 - Tap / Spacebar keyer: tap to input dots/dashes, decode live
 - Learn mode: interactive chart, filter, flashcard flip
 - Practice: letters / words / sentences, difficulty, streak, hints
 - Quiz: timed, 10 Qs, difficulty, review of mistakes
 - History + Stats saved to morse_stats.json (persistent)
 - Keyboard shortcuts
"""
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from typing import Any, TypedDict, cast
import random, time, threading, json, os

try:
    import winsound
    def _beep_winsound(freq: int, ms: int) -> None:
        winsound.Beep(freq, max(1, int(ms)))
    _beep = _beep_winsound
except ImportError:
    def _beep(freq: int, ms: int) -> None:
        _ = freq
        print("\a", end="", flush=True); time.sleep(ms/1000)

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-', ',':'--..--', '?':'..--..', "'":'.----.', '!':'-.-.--', '/':'-..-.', '(':'-.--.', ')':'-.--.-',
    '&':'.-...', ':':'---...', ';':'-.-.-.', '=':'-...-', '+':'.-.-.', '-':'-....-', '_':'..--.-',
    '"':'.-..-.', '$':'...-..-', '@':'.--.-.', ' ':'/',
}
# Prosigns (no space between letters in real use, shown as <...>)
PROSIGNS = {'<AA>':'.-.-','<AR>':'.-.-.','<AS>':'.-...','<BK>':'-...-.-','<BT>':'-...-','<CL>':'-.-..-..','<CQ>':'-.-.-..--','<DE>':'-.. .','<K>':'-.-','<KN>':'-.--.','<SK>':'...-.-','<SOS>':'...---...','<VE>':'...-.'}
REVERSE = {v:k for k,v in MORSE.items()}
REVERSE.update({v:k for k,v in PROSIGNS.items()})
WORDS = ["HELLO","WORLD","MORSE","CODE","PYTHON","RADIO","SIGNAL","BRAVO","DELTA","ECHO","FOXTROT","GOLF","HOTEL","INDIA","JULIET","KILO","LIMA","MIKE","NOVEMBER","OSCAR","PAPA","QUEBEC","ROMEO","SIERRA","TANGO","UNIFORM","VICTOR","WHISKEY","XRAY","YANKEE","ZULU","SOS","CQ","DE","73","88"]
SENTENCES = ["HELLO WORLD","SOS SOS SOS","CQ CQ DE RADIO","GOOD MORNING","HOW ARE YOU","MORSE CODE IS FUN","KEEP CALM AND CARRY ON","THE QUICK BROWN FOX","MAY THE FORCE BE WITH YOU"]

STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "morse_stats.json")

class HistoryEntry(TypedDict):
    time: str
    kind: str
    detail: str

class Stats(TypedDict):
    practice_correct: int
    practice_total: int
    quiz_correct: int
    quiz_total: int
    best_streak: int
    history: list[HistoryEntry]

def text_to_morse(text: str) -> str:
    out: list[str] = []
    for ch in text.upper():
        if ch in MORSE: out.append(MORSE[ch])
        elif ch in PROSIGNS: out.append(PROSIGNS[ch])
    return ' '.join(out)
def morse_to_text(morse: str) -> str:
    out: list[str] = []
    for word in morse.strip().split(' / '):
        chars: list[str] = []
        for code in word.split():
            chars.append(REVERSE.get(code,'?'))
        out.append(''.join(chars))
    return ' '.join(out)

class App:
    def __init__(self, root:tk.Tk):
        self.root=root; self.root.title("Morse Code App — Enhanced"); self.root.geometry("680x720")
        self.wpm=tk.IntVar(value=18); self.farnsworth=tk.IntVar(value=18); self.tone=tk.IntVar(value=700)
        self.show_light=tk.BooleanVar(value=True); self.show_timing=tk.BooleanVar(value=True)
        self.playing=False; self.stop_flag=False
        self.stats: Stats = self.load_stats()
        self.practice_answer=""; self.quiz_answer=""; self.quiz_q=0; self.quiz_score=0; self.quiz_mistakes: list[str]=[]
        self.quiz_start=0; self.practice_streak=0; self.best_streak=0
        self.tap_buffer=""; self.tap_last=0; self.tap_timer=None
        self.learn_filter=tk.StringVar(value="All")
        self.build()
        self.update_stats_labels()
        self.root.bind("<space>", self.on_space_tap)

    # ---------- persistence ----------
    def load_stats(self) -> Stats:
        d: Any = {}
        try:
            with open(STATS_FILE) as f: d=json.load(f)
        except Exception: pass
        return {"practice_correct":int(d.get("practice_correct",0)),"practice_total":int(d.get("practice_total",0)),
                "quiz_correct":int(d.get("quiz_correct",0)),"quiz_total":int(d.get("quiz_total",0)),
                "best_streak":int(d.get("best_streak",0)),"history":cast(list[HistoryEntry],d.get("history",[]))}
    def save_stats(self):
        self.stats["best_streak"]=max(self.stats["best_streak"], self.best_streak)
        try:
            with open(STATS_FILE,"w") as f: json.dump(self.stats,f,indent=2)
        except Exception as e: print(e)
    def add_history(self, kind: str, detail: str) -> None:
        self.stats["history"].insert(0, {"time":time.strftime("%H:%M %d %b"),"kind":kind,"detail":detail})
        self.stats["history"]=self.stats["history"][:50]; self.save_stats(); self.refresh_history()

    # ---------- UI ----------
    def build(self):
        top=tk.Frame(self.root); top.pack(fill="x", padx=10, pady=6)
        tk.Label(top,text="⚡ Morse Code Studio",font=("Arial",16,"bold")).pack(side="left")
        tk.Label(top,text="WPM:").pack(side="left", padx=(15,2))
        tk.Scale(top,from_=5,to=40,orient="horizontal",variable=self.wpm,length=120).pack(side="left")
        tk.Label(top,text="Tone:").pack(side="left", padx=(8,2))
        tk.Scale(top,from_=300,to=1200,orient="horizontal",variable=self.tone,length=110).pack(side="left")
        tk.Checkbutton(top,text="💡 Light",variable=self.show_light).pack(side="left", padx=6)
        tk.Checkbutton(top,text="Timing bars",variable=self.show_timing).pack(side="left")

        # Visualizer: light + timing canvas
        viz=tk.Frame(self.root, relief="groove", borderwidth=1); viz.pack(fill="x", padx=10)
        self.light=tk.Canvas(viz,width=70,height=70,bg="white",highlightthickness=0); self.light.pack(side="left",padx=10,pady=6)
        self.light_circle=self.light.create_oval(10,10,60,60,fill="#ddd",outline="#999")
        self.timing_canvas=tk.Canvas(viz,height=70,bg="#111",highlightthickness=0); self.timing_canvas.pack(side="left",fill="x",expand=True,padx=5,pady=6)
        tk.Button(viz,text="⏹ Stop",command=self.stop_playback).pack(side="right",padx=8)

        nb=ttk.Notebook(self.root); nb.pack(fill="both",expand=True,padx=10,pady=6)
        self.t1=tk.Frame(nb); self.t2=tk.Frame(nb); self.t3=tk.Frame(nb); self.t4=tk.Frame(nb); self.t5=tk.Frame(nb); self.t6=tk.Frame(nb); self.t7=tk.Frame(nb)
        for f,t in [(self.t1,"Converter"),(self.t2,"Tap Keyer"),(self.t3,"Learn"),(self.t4,"Practice"),(self.t5,"Quiz"),(self.t6,"History & Stats"),(self.t7,"Settings")]:
            nb.add(f,text=t)

        # Converter
        tk.Label(self.t1,text="Type in either box — it converts live:").pack(anchor="w",padx=10,pady=(8,0))
        tk.Label(self.t1,text="Text:").pack(anchor="w",padx=10)
        self.text_entry=tk.Text(self.t1,height=4,width=70); self.text_entry.pack(padx=10)
        self.text_entry.bind("<KeyRelease>", lambda e: self.live_text_to_morse())
        tk.Label(self.t1,text="Morse  ( .  -  space,  /  = word gap ):").pack(anchor="w",padx=10)
        self.morse_entry=tk.Text(self.t1,height=4,width=70); self.morse_entry.pack(padx=10)
        self.morse_entry.bind("<KeyRelease>", lambda e: self.live_morse_to_text())
        btns=tk.Frame(self.t1); btns.pack(pady=8)
        for txt,cmd in [("▶ Play Text",self.play_text_morse),("▶ Play Morse",self.play_morse_box),("📋 Copy Morse",self.copy_morse),("📋 Copy Text",self.copy_text),("🗑 Clear",self.clear_converter),("💾 Export .txt",self.export_converter)]:
            tk.Button(btns,text=txt,command=cmd).pack(side="left",padx=3)
        self.conv_status=tk.Label(self.t1,text="Ready — try HELLO WORLD",fg="gray"); self.conv_status.pack()
        tk.Label(self.t1,text="Tip: Press Space anywhere (except in text boxes) to tap. In Tap tab, use the big button.",fg="gray",font=("Arial",8)).pack()

        # Tap Keyer
        tk.Label(self.t2,text="Hold / tap the button — short = dot, long = dash. Pause = new letter, longer pause = new word.",wraplength=600).pack(padx=10,pady=8)
        self.tap_btn=tk.Button(self.t2,text="●  TAP / HOLD  (or hold SPACE)",font=("Arial",16,"bold"),height=3,width=30,bg="#222",fg="white")
        self.tap_btn.pack(pady=10)
        self.tap_btn.bind("<ButtonPress-1>", lambda e: self.tap_down()); self.tap_btn.bind("<ButtonRelease-1>", lambda e: self.tap_up())
        tk.Label(self.t2,text="Current letter:").pack()
        self.tap_letter_label=tk.Label(self.t2,text="",font=("Courier",22,"bold")); self.tap_letter_label.pack()
        tk.Label(self.t2,text="Decoded:").pack()
        self.tap_decoded=tk.Label(self.t2,text="",font=("Arial",14),wraplength=600); self.tap_decoded.pack()
        self.tap_morse_label=tk.Label(self.t2,text="",font=("Courier",12),fg="gray"); self.tap_morse_label.pack()
        tk.Button(self.t2,text="Clear Tap",command=self.clear_tap).pack(pady=8)

        # Learn
        lf=tk.Frame(self.t3); lf.pack(fill="x",padx=10,pady=6)
        tk.Label(lf,text="Filter:").pack(side="left")
        ttk.Combobox(lf,textvariable=self.learn_filter,values=["All","Letters","Numbers","Punctuation","Prosigns"],state="readonly",width=14).pack(side="left",padx=5)
        tk.Button(lf,text="Show",command=self.render_learn).pack(side="left")
        tk.Button(lf,text="🔀 Flashcard",command=self.flashcard).pack(side="left",padx=5)
        self.flash_label=tk.Label(self.t3,text="Click Flashcard to start",font=("Arial",20,"bold")); self.flash_label.pack(pady=8)
        tk.Button(self.t3,text="Reveal / Next",command=self.flashcard).pack()
        self.learn_frame=tk.Frame(self.t3); self.learn_frame.pack(fill="both",expand=True,padx=10,pady=6)
        self.render_learn()

        # Practice
        pf=tk.Frame(self.t4); pf.pack(fill="x",padx=10,pady=6)
        tk.Label(pf,text="Mode:").pack(side="left")
        self.practice_mode=tk.StringVar(value="Letters"); ttk.Combobox(pf,textvariable=self.practice_mode,values=["Letters","Words","Sentences"],state="readonly",width=12).pack(side="left",padx=4)
        tk.Label(pf,text="Length:").pack(side="left")
        self.practice_len=tk.IntVar(value=5); tk.Spinbox(pf,from_=1,to=20,textvariable=self.practice_len,width=5).pack(side="left",padx=4)
        tk.Button(pf,text="🎲 New",command=self.new_practice).pack(side="left",padx=6)
        tk.Button(pf,text="▶ Play",command=self.play_practice).pack(side="left")
        self.practice_morse_label=tk.Label(self.t4,text="",font=("Courier",14),wraplength=620); self.practice_morse_label.pack(pady=8)
        tk.Label(self.t4,text="Your answer:").pack()
        self.practice_entry=tk.Entry(self.t4,width=50,font=("Arial",12)); self.practice_entry.pack(); self.practice_entry.bind("<Return>",lambda e: self.check_practice())
        tk.Button(self.t4,text="💡 Hint (first letter)",command=self.practice_hint).pack(pady=4)
        tk.Button(self.t4,text="Check",command=self.check_practice).pack()
        self.practice_result=tk.Label(self.t4,text="",font=("Arial",12,"bold")); self.practice_result.pack(pady=6)
        self.streak_label=tk.Label(self.t4,text="Streak: 0  |  Best: 0"); self.streak_label.pack()

        # Quiz
        qf=tk.Frame(self.t5); qf.pack(fill="x",padx=10,pady=6)
        tk.Label(qf,text="Difficulty:").pack(side="left")
        self.quiz_diff=tk.StringVar(value="Medium"); ttk.Combobox(qf,textvariable=self.quiz_diff,values=["Easy","Medium","Hard"],state="readonly",width=10).pack(side="left",padx=4)
        tk.Button(qf,text="▶ Start Quiz (10 Qs)",command=self.start_quiz).pack(side="left",padx=6)
        tk.Button(qf,text="▶ Play",command=self.play_quiz).pack(side="left")
        self.quiz_morse_label=tk.Label(self.t5,text="",font=("Courier",14),wraplength=620); self.quiz_morse_label.pack(pady=8)
        self.quiz_progress=tk.Label(self.t5,text=""); self.quiz_progress.pack()
        self.quiz_entry=tk.Entry(self.t5,width=50,font=("Arial",12)); self.quiz_entry.pack(); self.quiz_entry.bind("<Return>",lambda e: self.submit_quiz())
        tk.Button(self.t5,text="Submit",command=self.submit_quiz).pack(pady=6)
        self.quiz_result=tk.Label(self.t5,text="",font=("Arial",12,"bold")); self.quiz_result.pack()
        self.quiz_timer_label=tk.Label(self.t5,text="",fg="gray"); self.quiz_timer_label.pack()

        # History & Stats
        self.stats_label=tk.Label(self.t6,text="",font=("Arial",12),justify="left"); self.stats_label.pack(padx=10,pady=8,anchor="w")
        tk.Button(self.t6,text="Reset All Stats",command=self.reset_stats).pack(anchor="w",padx=10)
        tk.Label(self.t6,text="Recent activity:").pack(anchor="w",padx=10,pady=(10,0))
        self.history_box=tk.Text(self.t6,height=12,width=75); self.history_box.pack(padx=10,pady=5)

        # Settings
        tk.Label(self.t7,text="Farnsworth spacing (extra gap between letters, helps learning):").pack(anchor="w",padx=10,pady=(10,0))
        tk.Scale(self.t7,from_=5,to=40,orient="horizontal",variable=self.farnsworth,length=300).pack(anchor="w",padx=10)
        tk.Label(self.t7,text="Shortcuts:\n• Ctrl+Enter — Play current Morse\n• Space (outside text boxes) — Tap keyer\n• Enter in Practice/Quiz — Submit",justify="left").pack(anchor="w",padx=10,pady=10)
        tk.Button(self.t7,text="Open Stats File Location",command=lambda: messagebox.showinfo("Stats",STATS_FILE)).pack(anchor="w",padx=10)
        self.root.bind("<Control-Return>", lambda e: self.play_morse_box())

    # ---------- converter ----------
    def live_text_to_morse(self):
        t=self.text_entry.get("1.0","end-1c"); m=text_to_morse(t)
        self.morse_entry.delete("1.0","end"); self.morse_entry.insert("1.0",m)
        self.conv_status.config(text=f"{len(t)} chars → {len(m)} Morse symbols")
    def live_morse_to_text(self):
        m=self.morse_entry.get("1.0","end-1c"); t=morse_to_text(m)
        # avoid loop: only update text if different and user is in morse box
        if self.root.focus_get()==self.morse_entry:
            self.text_entry.delete("1.0","end"); self.text_entry.insert("1.0",t)
        self.conv_status.config(text=f"Decoded: {t[:60]}")
    def copy_morse(self): self.root.clipboard_clear(); self.root.clipboard_append(self.morse_entry.get("1.0","end-1c"))
    def copy_text(self): self.root.clipboard_clear(); self.root.clipboard_append(self.text_entry.get("1.0","end-1c"))
    def clear_converter(self):
        self.text_entry.delete("1.0","end"); self.morse_entry.delete("1.0","end"); self.conv_status.config(text="Cleared")
    def export_converter(self):
        p=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text","*.txt")])
        if p:
            open(p,"w").write(f"Text:\n{self.text_entry.get('1.0','end-1c')}\n\nMorse:\n{self.morse_entry.get('1.0','end-1c')}\n")
            messagebox.showinfo("Exported",p)

    # ---------- playback ----------
    def unit(self): return 1.2 / max(5,self.wpm.get())  # PARIS standard: dot = 1.2/WPM
    def stop_playback(self): self.stop_flag=True
    def flash(self, on: bool):
        if self.show_light.get():
            self.light.itemconfig(self.light_circle, fill="#ffdd00" if on else "#ddd")
    def play_sequence(self, morse: str):
        if self.playing: return
        self.playing=True; self.stop_flag=False; self.timing_canvas.delete("all")
        u=self.unit(); gap_u=1.2/max(5,self.farnsworth.get())
        def run():
            x=5
            for ch in morse:
                if self.stop_flag: break
                if ch=='.':
                    self.flash(True); _beep(self.tone.get(), int(u*1000)); self.flash(False); time.sleep(u)
                    self.draw_bar(x, u, "#ffd700"); x+=u*60
                elif ch=='-':
                    self.flash(True); _beep(self.tone.get(), int(3*u*1000)); self.flash(False); time.sleep(u)
                    self.draw_bar(x, 3*u, "#ff8800"); x+=3*u*60
                elif ch==' ': time.sleep(max(gap_u, u*2)); x+=gap_u*60
                elif ch=='/': time.sleep(4*u); x+=4*u*60
                if x>600: x=5; self.timing_canvas.delete("all")
            self.playing=False; self.flash(False)
        threading.Thread(target=run,daemon=True).start()
    def draw_bar(self, x: float, dur: float, color: str):
        if not self.show_timing.get(): return
        self.timing_canvas.create_rectangle(x,20,x+max(6,dur*60),50,fill=color,outline="")
    def play_text_morse(self): self.play_sequence(text_to_morse(self.text_entry.get("1.0","end-1c")))
    def play_morse_box(self): self.play_sequence(self.morse_entry.get("1.0","end-1c"))
    def play_practice(self): self.play_sequence(self.practice_morse_label.cget("text"))
    def play_quiz(self): self.play_sequence(self.quiz_morse_label.cget("text"))

    # ---------- tap keyer ----------
    def on_space_tap(self, _e: object):
        # ignore when typing in entries
        if str(self.root.focus_get()).endswith("Text") or str(self.root.focus_get()).endswith("Entry"): return
        if not hasattr(self,'_space_down'): self._space_down=False
        if not self._space_down: self._space_down=True; self.tap_down()
        else: self._space_down=False; self.tap_up()
    def tap_down(self): self.tap_last=time.time()
    def tap_up(self):
        dur=time.time()-self.tap_last
        self.tap_buffer += '.' if dur<0.22 else '-'
        self.tap_letter_label.config(text=self.tap_buffer)
        if self.tap_timer: self.root.after_cancel(self.tap_timer)
        self.tap_timer=self.root.after(700, self.tap_finish_letter)
    def tap_finish_letter(self):
        if not self.tap_buffer: return
        ch=REVERSE.get(self.tap_buffer,'?')
        cur=self.tap_decoded.cget("text")
        self.tap_decoded.config(text=cur+ch)
        self.tap_morse_label.config(text=self.tap_morse_label.cget("text")+" "+self.tap_buffer)
        self.tap_buffer=""; self.tap_letter_label.config(text="")
    def clear_tap(self): self.tap_buffer=""; self.tap_decoded.config(text=""); self.tap_morse_label.config(text=""); self.tap_letter_label.config(text="")

    # ---------- learn ----------
    def render_learn(self):
        for w in self.learn_frame.winfo_children(): w.destroy()
        f=self.learn_filter.get()
        items: list[tuple[str, str]]=[]
        if f in ("All","Letters"): items+=[(k,MORSE[k]) for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        if f in ("All","Numbers"): items+=[(k,MORSE[k]) for k in "0123456789"]
        if f in ("All","Punctuation"): items+=[(k,MORSE[k]) for k in ".,?'/!/:;=&+-_\"$@()"]
        if f in ("All","Prosigns"): items+=[(k,PROSIGNS[k]) for k in PROSIGNS]
        for i,(k,v) in enumerate(items):
            b=tk.Button(self.learn_frame,text=f"{k}\n{v}",width=10,command=lambda vv=v: self.play_sequence(vv))
            b.grid(row=i//6,column=i%6,padx=3,pady=3)
    def flashcard(self):
        if not hasattr(self,'_flash_answer') or self._flash_answer is None:
            pool=[k for k in MORSE if k!=' ']
            self._flash_answer=random.choice(pool); self.flash_label.config(text=self._flash_answer,fg="black")
        else:
            self.flash_label.config(text=f"{self._flash_answer}  =  {MORSE[self._flash_answer]}",fg="#0a7")
            self._flash_answer=None

    # ---------- practice ----------
    def new_practice(self):
        mode=self.practice_mode.get(); n=self.practice_len.get()
        if mode=="Letters": ans=''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(n))
        elif mode=="Words": ans=' '.join(random.choice(WORDS) for _ in range(max(1,n//4)))
        else: ans=random.choice(SENTENCES)
        self.practice_answer=ans; self.practice_morse_label.config(text=text_to_morse(ans))
        self.practice_entry.delete(0,"end"); self.practice_result.config(text="")
    def practice_hint(self):
        if self.practice_answer: self.practice_entry.delete(0,"end"); self.practice_entry.insert(0,self.practice_answer[0])
    def check_practice(self):
        if not self.practice_answer: self.new_practice(); return
        user=self.practice_entry.get().strip().upper(); ok=user==self.practice_answer
        self.stats["practice_total"]+=1
        if ok:
            self.stats["practice_correct"]+=1; self.practice_streak+=1; self.best_streak=max(self.best_streak,self.practice_streak)
            self.practice_result.config(text="✅ Correct!",fg="green")
        else:
            self.practice_streak=0; self.practice_result.config(text=f"❌ Answer: {self.practice_answer}",fg="red")
        self.streak_label.config(text=f"Streak: {self.practice_streak}  |  Best: {self.best_streak}")
        self.add_history("Practice",f"{'✅' if ok else '❌'} {self.practice_answer} — you said {user}")
        self.update_stats_labels(); self.new_practice()

    # ---------- quiz ----------
    def start_quiz(self):
        self.quiz_q=0; self.quiz_score=0; self.quiz_mistakes=[]; self.quiz_start=time.time(); self.next_quiz()
    def next_quiz(self):
        if self.quiz_q>=10:
            elapsed=int(time.time()-self.quiz_start)
            self.quiz_morse_label.config(text="🏁 Quiz finished!")
            self.quiz_progress.config(text=f"Final: {self.quiz_score}/10 in {elapsed}s")
            self.quiz_result.config(text=f"Mistakes: {', '.join(self.quiz_mistakes) if self.quiz_mistakes else 'None — perfect!'}",fg="#0a7")
            self.stats["quiz_total"]+=10; self.stats["quiz_correct"]+=self.quiz_score
            self.add_history("Quiz",f"{self.quiz_score}/10 in {elapsed}s — Mistakes: {self.quiz_mistakes}")
            self.update_stats_labels(); return
        self.quiz_q+=1; d=self.quiz_diff.get()
        n=3 if d=="Easy" else 5 if d=="Medium" else 8
        pool="ABCDEFGHIJKLMNOPQRSTUVWXYZ" if d!="Hard" else "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?/"
        self.quiz_answer=''.join(random.choice(pool) for _ in range(n))
        self.quiz_morse_label.config(text=text_to_morse(self.quiz_answer))
        self.quiz_progress.config(text=f"Question {self.quiz_q}/10  |  Score {self.quiz_score}")
        self.quiz_entry.delete(0,"end"); self.quiz_entry.focus()
    def submit_quiz(self):
        if not self.quiz_answer or self.quiz_q>10: return
        user=self.quiz_entry.get().strip().upper()
        if user==self.quiz_answer: self.quiz_score+=1; self.quiz_result.config(text="✅ Correct!",fg="green")
        else: self.quiz_mistakes.append(f"{self.quiz_answer} (you: {user})"); self.quiz_result.config(text=f"❌ Answer: {self.quiz_answer}",fg="red")
        self.next_quiz()

    # ---------- stats ----------
    def update_stats_labels(self):
        s=self.stats
        self.stats_label.config(text=f"Practice: {s['practice_correct']}/{s['practice_total']}  •  Quiz: {s['quiz_correct']}/{s['quiz_total']}  •  Best streak: {s['best_streak']}")
        self.streak_label.config(text=f"Streak: {self.practice_streak}  |  Best: {max(self.best_streak,s['best_streak'])}")
        self.refresh_history()
    def refresh_history(self):
        self.history_box.delete("1.0","end")
        for h in self.stats["history"]:
            self.history_box.insert("end", f"{h['time']}  [{h['kind']}]  {h['detail']}\n")
    def reset_stats(self):
        if messagebox.askyesno("Reset","Clear all saved stats & history?"):
            self.stats=Stats(practice_correct=0,practice_total=0,quiz_correct=0,quiz_total=0,best_streak=0,history=[])
            self.save_stats(); self.update_stats_labels()

if __name__=="__main__":
    root=tk.Tk(); app=App(root); root.mainloop()
