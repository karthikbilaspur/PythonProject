# Summary

This Python program uses the Pillow library to convert images to JPG format. Here's a step-by-step breakdown:
The program asks the user for the input image file path and the output JPG file path.
It checks if the output file path has a .jpg extension and adds it if necessary.
The convert_to_jpg function opens the input image file, converts it to RGB mode (since JPG doesn't support alpha channels), and saves it as a JPG file.
If any errors occur during the conversion process, the program prints an error message.
Requirements
Python 3.x
Pillow library (pip install pillow)
Usage
Save this code in a file (e.g., image_converter.py).
Run the program using Python (e.g., python image_converter.py).
