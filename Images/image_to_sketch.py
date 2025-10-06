import cv2
import numpy as np
import os

def load_image(image_path):
 """Loads an image from the specified path."""
 try:
 image = cv2.imread(image_path)
 if image is None:
 raise FileNotFoundError(f"Image not found at path: {image_path}")
 return image
 except Exception as e:
 print(f"Error loading image: {e}")
 return None

def image_to_sketch(image):
 """Converts an image to a sketch."""
 gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 inverted_image = 255 - gray_image
 blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
 sketch = cv2.divide(gray_image, 255 - blurred_image, scale=256)
 return sketch

def display_image(image, window_name):
 """Displays an image in a window."""
 cv2.imshow(window_name, image)
 cv2.waitKey(0)
 cv2.destroyAllWindows()

def save_image(image, filename):
 """Saves an image to a file."""
 try:
 cv2.imwrite(filename, image)
 print("Sketch saved successfully.")
 except Exception as e:
 print(f"Error saving sketch: {e}")

def get_valid_image_path():
 """Gets a valid image path from the user."""
 while True:
 image_path = input("Enter the image path: ")
 if os.path.isfile(image_path):
 return image_path
 else:
 print("Invalid image path. Please try again.")

def get_filename():
 """Gets a filename from the user."""
 while True:
 filename = input("Enter the filename: ")
 if filename:
 return filename
 else:
 print("Filename cannot be empty. Please try again.")

def get_save_confirmation():
 """Gets save confirmation from the user."""
 while True:
 save = input("Do you want to save the sketch? (yes/no): ").lower()
 if save in ['yes', 'no']:
 return save == 'yes'
 else:
 print("Invalid input. Please enter 'yes' or 'no'.")

def main():
 image_path = get_valid_image_path()
 image = load_image(image_path)
 if image is not None:
 sketch = image_to_sketch(image)
 display_image(sketch, 'Sketch')
 if get_save_confirmation():
 filename = get_filename()
 save_image(sketch, filename)

if __name__ == "__main__":
 main()