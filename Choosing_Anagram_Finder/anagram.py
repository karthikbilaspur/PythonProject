import itertools

def find_anagrams(word, min_length=0, max_length=None, dictionary=None):
    """Generate all possible anagrams for a word"""
    # Remove spaces and convert to lowercase
    word = word.replace(" ", "").lower()
    
    if max_length is None:
        max_length = len(word)
    
    # Generate all permutations
    perms = [''.join(p) for r in range(min_length, max_length + 1) 
             for p in itertools.permutations(word, r)]
    
    # Remove duplicates by converting to a set
    anagrams = set(perms)
    
    if dictionary:
        # Filter anagrams using a dictionary file
        with open(dictionary, 'r') as f:
            dict_words = set(word.strip().lower() for word in f)
        anagrams = anagrams & dict_words
    
    return anagrams

def load_dictionary(file_path):
    """Load a dictionary file into a set"""
    with open(file_path, 'r') as f:
        return set(word.strip().lower() for word in f)

def main():
    word = input("Enter a word: ")
    min_length = int(input("Enter minimum anagram length (default=0): ") or 0)
    max_length = input("Enter maximum anagram length (default=word length): ")
    max_length = int(max_length) if max_length else None
    
    use_dictionary = input("Use a dictionary file to filter anagrams? (y/n): ")
    dictionary = None
    if use_dictionary.lower() == 'y':
        dictionary = input("Enter dictionary file path: ")
    
    anagrams = find_anagrams(word, min_length, max_length, dictionary)
    
    print("Anagrams:")
    for anagram in anagrams:
        print(anagram)

if __name__ == "__main__":
    main()