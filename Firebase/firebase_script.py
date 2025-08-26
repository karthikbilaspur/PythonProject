import firebase_admin
from firebase_admin import credentials, db, firestore
import requests
import json

# Initialize Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com',
    'projectId': 'your-project-id',
})

# Function to generate random user data
def get_random_user():
    response = requests.get('https://randomuser.me/api/')
    data = json.loads(response.text)
    return data['results'][0]

# Realtime Database
def add_user_to_realtime_db(user_data):
    ref = db.reference('users')
    ref.push({
        'name': user_data['name']['first'] + ' ' + user_data['name']['last'],
        'email': user_data['email']
    })

# Firestore
def add_user_to_firestore(user_data):
    db_fs = firestore.client()
    doc_ref = db_fs.collection('users').document()
    doc_ref.set({
        'name': user_data['name']['first'] + ' ' + user_data['name']['last'],
        'email': user_data['email']
    })

# Get random user data and add to databases
user_data = get_random_user()
add_user_to_realtime_db(user_data)
add_user_to_firestore(user_data)

# Get data from Firestore
db_fs = firestore.client()
docs = db_fs.collection('users').stream()
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    