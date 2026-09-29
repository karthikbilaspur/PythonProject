import json

def save_words_to_file(words, filename="words.json"):
    try:
        with open(filename, "w") as file:
            json.dump(words, file, indent=4)
        print(f"Words saved to {filename} successfully.")
    except Exception as e:
        print(f"Error saving words to file: {e}")

def load_words_from_file(filename="words.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except Exception as e:
        print(f"Error loading words from file: {e}")
        return None

def export_words_to_csv(words, filename="words.csv"):
    try:
        with open(filename, "w") as file:
            file.write("Category,Word,Meaning\n")
            for category in words['words']:
                for word in words['words'][category]:
                    file.write(f"{category},{word['word']},{word['meaning']}\n")
        print(f"Words exported to {filename} successfully.")
    except Exception as e:
        print(f"Error exporting words to CSV file: {e}")

def import_words_from_csv(filename="words.csv"):
    try:
        words = {'words': {}}
        with open(filename, "r") as file:
            next(file)  # Skip header
            for line in file:
                category, word, meaning = line.strip().split(",")
                if category not in words['words']:
                    words['words'][category] = []
                words['words'][category].append({"word": word, "meaning": meaning})
        print(f"Words imported from {filename} successfully.")
        return words
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except Exception as e:
        print(f"Error importing words from CSV file: {e}")
        return None

def file_manager_menu(words):
    while True:
        print("\nFile Manager Menu:")
        print("1. Save Words to File")
        print("2. Load Words from File")
        print("3. Export Words to CSV")
        print("4. Import Words from CSV")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            save_words_to_file(words)
        elif choice == "2":
            loaded_words = load_words_from_file()
            if loaded_words:
                words['words'] = loaded_words['words']
                print("Words loaded successfully.")
        elif choice == "3":
            export_words_to_csv(words)
        elif choice == "4":
            imported_words = import_words_from_csv()
            if imported_words:
                words['words'] = imported_words['words']
                print("Words imported successfully.")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")