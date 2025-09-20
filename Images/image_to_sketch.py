import cv2
import numpy as np

def image_to_sketch(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_image = 255 - gray_image

    # Blur the inverted image
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)

    # Draw the sketch
    sketch = cv2.divide(gray_image, 255 - blurred_image, scale=256)

    return sketch

def main():
    image_path = input("Enter the image path: ")
    sketch = image_to_sketch(image_path)

    # Display the sketch
    cv2.imshow('Sketch', sketch)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the sketch
    save = input("Do you want to save the sketch? (yes/no): ")
    if save.lower() == 'yes':
        filename = input("Enter the filename: ")
        cv2.imwrite(filename, sketch)
        print("Sketch saved successfully.")

if __name__ == "__main__":
    main()