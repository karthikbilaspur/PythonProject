import datetime, webbrowser
from typing import Any, cast
try:
 import speech_recognition as sr, pyttsx3  # type: ignore[reportMissingTypeStubs]
except ImportError: sr=None; pyttsx3=None
def speak(t: str, e: Any = None) -> None:
 engine = e
 if engine is None:
  if pyttsx3 is None: return
  engine = cast(Any, pyttsx3).init()
 engine.say(t); engine.runAndWait()
def get_audio() -> str:
 if sr is None: return ""
 r=sr.Recognizer()
 with sr.Microphone() as s:
  r.adjust_for_ambient_noise(s, duration=0.5); print("Listening...")
  try: a=r.listen(s, timeout=8, phrase_time_limit=8)
  except Exception: return ""
 try:
  t = cast(str, cast(Any, r).recognize_google(a)); print("You said:", t); return t.lower()
 except Exception: return ""
def handle(t: str, e: Any) -> bool:
 if not t: return True
 if "google" in t: speak("Opening Google",e); webbrowser.open("https://www.google.com")
 elif "youtube" in t: speak("Opening YouTube",e); webbrowser.open("https://www.youtube.com")
 elif "gmail" in t: speak("Opening Gmail",e); webbrowser.open("https://mail.google.com")
 elif "news" in t: speak("Here are headlines",e); webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
 elif "search" in t:
  q=t.replace("search","").strip(); speak(f"Searching for {q}",e); webbrowser.open_new_tab("https://www.google.com/search?q="+q.replace(" ","+"))
 elif "time" in t: speak("The time is "+datetime.datetime.now().strftime("%H:%M:%S"),e)
 elif "camera" in t or "take a photo" in t:
  speak("Taking a photo",e)
  try:
   import cv2; c=cv2.VideoCapture(0); ok,f=c.read(); c.release()
   if ok: cv2.imwrite("photo.jpg",f)
  except Exception as ex: print(ex)
 elif "quit" in t or "exit" in t or "stop" in t: speak("Goodbye",e); return False
 else: speak("Sorry, I did not understand",e)
 return True
def main():
 if pyttsx3 is None: print("pip install SpeechRecognition pyttsx3 pyaudio"); return
 e: Any = cast(Any, pyttsx3).init(); speak("Hello! This is your Voice Assistant. How can I help you?",e)
 while True:
  if not handle(get_audio(),e): break
def open_window(parent: Any = None) -> None:
 _ = parent
 import threading; threading.Thread(target=main, daemon=True).start(); print("Voice Assistant started - speak into mic.")
if __name__=="__main__": main()
