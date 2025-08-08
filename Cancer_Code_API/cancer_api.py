import requests
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app, logging=True)

# API endpoint for hospital listings
hospital_api_endpoint = "https://api.data.gov.in/resource/99808f6e-da80-43f8-bafd-87d645a414a8?api-key=YOUR_API_KEY&format=json&offset=0&limit=100"

# API endpoint for cancer statistics
cancer_api_endpoint = "https://example.com/cancer-statistics"

# Initialize logger
logging.basicConfig(level=logging.INFO)

def fetch_hospitals():
    try:
        response = requests.get(hospital_api_endpoint)
        response.raise_for_status()
        data = json.loads(response.text)
        hospitals = data["records"]
        return hospitals
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching hospitals: {e}")
        return []

def fetch_cancer_stats():
    try:
        response = requests.get(cancer_api_endpoint)
        response.raise_for_status()
        data = json.loads(response.text)
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching cancer statistics: {e}")
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('update', {'data': 'Connected'})

@socketio.on('update')
def handle_update():
    # Fetch latest cancer statistics and hospital listings
    cancer_stats = fetch_cancer_stats()
    hospitals = fetch_hospitals()
    emit('update', {'cancer_stats': cancer_stats, 'hospitals': hospitals})

@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = fetch_hospitals()
    return render_template('hospitals.html', hospitals=hospitals)

@app.route('/cancer-stats', methods=['GET'])
def get_cancer_stats():
    cancer_stats = fetch_cancer_stats()
    return render_template('cancer_stats.html', cancer_stats=cancer_stats)

@app.route('/search', methods=['POST'])
def search_hospitals():
    query = request.form.get('query', '')
    hospitals = fetch_hospitals()
    search_results = [hospital for hospital in hospitals if query.lower() in hospital.get('hospital_name', '').lower()]
    return render_template('search_results.html', search_results=search_results)

@app.route('/api/hospitals', methods=['GET'])
def get_hospitals_api():
    hospitals = fetch_hospitals()
    return jsonify(hospitals)

@app.route('/api/cancer-stats', methods=['GET'])
def get_cancer_stats_api():
    cancer_stats = fetch_cancer_stats()
    return jsonify(cancer_stats)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    socketio.run(app)