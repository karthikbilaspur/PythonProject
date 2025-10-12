import time
import random
import winsound

# Define Morse code mapping
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'
}

def text_to_morse(text):
    morse = ''
    for char in text.upper():
        if char in morse_code:
            morse += morse_code[char] + ' '
    return morse

def morse_to_text(morse):
    text = ''
    morse_chars = morse.split(' ')
    reverse_mapping = {value: key for key, value in morse_code.items()}
    for char in morse_chars:
        if char in reverse_mapping:
            text += reverse_mapping[char]
    return text

def play_morse(morse, speed):
    for char in morse:
        if char == '.':
            winsound.Beep(1000, int(100 / speed))
            time.sleep(0.1 / speed)
        elif char == '-':
            winsound.Beep(1000, int(300 / speed))
            time.sleep(0.3 / speed)
        elif char == ' ':
            time.sleep(0.2 / speed)
        elif char == '/':
            time.sleep(0.5 / speed)

def practice_morse():
    print("Morse Code Practice")
    print("1. Text to Morse")
    print("2. Morse to Text")
    print("3. Random Practice")
    print("4. Quiz Mode")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        text = input("Enter text to convert to Morse: ")
        morse = text_to_morse(text)
        print(f"Morse Code: {morse}")
        speed = float(input("Enter speed (default=1): ") or 1)
        play_morse(morse, speed)
        
    elif choice == '2':
        morse = input("Enter Morse code to convert to text: ")
        text = morse_to_text(morse)
        print(f"Text: {text}")
        
    elif choice == '3':
        text = ''.join(random.choice(list(morse_code.keys())) for _ in range(10))
        morse = text_to_morse(text)
        print(f"Morse Code: {morse}")
        speed = float(input("Enter speed (default=1): ") or 1)
        play_morse(morse, speed)
        answer = input("Enter the text: ")
        if answer.upper() == text:
            print("Correct!")
        else:
            print(f"Sorry, the correct answer was {text}")
            
    elif choice == '4':
        score = 0
        for _ in range(10):
            text = ''.join(random.choice(list(morse_code.keys())) for _ in range(5))
            morse = text_to_morse(text)
            print(f"Morse Code: {morse}")
            answer = input("Enter the text: ")
            if answer.upper() == text:
                score += 1
                print("Correct!")
            else:
                print(f"Sorry, the correct answer was {text}")
        print(f"Your final score is {score} out of 10")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    practice_morse()