from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string

nltk.download('stopwords')

def auto_spell_checker(text):
    """
    Checks for spelling errors in the given text and suggests corrections.
    
    Args:
        text (str): The text to be checked.
    
    Returns:
        A dictionary with misspelled words as keys and their corrections as values.
    """
    spell = SpellChecker()

    # Split the text into words
    words = text.split()

    # Find misspelled words
    misspelled = spell.unknown(words)

    # Create a dictionary with corrections
    corrections = {}
    for word in misspelled:
        corrections[word] = spell.correction(word)

    return corrections

def text_statistics(text):
    """
    Calculates statistics for the given text.
    
    Args:
        text (str): The text to be analyzed.
    
    Returns:
        A dictionary with text statistics.
    """
    stats = {
        'word_count': len(text.split()),
        'char_count': len(text),
        'stopword_count': sum(1 for word in text.lower().split() if word in stopwords.words('english')),
        'avg_word_length': sum(len(word) for word in text.split()) / len(text.split()),
    }
    return stats

def most_common_words(text, n=5):
    """
    Finds the most common words in the given text.
    
    Args:
        text (str): The text to be analyzed.
        n (int): The number of most common words to return.
    
    Returns:
        A list of tuples with the most common words and their frequencies.
    """
    words = text.translate(str.maketrans('', '', string.punctuation)).lower().split()
    return Counter(words).most_common(n)

def main():
    while True:
        print("\nAuto Spell Checker Menu:")
        print("1. Spell Check")
        print("2. Text Statistics")
        print("3. Most Common Words")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '4':
            break
        
        text = input("Enter the text: ")
        
        if choice == '1':
            corrections = auto_spell_checker(text)
            if corrections:
                print("Misspelled words and their corrections:")
                for word, correction in corrections.items():
                    print(f"{word}: {correction}")
            else:
                print("No spelling errors found.")
        
        elif choice == '2':
            stats = text_statistics(text)
            print("Text statistics:")
            for key, value in stats.items():
                print(f"{key}: {value}")
        
        elif choice == '3':
            common_words = most_common_words(text)
            print("Most common words:")
            for word, frequency in common_words:
                print(f"{word}: {frequency}")
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()