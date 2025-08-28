import requests
from geopy.geocoders import Nominatim
import webbrowser

class GeoLocator:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.geolocator = Nominatim(user_agent="geoapiExercises")

    def get_geo_coordinates(self, location):
        try:
            location_obj = self.geolocator.geocode(location)
            if location_obj is not None:
                return location_obj.latitude, location_obj.longitude
            else:
                return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def get_geo_coordinates_using_google_maps_api(self, location):
        if self.api_key is None:
            print("Google Maps API key is not provided.")
            return None
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={self.api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["status"] == "OK":
                latitude = data["results"][0]["geometry"]["location"]["lat"]
                longitude = data["results"][0]["geometry"]["location"]["lng"]
                return latitude, longitude
            else:
                return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def open_location_in_google_maps(self, latitude, longitude):
        url = f"https://www.google.com/maps/place/{latitude},{longitude}"
        webbrowser.open(url)

def main():
    api_key = input("Enter your Google Maps API key (optional): ")
    if api_key.strip() == "":
        api_key = None
    geo_locator = GeoLocator(api_key)
    while True:
        print("\nOptions:")
        print("1. Get geo-coordinates using Nominatim")
        print("2. Get geo-coordinates using Google Maps API")
        print("3. Open location in Google Maps")
        print("4. Quit")
        option = input("Enter your choice: ")
        if option == "1":
            location = input("Enter the location: ")
            geo_coordinates = geo_locator.get_geo_coordinates(location)
            if geo_coordinates is not None:
                print(f"Latitude: {geo_coordinates[0]}")
                print(f"Longitude: {geo_coordinates[1]}")
        elif option == "2":
            location = input("Enter the location: ")
            geo_coordinates = geo_locator.get_geo_coordinates_using_google_maps_api(location)
            if geo_coordinates is not None:
                print(f"Latitude: {geo_coordinates[0]}")
                print(f"Longitude: {geo_coordinates[1]}")
        elif option == "3":
            latitude = float(input("Enter the latitude: "))
            longitude = float(input("Enter the longitude: "))
            geo_locator.open_location_in_google_maps(latitude, longitude)
        elif option == "4":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()