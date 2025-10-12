import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# Load the dataset
movies = pd.read_csv('https://raw.githubusercontent.com/AnkitKumar1311/Sentiment-Analysis-on-Movie-Reviews/master/IMDB%20Dataset.csv')

# Map sentiment to numerical values
sentiment_map = {'positive': 1, 'negative': 0}
movies['sentiment'] = movies['sentiment'].map(sentiment_map)

# Function to preprocess the review
def preprocess_review(review):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Tokenize the review
    tokens = word_tokenize(review)
    
    # Remove stopwords and lemmatize the tokens
    filtered_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in stop_words]
    
    # Join the filtered tokens back into a string
    filtered_review = ' '.join(filtered_tokens)
    
    return filtered_review

# Preprocess the reviews
movies['review'] = movies['review'].apply(preprocess_review)

# Split data into X and y
X = movies['review']
y = movies['sentiment']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform both the training and testing data
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Define models
models = {
    'MultinomialNB': MultinomialNB(),
    'RandomForestClassifier': RandomForestClassifier(n_estimators=100),
    'LogisticRegression': LogisticRegression(max_iter=1000),
    'SVC': SVC(probability=True)
}

# Train models
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Model: {name}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}\n")

# Hyperparameter tuning for SVC
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf', 'poly']
}
grid = GridSearchCV(SVC(probability=True), param_grid, cv=5)
grid.fit(X_train, y_train)
print(f"Best Parameters: {grid.best_params_}")
print(f"Best Score: {grid.best_score_}")

# Function to analyze the sentiment of a review
def analyze_sentiment(review):
    review = preprocess_review(review)
    review = vectorizer.transform([review])
    sentiment = grid.best_estimator_.predict(review)
    if sentiment[0] == 1:
        return "Positive"
    else:
        return "Negative"

# Test the function
review = "This movie is amazing! I loved it."
print(f"Sentiment: {analyze_sentiment(review)}")