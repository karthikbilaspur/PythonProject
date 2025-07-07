import random
from word_list import words
from file_manager import save_words_to_file, load_words_from_file
from quiz import quiz_mode, advanced_quiz_mode

def generate_random_word(category=None):
    if category:
        if category in words['words']:
            return random.choice(words['words'][category])
        else:
            print("Invalid category.")
            return None
    else:
        category = random.choice(list(words['words'].keys()))
        return random.choice(words['words'][category])

def generate_random_words(num_words, category=None):
    random_words = []
    for _ in range(num_words):
        word = generate_random_word(category)
        if word:
            random_words.append(word)
    return random_words

def search_word(word):
    for category in words['words']:
        for w in words['words'][category]:
            if w['word'].lower() == word.lower():
                return w
    return None

def add_word(category, word, meaning):
    if category in words['words']:
        words['words'][category].append({"word": word, "meaning": meaning})
    else:
        words['words'][category] = [{"word": word, "meaning": meaning}]
    print("Word added successfully.")

def delete_word(word):
    for category in words['words']:
        for w in words['words'][category]:
            if w['word'].lower() == word.lower():
                words['words'][category].remove(w)
                print("Word deleted successfully.")
                return
    print("Word not found.")

def display_all_words():
    for category in words['words']:
        print(f"Category: {category}")
        for word in words['words'][category]:
            print(f"Word: {word['word']}, Meaning: {word['meaning']}")
        print()

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
        print("11. Advanced Quiz Mode")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Available categories:")
            for category in words['words']:
                print(category)
            category = input("Enter category (or leave blank for random category): ")
            if category:
                random_word = generate_random_word(category)
            else:
                random_word = generate_random_word()
            if random_word:
                print(f"Word: {random_word['word']}, Meaning: {random_word['meaning']}")
        elif choice == "2":
            print("Available categories:")
            for category in words['words']:
                print(category)
            category = input("Enter category (or leave blank for random category): ")
            try:
                num_words = int(input("Enter the number of words to generate: "))
                if category:
                    random_words = generate_random_words(num_words, category)
                else:
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
            print("Available categories:")
            for category in words['words']:
                print(category)
            category = input("Enter category: ")
            word = input("Enter the word to add: ")
            meaning = input("Enter the meaning of the word: ")
            add_word(category, word, meaning)
        elif choice == "5":
            word = input("Enter the word to delete: ")
            delete_word(word)
        elif choice == "6":
            break
        elif choice == "7":
            display_all_words()
        elif choice == "8":
            save_words_to_file(words)
        elif choice == "9":
            loaded_words = load_words_from_file()
            if loaded_words:
                words['words'] = loaded_words['words']
                print("Words loaded successfully.")
        elif choice == "10":
            quiz_mode(words)
        elif choice == "11":
            advanced_quiz_mode(words)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()