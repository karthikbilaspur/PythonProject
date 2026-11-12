
"""
Your Own Travel Map App
Python + Flask + Leaflet + Nominatim (OpenStreetMap)
- Add places YOU have visited
- Geocodes with Nominatim (free, no API key)
- Saves to places.json (your own data)
- Shows all on interactive map
Run: pip install flask geopy
     python app.py
Then open http://127.0.0.1:5000
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import json, os, time

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "places.json")
geolocator = Nominatim(user_agent="my_travel_map_app_v1")

def load_places():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_places(places):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(places, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    places = load_places()
    return render_template("index.html", places=places, count=len(places))

@app.route("/api/places")
def api_places():
    return jsonify(load_places())

@app.route("/add", methods=["POST"])
def add_place():
    name = request.form.get("name", "").strip()
    notes = request.form.get("notes", "").strip()
    date_visited = request.form.get("date_visited", "").strip()
    category = request.form.get("category", "Visited").strip() or "Visited"

    if not name:
        return redirect(url_for("index"))

    # Geocode - respect Nominatim rate limit
    try:
        time.sleep(1)
        loc = geolocator.geocode(name)
    except (GeocoderTimedOut, GeocoderUnavailable):
        loc = None

    if not loc:
        return render_template("index.html", places=load_places(), count=len(load_places()), error=f"Could not find '{name}'. Try a more specific name like 'Lalbagh, Bangalore'")

    places = load_places()
    new_place = {
        "id": int(time.time()*1000),
        "name": name,
        "display_name": loc.address,
        "notes": notes,
        "date_visited": date_visited,
        "category": category,
        "lat": loc.latitude,
        "lng": loc.longitude
    }
    places.append(new_place)
    save_places(places)
    return redirect(url_for("index"))

@app.route("/delete/<int:place_id>", methods=["POST"])
def delete_place(place_id):
    places = [p for p in load_places() if p["id"] != place_id]
    save_places(places)
    return redirect(url_for("index"))

@app.route("/export")
def export():
    return jsonify(load_places())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
