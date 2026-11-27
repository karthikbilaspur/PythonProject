import tkinter as tk, wave, threading
from tkinter import filedialog, messagebox
try: import pyaudio
except ImportError: pyaudio=None
def record_audio(fn: str, seconds: int) -> str:
 if pyaudio is None: raise RuntimeError("pip install pyaudio")
 CHUNK,FORMAT,CHANNELS,RATE=1024,pyaudio.paInt16,2,44100
 p=pyaudio.PyAudio(); s=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK); frames: list[bytes]=[]
 for _ in range(int(RATE/CHUNK*seconds)): frames.append(s.read(CHUNK))
 s.stop_stream(); s.close(); p.terminate()
 with wave.open(fn,"wb") as wf: wf.setnchannels(CHANNELS); wf.setsampwidth(p.get_sample_size(FORMAT)); wf.setframerate(RATE); wf.writeframes(b"".join(frames))
 return fn
class AudioRecorder:
 def __init__(self, parent: tk.Misc | None = None):
  self.window=tk.Toplevel(parent) if parent else tk.Tk(); self.window.title("Audio Recorder"); self.window.geometry("420x260")
  tk.Label(self.window,text="Audio Recorder",font=("Arial",14,"bold")).pack(pady=10)
  tk.Label(self.window,text="Seconds:").pack(); self.sec_var=tk.StringVar(value="5"); tk.Entry(self.window,textvariable=self.sec_var,width=10).pack()
  tk.Label(self.window,text="Save as:").pack(pady=5); self.file_entry=tk.Entry(self.window,width=45); self.file_entry.insert(0,"recording.wav"); self.file_entry.pack()
  tk.Button(self.window,text="Browse",command=self.browse).pack(pady=3)
  tk.Button(self.window,text="Start Recording",bg="#F44336",fg="white",command=self.start).pack(pady=10)
  self.status=tk.Label(self.window,text="",fg="green"); self.status.pack()
 def browse(self):
  p=filedialog.asksaveasfilename(defaultextension=".wav",filetypes=[("WAV","*.wav")])
  if p: self.file_entry.delete(0,tk.END); self.file_entry.insert(0,p)
 def start(self):
  def job():
   try: self.status.config(text="Recording..."); self.window.update(); out=record_audio(self.file_entry.get().strip(), int(self.sec_var.get() or 5)); self.status.config(text="Saved: "+out)
   except Exception as e: messagebox.showerror("Error",str(e))
  threading.Thread(target=job,daemon=True).start()
 def run(self): self.window.mainloop()
def open_window(parent: tk.Misc | None = None) -> AudioRecorder: return AudioRecorder(parent)
if __name__=="__main__": AudioRecorder().run()
