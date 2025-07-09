import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import spacy

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Load data from intents.json
data_file = open('intents.json').read()
intents = json.loads(data_file)

words = []
classes = []
documents = []
ignore_letters = ['!', '?', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc¹)] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] 
    results.sort(key=lambda x: x¹, reverse=True) 
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r¹)})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents_tag = intents_json['intents']
    for i in list_of_intents_tag:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    doc = nlp(msg)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print("Entities:", entities)
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

import tkinter as tk
from tkinter import *

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")
ChatLog.config(state=DISABLED)
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)
base.mainloop()