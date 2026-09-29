import random

# List of word categories
categories = ["animals", "food", "cities", "countries", "planets", "sports", "instruments", "vehicles"]

# Dictionary of words with meanings
words = {
    "animals": [
        {"word": "dog", "meaning": "a domesticated carnivorous mammal"},
        {"word": "cat", "meaning": "a small domesticated carnivorous mammal"},
        {"word": "lion", "meaning": "a large carnivorous mammal"},
        # Add more animal words here...
    ],
    "food": [
        {"word": "apple", "meaning": "a sweet, juicy fruit"},
        {"word": "pizza", "meaning": "a dish of Italian origin"},
        {"word": "sushi", "meaning": "a Japanese dish"},
        # Add more food words here...
    ],
    # Add more categories and words here...
}

def generate_random_word(category):
    return random.choice(words[category])

def generate_random_words(num_words):
    random_words = []
    for _ in range(num_words):
        category = random.choice(categories)
        word = generate_random_word(category)
        random_words.append(word)
    return random_words

# Generate 10 random words
random_words = generate_random_words(10)
for word in random_words:
    print(f"Word: {word['word']}, Meaning: {word['meaning']}")