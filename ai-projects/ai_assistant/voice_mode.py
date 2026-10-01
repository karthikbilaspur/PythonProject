
""" voice_mode.py - Speak words, listen answers """
try:
    import pyttsx3
    engine = pyttsx3.init()
    def speak(text):
        engine.say(text)
        engine.runAndWait()
except:
    def speak(text):
        print(f"[VOICE MOCK]: {text}")

def voice_quiz(word_engine, brain):
    print("=== VOICE MODE ===")
    for _ in range(3):
        w = word_engine.generate_random_word()
        if not w: break
        speak(f"What is the meaning of {w['word']}")
        ans = input(f"Speaking: {w['word']} > Your meaning: ")
        if ans.lower() in w['meaning'].lower():
            print("Correct!")
            speak("Correct")
        else:
            print(f"Wrong: {w['meaning']}")
            speak(f"Wrong, it means {w['meaning']}")
            brain.log_mistake(w['word'])
