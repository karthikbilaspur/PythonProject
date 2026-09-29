import json
import random

# Dictionary of words with meanings
words = {
    "words": [
        {"word": "apple", "meaning": "a fruit"},
        {"word": "dog", "meaning": "an animal"},
        {"word": "cat", "meaning": "a small domesticated carnivorous mammal"},
        {"word": "car", "meaning": "a road vehicle"},
        {"word": "tree", "meaning": "a perennial plant with a single stem"},
        {"word": "house", "meaning": "a building for human habitation"},
        {"word": "pen", "meaning": "a writing instrument"},
        {"word": "paper", "meaning": "a material for writing or printing"},
        {"word": "book", "meaning": "a written or printed work"},
        {"word": "chair", "meaning": "a piece of furniture for sitting"},
        {"word": "table", "meaning": "a piece of furniture with a flat surface"},
        {"word": "phone", "meaning": "a device for communicating"},
        {"word": "computer", "meaning": "an electronic device for processing data"},
        {"word": "music", "meaning": "an art form consisting of sound and silence"},
        {"word": "movie", "meaning": "a series of moving images"},
        {"word": "game", "meaning": "an activity or contest with rules"},
        {"word": "sport", "meaning": "a physical activity or competition"},
        {"word": "food", "meaning": "anything that is eaten to sustain life"},
        {"word": "water", "meaning": "a liquid substance"},
        {"word": "fire", "meaning": "the rapid oxidation of a material"},
        {"word": "earth", "meaning": "the planet we live on"},
        {"word": "sun", "meaning": "the star at the center of our solar system"},
        {"word": "moon", "meaning": "the natural satellite of the earth"},
        {"word": "star", "meaning": "a massive ball of hot, glowing gas"},
        {"word": "river", "meaning": "a natural flowing body of water"},
        {"word": "lake", "meaning": "a body of water surrounded by land"},
        {"word": "ocean", "meaning": "a vast body of saltwater"},
        {"word": "mountain", "meaning": "a natural elevation of the earth's surface"},
        {"word": "valley", "meaning": "a low area of land between hills or mountains"},
        {"word": "city", "meaning": "a large human settlement"},
        {"word": "town", "meaning": "a smaller human settlement"},
        {"word": "village", "meaning": "a small human settlement"},
        {"word": "school", "meaning": "an institution for education"},
        {"word": "university", "meaning": "an institution for higher education"},
        {"word": "library", "meaning": "a collection of books and other written materials"},
        {"word": "hospital", "meaning": "an institution for medical care"},
        {"word": "doctor", "meaning": "a person trained to practice medicine"},
        {"word": "nurse", "meaning": "a person trained to care for the sick or injured"},
        {"word": "teacher", "meaning": "a person who educates others"},
        {"word": "student", "meaning": "a person who is learning"},
        {"word": "engineer", "meaning": "a person who designs and builds machines or structures"},
        {"word": "lawyer", "meaning": "a person who practices law"},
        {"word": "artist", "meaning": "a person who creates art"},
        {"word": "musician", "meaning": "a person who plays music"},
        {"word": "writer", "meaning": "a person who writes books or articles"},
        {"word": "actor", "meaning": "a person who performs in plays or movies"},
        {"word": "athlete", "meaning": "a person who competes in sports"}
    ]
}

def generate_random_word():
    return random.choice(words['words'])

def generate_random_words(num_words):
    random_words = []
    for _ in range(num_words):
        word = generate_random_word()
        random_words.append(word)
    return random_words

def search_word(word):
    for w in words['words']:
        if w['word'].lower() == word.lower():
            return w
    return None

def add_word(word, meaning):
    words['words'].append({"word": word, "meaning": meaning})

def delete_word(word):
    for w in words['words']:
        if w['word'].lower() == word.lower():
            words['words'].remove(w)
            return

def display_all_words():
    for word in words['words']:
        print(f"Word: {word['word']}, Meaning: {word['meaning']}")

def save_words_to_file():
    with open("words.json", "w") as file:
        json.dump(words, file, indent=4)
    print("Words saved to file successfully.")

def load_words_from_file():
    try:
        with open("words.json", "r") as file:
            global words
            words = json.load(file)
        print("Words loaded from file successfully.")
    except FileNotFoundError:
        print("File not found.")

def quiz_mode():
    score = 0
    for _ in range(5):
        random_word = generate_random_word()
        answer = input(f"What is the meaning of '{random_word['word']}'? ")
        if answer.lower() == random_word['meaning'].lower():
            score += 1
            print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{random_word['meaning']}'.")
    print(f"Your final score is {score} out of 5.")

def main():
    while True:
        print("\nWord Generator Menu:")
        print("1. Generate Random Word")
        print("2. Generate Multiple Random Words")
        print("3. Search for a Word")
        print("4. Add a Word")
        print("5. Delete a Word")
        print("6. Exit")
        print("7. Display All Words")
        print("8. Save Words to File")
        print("9. Load Words from File")
        print("10. Quiz Mode")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            random_word = generate_random_word()
            print(f"Word: {random_word['word']}, Meaning: {random_word['meaning']}")
        elif choice == "2":
            try:
                num_words = int(input("Enter the number of words to generate: "))
                random_words = generate_random_words(num_words)
                for word in random_words:
                    print(f"Word: {word['word']}, Meaning: {word['meaning']}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            word = input("Enter the word to search for: ")
            result = search_word(word)
            if result:
                print(f"Word: {result['word']}, Meaning: {result['meaning']}")
            else:
                print("Word not found.")
        elif choice == "4":
            word = input("Enter the word to add: ")
            meaning = input("Enter the meaning of the word: ")
            add_word(word, meaning)
            print("Word added successfully.")
        elif choice == "5":
            word = input("Enter the word to delete: ")
            delete_word(word)
            print("Word deleted successfully.")
        elif choice == "6":
            break
        elif choice == "7":
            display_all_words()
        elif choice == "8":
            save_words_to_file()
        elif choice == "9":
            load_words_from_file()
        elif choice == "10":
            quiz_mode()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()