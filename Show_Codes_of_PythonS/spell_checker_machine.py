import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import words
import nltk
nltk.download('words')

# Get English words
english_words = set(words.words())

# Create a dataset of correct and incorrect spellings
data = {
    'text': [],
    'label': []
}

# Generate some incorrect spellings
for word in english_words:
    if np.random.rand() < 0.5:
        # Introduce a random typo
        typo_type = np.random.choice(['insert', 'delete', 'replace'])
        if typo_type == 'insert':
            typo_word = word + np.random.choice(list('abcdefghijklmnopqrstuvwxyz'))
        elif typo_type == 'delete':
            typo_word = word[:-1]
        else:
            typo_word = word[:-1] + np.random.choice(list('abcdefghijklmnopqrstuvwxyz'))
        data['text'].append(typo_word)
        data['label'].append(0)  # Incorrect spelling
    data['text'].append(word)
    data['label'].append(1)  # Correct spelling

df = pd.DataFrame(data)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform both the training and testing data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_tfidf, y_train)

# Evaluate the model
y_pred = clf.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Use the model to check spellings
def spell_check(text: str) -> None:
    text_tfidf = vectorizer.transform([text])
    prediction = clf.predict(text_tfidf)
    if prediction[0] == 1:
        print(f"'{text}' is likely a correct spelling.")
    else:
        print(f"'{text}' is likely an incorrect spelling.")

# Test the spell check function
spell_check("hello")
spell_check("helo")