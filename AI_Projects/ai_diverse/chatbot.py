import json
import random
import pickle
from pathlib import Path
from typing import Any
import numpy as np
import nltk  # type: ignore[import-not-found]
from nltk.stem import WordNetLemmatizer  # type: ignore[import-not-found]
from tensorflow.keras.models import Sequential  # type: ignore[import-not-found]
from tensorflow.keras.layers import Dense, Dropout  # type: ignore[import-not-found]
from tensorflow.keras.optimizers import SGD  # type: ignore[import-not-found]

# --- Config ---
INTENTS_FILE = Path("intents.json")
WORDS_FILE = Path("words.pkl")
CLASSES_FILE = Path("classes.pkl")
ERROR_THRESHOLD = 0.25

lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

def load_intents() -> dict[str, Any]:
    if not INTENTS_FILE.exists():
        raise FileNotFoundError(f"{INTENTS_FILE} not found")
    return json.loads(INTENTS_FILE.read_text(encoding='utf-8'))

def preprocess_intents(
    intents: dict[str, Any],
) -> tuple[list[str], list[str], list[tuple[list[str], str]]]:
    words: list[str] = []
    classes: list[str] = []
    documents: list[tuple[list[str], str]] = []
    ignore_letters = {'!', '?', '.', ','}

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            tokens: list[str] = nltk.word_tokenize(str(pattern))
            words.extend(tokens)
            documents.append((tokens, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))
    return words, classes, documents

def create_training_data(
    words: list[str],
    classes: list[str],
    documents: list[tuple[list[str], str]],
) -> tuple[np.ndarray, np.ndarray]:
    training: list[tuple[list[int], list[int]]] = []
    output_empty = [0] * len(classes)

    for word_patterns, tag in documents:
        word_patterns = [lemmatizer.lemmatize(w.lower()) for w in word_patterns]
        bag = [1 if w in word_patterns else 0 for w in words]

        output_row = list(output_empty)
        output_row[classes.index(tag)] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    return np.array(train_x), np.array(train_y)

def build_model(input_len: int, output_len: int) -> Any:
    model: Any = Sequential([
        Dense(128, input_shape=(input_len,), activation='relu'),  # type: ignore[call-arg]
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(output_len, activation='softmax')
    ])
    sgd: Any = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

# --- Inference (separated from training) ---
def clean_up_sentence(sentence: str) -> list[str]:
    tokens: list[str] = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(w.lower()) for w in tokens]

def bow(sentence: str, words: list[str]) -> np.ndarray:
    sentence_words = clean_up_sentence(sentence)
    return np.array([1 if w in sentence_words else 0 for w in words])

def predict_class(
    sentence: str, model: Any, words: list[str], classes: list[str]
) -> list[dict[str, str]]:
    p = bow(sentence, words)
    res = model.predict(np.array([p]), verbose=0)[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(ints: list[dict[str, str]], intents_json: dict[str, Any]) -> str:
    if not ints:
        return "I didn't understand that. Could you rephrase?"
    tag = ints[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Sorry, I don't have a response for that."

# --- Training Entry Point ---
if __name__ == "__main__":
    intents = load_intents()
    words, classes, documents = preprocess_intents(intents)

    pickle.dump(words, open(WORDS_FILE, 'wb'))
    pickle.dump(classes, open(CLASSES_FILE, 'wb'))

    train_x, train_y = create_training_data(words, classes, documents)
    model = build_model(len(train_x[0]), len(train_y[0]))
    model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
    model.save("chatbot_model.h5")
    print("Training complete. Model saved.")