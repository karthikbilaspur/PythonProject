from nltk.corpus import wordnet
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
nltk.download('wordnet')

class AdjectiveForms:
    def __init__(self):
        self.irregular_adjectives = {
            'good': ('better', 'best'),
            'bad': ('worse', 'worst'),
            'far': ('farther', 'farthest'),
            'little': ('less', 'least'),
            'many': ('more', 'most'),
            'much': ('more', 'most'),
        }

    def get_synsets(self, adjective):
        return wordnet.synsets(adjective)

    def generate_comparative_superlative(self, adjective):
        adjective = adjective.lower()
        if adjective in self.irregular_adjectives:
            return self.irregular_adjectives[adjective]

        synsets = self.get_synsets(adjective)
        if synsets:
            syn = synsets[0]
            lemmas = [lemma.name().replace('_', ' ') for lemma in syn.lemmas()]
            if len(lemmas) >= 2:
                comparative = lemmas[1]
            else:
                comparative = self.rule_based_comparative(adjective)
            if len(lemmas) >= 3:
                superlative = lemmas[2]
            else:
                superlative = self.rule_based_superlative(adjective)
            return comparative, superlative
        else:
            comparative = self.rule_based_comparative(adjective)
            superlative = self.rule_based_superlative(adjective)
            return comparative, superlative

    def rule_based_comparative(self, adjective):
        if adjective.endswith('e'):
            return adjective + 'r'
        elif adjective.endswith('y'):
            return adjective[:-1] + 'ier'
        elif adjective.endswith('er') or adjective.endswith('ow'):
            return adjective + 'er'
        else:
            return adjective + 'er'

    def rule_based_superlative(self, adjective):
        if adjective.endswith('e'):
            return adjective + 'st'
        elif adjective.endswith('y'):
            return adjective[:-1] + 'iest'
        elif adjective.endswith('er') or adjective.endswith('ow'):
            return adjective + 'est'
        else:
            return adjective + 'est'

    def train_machine_learning_model(self, adjectives, comparatives, superlatives):
        # Create a CountVectorizer object
        vectorizer = CountVectorizer()

        # Fit the vectorizer to the adjectives and transform them into vectors
        X = vectorizer.fit_transform(adjectives)

        # Split the data into training and testing sets
        X_train, X_test, y_train_comparative, y_test_comparative = train_test_split(X, comparatives, test_size=0.2, random_state=42)
        _, _, y_train_superlative, y_test_superlative = train_test_split(X, superlatives, test_size=0.2, random_state=42)

        # Train a Multinomial Naive Bayes classifier
        comparative_model = MultinomialNB()
        comparative_model.fit(X_train, y_train_comparative)

        superlative_model = MultinomialNB()
        superlative_model.fit(X_train, y_train_superlative)

        return comparative_model, superlative_model, vectorizer

    def train_deep_learning_model(self, adjectives, comparatives, superlatives):
        # Create a tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(adjectives)

        # Convert the adjectives to sequences
        sequences = tokenizer.texts_to_sequences(adjectives)

        # Pad the sequences
        padded_sequences = pad_sequences(sequences, maxlen=10)

        # One-hot encode the comparatives and superlatives
        comparative_one_hot = pd.get_dummies(comparatives).values
        superlative_one_hot = pd.get_dummies(superlatives).values

        # Split the data into training and testing sets
        X_train, X_test, y_train_comparative, y_test_comparative = train_test_split(padded_sequences, comparative_one_hot, test_size=0.2, random_state=42)
        _, _, y_train_superlative, y_test_superlative = train_test_split(padded_sequences, superlative_one_hot, test_size=0.2, random_state=42)

        # Create and compile the model
        comparative_model = Sequential()
        comparative_model.add(Embedding(len(tokenizer.word_index) + 1, 64, input_length=10))
        comparative_model.add(LSTM(64, dropout=0.2))
        comparative_model.add(Dense(comparative_one_hot.shape[1], activation='softmax'))
        comparative_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        superlative_model = Sequential()
        superlative_model.add(Embedding(len(tokenizer.word_index) + 1, 64, input_length=10))
        superlative_model.add(LSTM(64, dropout=0.2))
        superlative_model.add(Dense(superlative_one_hot.shape[1], activation='softmax'))
        superlative_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        comparative_model.fit(X_train, y_train_comparative, epochs=10, batch_size=32)
        superlative_model.fit(X_train, y_train_superlative, epochs=10, batch_size=32)

        return comparative_model, superlative_model, tokenizer

def main():
    adjective_forms = AdjectiveForms()
    adjectives = ['good', 'bad', 'far', 'little', 'many', 'much']
    comparatives = ['better', 'worse', 'farther', 'less', 'more', 'more']
    superlatives = ['best', 'worst', 'farthest', 'least', 'most', 'most']

    # Train machine learning models
    comparative_ml_model, superlative_ml_model, vectorizer = adjective_forms.train_machine_learning_model(adjectives, comparatives, superlatives)

    # Train deep learning models
    comparative_dl_model, superlative_dl_model, tokenizer = adjective_forms.train_deep_learning_model(adjectives, comparatives, superlatives)

    # Test the models
    test_adjective = 'happy'
    comparative, superlative = adjective_forms.generate_comparative_superlative(test_adjective)
    print(f"Comparative of {test_adjective}: {comparative}")
    print(f"Superlative of {test_adjective}: {superlative}")

    # Use machine learning models to predict comparative and superlative forms
    test_adjective_vector = vectorizer.transform([test_adjective])
    predicted_comparative = comparative_ml_model.predict(test_adjective_vector)
    predicted_superlative = superlative_ml_model.predict(test_adjective_vector)
    print(f"Predicted Comparative of {test_adjective} using ML: {predicted_comparative}")
    print(f"Predicted Superlative of {test_adjective} using ML: {predicted_superlative}")

    # Use deep learning models to predict comparative and superlative forms
    test_adjective_sequence = tokenizer.texts_to_sequences([test_adjective])
    test_adjective_padded_sequence = pad_sequences(test_adjective_sequence, maxlen=10)
    predicted_comparative = comparative_dl_model.predict(test_adjective_padded_sequence)
    predicted_superlative = superlative_dl_model.predict(test_adjective_padded_sequence)
    print(f"Predicted Comparative of {test_adjective} using DL: {predicted_comparative}")
    print(f"Predicted Superlative of {test_adjective} using DL: {predicted_superlative}")

if __name__ == "__main__":
    main()