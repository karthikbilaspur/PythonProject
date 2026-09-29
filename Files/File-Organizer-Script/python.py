import os
from sentence_transformers import SentenceTransformer, util
import numpy as np
import shutil
from PIL import Image
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import re

class FileOrganizer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vgg_model = VGG16(weights='imagenet', include_top=True)
        self.text_model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

    def index_files(self, directory):
        self.file_names = []
        self.file_embeddings = []
        self.file_types = []

        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                self.file_names.append(filename)
                self.file_types.append(self.get_file_type(filename))

                if self.file_types[-1] == 'text':
                    embedding = self.model.encode(filename)
                    self.file_embeddings.append(embedding)
                elif self.file_types[-1] == 'image':
                    img_embedding = self.get_image_embedding(os.path.join(directory, filename))
                    self.file_embeddings.append(img_embedding)

    def organize_files(self, directory):
        for i, filename in enumerate(self.file_names):
            if self.file_types[i] == 'text':
                category = self.get_text_category(filename)
            elif self.file_types[i] == 'image':
                category = self.get_image_category(self.file_embeddings[i])

            folder_path = os.path.join(directory, category)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            shutil.move(os.path.join(directory, filename), folder_path)

    def get_file_type(self, filename):
        if filename.endswith('.txt') or filename.endswith('.docx'):
            return 'text'
        elif filename.endswith('.jpg') or filename.endswith('.png'):
            return 'image'
        else:
            return 'unknown'

    def get_image_embedding(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = self.vgg_model.predict(img)
        return features.flatten()

    def get_image_category(self, img_embedding):
        # Use a clustering algorithm or a classification model to categorize images
        # For simplicity, let's use a simple threshold-based approach
        if np.argmax(img_embedding) < 500:
            return 'Animals'
        else:
            return 'Landscapes'

    def get_text_category(self, filename):
        inputs = self.tokenizer(filename, return_tensors='pt')
        outputs = self.text_model(**inputs)
        logits = outputs.logits
        category = torch.argmax(logits).item()
        if category == 0:
            return 'Negative'
        else:
            return 'Positive'

if __name__ == "__main__":
    directory = input("Enter directory path to organize: ")
    file_organizer = FileOrganizer()
    file_organizer.index_files(directory)
    file_organizer.organize_files(directory)