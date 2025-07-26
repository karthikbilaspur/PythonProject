import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    # Remove punctuation
    sentences = [sentence.replace(".", "").replace(",", "").replace("!", "").replace("?", "") for sentence in sentences]
    return sentences

def create_bag_of_words(sentences):
    # Create a CountVectorizer object
    count_vectorizer = CountVectorizer()
    # Fit and transform the sentences
    bow = count_vectorizer.fit_transform(sentences)
    return bow, count_vectorizer

def create_dataframe(bow, count_vectorizer):
    # Convert the Bag of Words matrix to a numpy array
    bow_array = bow.toarray()
    # Create a pandas DataFrame
    df = pd.DataFrame(bow_array, columns=count_vectorizer.get_feature_names_out())
    return df

def main():
    # Get user input
    text = input("Enter your text: ")
    # Preprocess the text
    sentences = preprocess_text(text)
    print("Preprocessed Sentences:")
    print(sentences)
    # Create the Bag of Words model
    bow, count_vectorizer = create_bag_of_words(sentences)
    print("Bag of Words Matrix:")
    print(bow.toarray())
    print("Vocabulary:")
    print(count_vectorizer.vocabulary_)
    print("Features:")
    print(count_vectorizer.get_feature_names_out())
    # Create a DataFrame
    df = create_dataframe(bow, count_vectorizer)
    print("DataFrame:")
    print(df)
    # Export to Excel
    df.to_excel('./bag_of_words.xlsx', sheet_name='data', index=False)

if __name__ == "__main__":
    main()