import csv
from gmplot import gmplot

def get_csv_path():
    return input("Enter the path of your CSV file (with filename and extension): ")

def get_zoom_level():
    while True:
        try:
            return int(input("Enter your zoom level (less value zooms out, large value zooms in): "))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def calculate_center(csv_path):
    x, y = 0, 0
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            try:
                lat, long = float(row[0]), float(row[1])
                x += lat
                y += long
                count += 1
            except (IndexError, ValueError):
                print(f"Skipping invalid row: {row}")
    if count == 0:
        raise ValueError("No valid coordinates found in the CSV file.")
    return x / count, y / count

def plot_map(csv_path, zoom):
    center_lat, center_long = calculate_center(csv_path)
    gmap = gmplot.GoogleMapPlotter(center_lat, center_long, zoom)

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        k = 0
        for row in reader:
            try:
                lat, long = float(row[0]), float(row[1])
                if k == 0:
                    gmap.marker(lat, long, 'green')
                    k = 1
                else:
                    gmap.marker(lat, long, 'blue')
                    k = 0
            except (IndexError, ValueError):
                print(f"Skipping invalid row: {row}")

    gmap.draw("Output.html")
    print("Done! Check file Output.html")

def main():
    csv_path = get_csv_path()
    zoom = get_zoom_level()
    plot_map(csv_path, zoom)

if __name__ == "__main__":
    main()