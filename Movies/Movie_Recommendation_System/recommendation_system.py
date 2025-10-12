import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
movies = pd.read_csv('https://example.com/top_rated_movies.csv')  # Replace with actual URL

# Function to preprocess the plot
def preprocess_plot(plot):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Tokenize the plot
    tokens = word_tokenize(plot)
    
    # Remove stopwords and lemmatize the tokens
    filtered_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in stop_words]
    
    # Join the filtered tokens back into a string
    filtered_plot = ' '.join(filtered_tokens)
    
    return filtered_plot

# Preprocess the plots
movies['description'] = movies['description'].apply(preprocess_plot)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the plots and transform them into vectors
plot_vectors = vectorizer.fit_transform(movies['description'])

# Function to get movie recommendations
def get_recommendations(movie_title, num_recommendations):
    # Get the index of the movie
    movie_index = movies[movies['title'] == movie_title].index[0]
    
    # Calculate the cosine similarity between the movie and all other movies
    similarities = cosine_similarity(plot_vectors[movie_index:movie_index+1], plot_vectors).flatten()
    
    # Get the indices of the top N most similar movies
    top_indices = similarities.argsort()[-num_recommendations-1:-1][::-1]
    
    # Get the titles of the top N most similar movies
    recommended_movies = movies.iloc[top_indices]['title']
    
    return recommended_movies

# Test the function
movie_title = 'The Shawshank Redemption'
num_recommendations = 5
recommended_movies = get_recommendations(movie_title, num_recommendations)
print(f"Recommended movies for '{movie_title}':")
print(recommended_movies)