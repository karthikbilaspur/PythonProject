import requests
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# API endpoint and API key
api_endpoint = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
api_key = "YOUR_API_KEY_HERE"

# Function to get word embeddings for a location
def get_word_embedding(location: str) -> np.ndarray | None:
    params = {
        "input": location,
        "key": api_key
    }
    response = requests.get(api_endpoint, params=params)
    data = response.json()
    if data["status"] != "OK":
        return None
    # Get the first prediction
    prediction = data["predictions"][0]
    # Get the description of the location
    description = prediction["description"]
    # Use a simple word embedding model (e.g. word2vec) to get the vector
    # For simplicity, we'll use a pre-trained model from gensim
    from gensim.models import Word2Vec
    model = Word2Vec.load("word2vec_model")
    words = description.split()
    vectors = [model.wv[word] for word in words if word in model.wv]
    if not vectors:
        return None
    vector = np.mean(vectors=vectors, axis=0)
    return vector

# Get word embeddings for a list of locations
locations = ["New York", "London", "Paris", "Tokyo", "Sydney"]
vectors = []
for location in locations:
    vector = get_word_embedding(location)
    if vector is not None:
        vectors.append(vector)

# Apply PCA to reduce dimensionality
pca = PCA(n_components=2)
vectors_pca = pca.fit_transform(vectors)

# Plot word embeddings
plt.figure(figsize=(10, 10))
plt.scatter(vectors_pca[:, 0], vectors_pca[:, 1])
for i, location in enumerate(locations):
    plt.annotate(location, (vectors_pca[i, 0], vectors_pca[i, 1]))
plt.show()