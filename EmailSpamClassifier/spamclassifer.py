import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

# Load the dataset
def load_dataset(file_path):
    data = pd.read_csv(file_path)
    return data

# Preprocess the data
def preprocess_data(data):
    # Convert all text to lowercase
    data['email'] = data['email'].apply(lambda x: x.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    data['email'] = data['email'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words]))
    
    return data

# Split the data into training and testing sets
def split_data(data):
    X = data['email']
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Train the model
def train_model(X_train, y_train):
    vectorizer = CountVectorizer()
    X_train_count = vectorizer.fit_transform(X_train)
    model = MultinomialNB()
    model.fit(X_train_count, y_train)
    return model, vectorizer

# Evaluate the model
def evaluate_model(model, vectorizer, X_test, y_test):
    X_test_count = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_count)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    return accuracy, report, matrix

# Use the model to classify new emails
def classify_email(model, vectorizer, email):
    email_count = vectorizer.transform([email])
    prediction = model.predict(email_count)
    return prediction[0]

# Main function
def main():
    # Load the dataset
    data = load_dataset('email_dataset.csv')
    
    # Preprocess the data
    data = preprocess_data(data)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data)
    
    # Train the model
    model, vectorizer = train_model(X_train, y_train)
    
    # Evaluate the model
    accuracy, report, matrix = evaluate_model(model, vectorizer, X_test, y_test)
    print(f'Accuracy: {accuracy:.3f}')
    print(report)
    print(matrix)
    
    # Classify a new email
    email = 'You have won a prize! Click here to claim it.'
    prediction = classify_email(model, vectorizer, email)
    print(f'Prediction: {prediction}')

if __name__ == '__main__':
    main()