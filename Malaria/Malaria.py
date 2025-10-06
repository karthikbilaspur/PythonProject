import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import tkinter as tk
from tkinter import messagebox

# Sample dataset (replace with your own dataset)
data = {
    "symptoms": ["fever, headache, vomiting", "headache, fatigue", "fever, cough"],
    "malaria": [1, 0, 0]
}

df = pd.DataFrame(data)

# Define a custom dataset class
class SymptomDataset(Dataset):
    def __init__(self, df, tokenizer):
        self.df = df
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        symptoms = self.df.iloc[idx, 0]
        labels = self.df.iloc[idx, 1]

        encoding = self.tokenizer(symptoms, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(labels, dtype=torch.long)
        }

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Prepare dataset and data loader
dataset = SymptomDataset(df, tokenizer)
train_size = int(len(dataset) * 0.8)
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)

# Train the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in train_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs.logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss / len(train_loader)}")

# Evaluate the model
model.eval()
test_loss = 0
correct = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs.logits, labels)
        test_loss += loss.item()
        _, predicted = torch.max(outputs.logits, dim=1)
        correct += (predicted == labels).sum().item()

accuracy = correct / len(test_dataset)
print(f"Test Accuracy: {accuracy:.4f}")

# Use the model in the GUI
class MalariaDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Malaria Detector")

        self.symptom_label = tk.Label(root, text="Enter your symptoms:")
        self.symptom_label.pack()
        self.symptom_entry = tk.Entry(root, width=50)
        self.symptom_entry.pack()

        self.detect_button = tk.Button(root, text="Detect Malaria", command=self.detect_malaria)
        self.detect_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def detect_malaria(self):
        try:
            symptoms = self.symptom_entry.get()
            inputs = tokenizer(symptoms, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
            inputs = {key: value.to(device) for key, value in inputs.items()}
            outputs = model(**inputs)
            logits = outputs.logits
            _, predicted = torch.max(logits, dim=1)
            result = "Malaria detected" if predicted.item() == 1 else "No malaria detected"
            self.result_label.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MalariaDetector(root)
    root.mainloop()