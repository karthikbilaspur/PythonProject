import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

class FileSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.file_names = []
        self.file_embeddings = []

    def index_files(self, directory):
        """Index files in the given directory."""
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                self.file_names.append(filename)
                # Use filename for embedding, you can also read file content if needed
                embedding = self.model.encode(filename)
                self.file_embeddings.append(embedding)

    def search_files(self, query, top_n=5):
        """Search files based on the query."""
        query_embedding = self.model.encode(query)
        similarities = util.cos_sim(query_embedding, self.file_embeddings)[0]
        top_indices = np.argsort(-similarities)[:top_n]
        
        results = [(self.file_names[i], similarities[i]) for i in top_indices]
        return results

if __name__ == "__main__":
    directory = input("Enter directory path to index: ")
    search_query = input("Enter search query: ")

    file_search = FileSearch()
    file_search.index_files(directory)
    results = file_search.search_files(search_query)

    print("Search Results:")
    for file, similarity in results:
        print(f"{file}: {similarity:.4f}")