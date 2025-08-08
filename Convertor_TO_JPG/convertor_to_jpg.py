from PIL import Image
import os

def convert_to_jpg(input_file, output_file):
    """
    Convert an image to JPG format.

    Args:
        input_file (str): Path to the input image file.
        output_file (str): Path to the output JPG file.
    """
    try:
        # Open the image file
        img = Image.open(input_file)

        # Convert the image to RGB mode (JPG doesn't support alpha channel)
        img = img.convert('RGB')

        # Save the image as JPG
        img.save(str(output_file), 'JPEG')
        print(f"Image converted and saved as {output_file}")

    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    # Get the input file path from the user
    input_file = input("Enter the input image file path: ")

    # Get the output file path from the user
    output_file = input("Enter the output JPG file path: ")

    # Check if the output file path has a .jpg extension
    if not output_file.endswith('.jpg'):
        output_file += '.jpg'

    # Convert the image to JPG
    convert_to_jpg(input_file, output_file)

if __name__ == "__main__":
    main()