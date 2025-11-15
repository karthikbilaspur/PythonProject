import nltk
from nltk.corpus import words
from nltk.metrics import edit_distance
from collections import Counter
import re

# Download required NLTK data
nltk.download('words')
nltk.download('brown')

# Get English words
english_words = set(words.words())

# Get word frequencies from Brown Corpus
brown_freq = Counter(nltk.corpus.brown.words())

def spell_check(text: str) -> None:
    # Tokenize the text into words
    words_to_check = re.findall(r'\b\w+\b', text)

    # Check each word
    for word in words_to_check:
        # Remove punctuation
        clean_word = word.lower()

        # Check if word is in English dictionary
        if clean_word not in english_words:
            print(f"Unknown word: {word}")

            # Suggest corrections
            suggestions = suggest_corrections(clean_word)
            if suggestions:
                print(f"Suggestions: {', '.join(suggestions)}")

def suggest_corrections(word: str) -> list[str]:
    # Find words with edit distance <= 2
    candidates = [w for w in english_words if edit_distance(w, word) <= 2]

    # Rank candidates by frequency
    ranked_candidates = sorted(candidates, key=lambda x: brown_freq[x], reverse=True)

    return ranked_candidates[:5]  # Return top 5 suggestions

def main():
    text = "Ths is a sampl text with som spelling errrs"
    spell_check(text)

if __name__ == "__main__":
    main()