import os
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class FileOrganizer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_types = {}

    def organize_files(self):
        for filename in os.listdir(self.root_dir):
            file_path = os.path.join(self.root_dir, filename)
            if os.path.isfile(file_path):
                file_type = self.get_file_type(filename)
                if file_type not in self.file_types:
                    self.file_types[file_type] = []
                self.file_types[file_type].append(filename)

        for file_type, files in self.file_types.items():
            dir_path = os.path.join(self.root_dir, file_type)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for file in files:
                shutil.move(os.path.join(self.root_dir, file), dir_path)

    def get_file_type(self, filename):
        # Use AI to determine file type based on content
        # For simplicity, we'll use file extension
        return os.path.splitext(filename)[1][1:]

    def cluster_files(self):
        # Use TF-IDF and cosine similarity to cluster files
        files = []
        for file_type, file_list in self.file_types.items():
            for file in file_list:
                files.append(file)

        vectorizer = TfidfVectorizer(input='filename')
        tfidf_matrix = vectorizer.fit_transform(files)
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Cluster files based on similarity
        clusters = []
        for i in range(len(files)):
            cluster = []
            for j in range(len(files)):
                if similarity_matrix[i][j] > 0.5:
                    cluster.append(files[j])
            clusters.append(cluster)

        return clusters

def main():
    organizer = FileOrganizer('/path/to/root/dir')
    organizer.organize_files()
    clusters = organizer.cluster_files()
    for cluster in clusters:
        print(cluster)

if __name__ == "__main__":
    main()