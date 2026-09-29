# File Search Script Summary

This Python script uses AI and natural language processing to search files in a directory based on semantic similarity. It:
Indexes files in a directory by generating embeddings for file names.
Searches files based on a query by calculating cosine similarity between query and file embeddings.
Returns top N most similar files.
Key Features:
Utilizes sentence transformer models for semantic search
Allows customization for content search and model selection
Provides a basic framework for file search with potential for expansion
Libraries Used:
sentence-transformers
numpy
