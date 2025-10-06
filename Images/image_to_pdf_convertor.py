from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, asksaveasfilename
import os

def image_to_pdf(image_paths, output_path, quality=100):
    try:
        images = [Image.open(image_path).convert('RGB') for image_path in image_paths]
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            quality=quality,
            optimize=True
        )
    except Exception as e:
        print(f"Error occurred during PDF conversion: {e}")

def validate_image_files(image_paths):
    valid_image_paths = []
    for image_path in image_paths:
        try:
            Image.open(image_path)
            valid_image_paths.append(image_path)
        except Exception as e:
            print(f"Skipping invalid image file: {image_path}")
    return valid_image_paths

def get_quality_setting():
    while True:
        quality = input("Enter image quality (1-100, default=100): ")
        if quality:
            try:
                quality = int(quality)
                if quality < 1 or quality > 100:
                    print("Invalid quality value. Please enter a value between 1 and 100.")
                else:
                    return quality
            except ValueError:
                print("Invalid quality value. Please enter a number.")
        else:
            return 100

def main():
    Tk().withdraw()
    while True:
        print("\nOptions:")
        print("1. Select images and convert to PDF")
        print("2. Quit")
        option = input("Choose an option: ")

        if option == "1":
            image_paths = askopenfilenames(
                title="Select Images",
                filetypes=[("Image Files", ".png .jpg .jpeg .bmp .gif")]
            )

            if not image_paths:
                print("No images selected.")
                continue

            image_paths = validate_image_files(image_paths)

            output_path = asksaveasfilename(
                title="Save PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", ".pdf")]
            )

            if not output_path:
                print("No output file selected.")
                continue

            quality = get_quality_setting()

            image_to_pdf(image_paths, output_path, quality)
            print(f"PDF saved as {output_path}")

        elif option == "2":
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()