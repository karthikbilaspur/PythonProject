import random

class CryptoMind:
    def __init__(self):
        self.puzzles = {
            "caesar": self.caesar_cipher,
            "vigenere": self.vigenere_cipher,
            "word_scramble": self.word_scramble,
            "anagram": self.anagram
        }

    def caesar_cipher(self):
        shift = random.randint(1, 10)
        word = random.choice(["hello", "world", "python"])
        encrypted_word = ""
        for char in word:
            encrypted_word += chr((ord(char) - 97 + shift) % 26 + 97)
        return word, encrypted_word, shift

    def vigenere_cipher(self):
        keyword = random.choice(["secret", "code", "cipher"])
        word = random.choice(["hello", "world", "python"])
        encrypted_word = ""
        keyword_index = 0
        for char in word:
            shift = ord(keyword[keyword_index % len(keyword)]) - 97
            encrypted_word += chr((ord(char) - 97 + shift) % 26 + 97)
            keyword_index += 1
        return word, encrypted_word, keyword

    def word_scramble(self):
        word = random.choice(["hello", "world", "python"])
        scrambled_word = list(word)
        random.shuffle(scrambled_word)
        return word, "".join(scrambled_word)

    def anagram(self):
        word = random.choice(["listen", "acts", "weird"])
        anagrams = ["silent", "cats", "wired"]
        return word, anagrams[random.randint(0, len(anagrams) - 1)]

    def play(self):
        print("Welcome to CryptoMind!")
        while True:
            print("\nChoose a puzzle type:")
            print("1. Caesar Cipher")
            print("2. Vigenère Cipher")
            print("3. Word Scramble")
            print("4. Anagram")
            print("5. Quit")
            choice = input("Enter your choice: ")
            if choice == "1":
                word, encrypted_word, shift = self.caesar_cipher()
                print(f"Decrypt the word: {encrypted_word}")
                answer = input("Enter your answer: ")
                if answer == word:
                    print("Correct!")
                else:
                    print(f"Sorry, the correct answer is {word}.")
            elif choice == "2":
                word, encrypted_word, keyword = self.vigenere_cipher()
                print(f"Decrypt the word: {encrypted_word}")
                answer = input("Enter your answer: ")
                if answer == word:
                    print("Correct!")
                else:
                    print(f"Sorry, the correct answer is {word}.")
            elif choice == "3":
                word, scrambled_word = self.word_scramble()
                print(f"Unscramble the word: {scrambled_word}")
                answer = input("Enter your answer: ")
                if answer == word:
                    print("Correct!")
                else:
                    print(f"Sorry, the correct answer is {word}.")
            elif choice == "4":
                word, anagram = self.anagram()
                print(f"Find an anagram of the word: {word}")
                answer = input("Enter your answer: ")
                if answer == anagram:
                    print("Correct!")
                else:
                    print(f"Sorry, one possible anagram is {anagram}.")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    game = CryptoMind()
    game.play()