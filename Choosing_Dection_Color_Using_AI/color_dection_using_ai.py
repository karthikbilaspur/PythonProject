import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_colors(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a feature vector
    image = image.reshape((-1, 3))

    # Perform K-means clustering to detect dominant colors
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(image)

    # Get the dominant colors
    colors = kmeans.cluster_centers_

    # Convert the colors to hexadecimal format
    hex_colors = []
    for color in colors:
        hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
        hex_colors.append(hex_color)

    return hex_colors

def main():
    image_path = "image.jpg"
    colors = detect_colors(image_path)
    print("Dominant colors:")
    for i, color in enumerate(colors):
        print(f"Color {i+1}: {color}")

if __name__ == "__main__":
    main()