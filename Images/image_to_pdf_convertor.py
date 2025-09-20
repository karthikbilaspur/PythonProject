from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, asksaveasfilename
import os

def image_to_pdf(image_paths, output_path, quality=100):
    images = []
    for image_path in image_paths:
        image = Image.open(image_path)
        images.append(image.convert('RGB'))

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        quality=quality,
        optimize=True
    )

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

            output_path = asksaveasfilename(
                title="Save PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", ".pdf")]
            )

            if not output_path:
                print("No output file selected.")
                continue

            quality = input("Enter image quality (1-100, default=100): ")
            if quality:
                try:
                    quality = int(quality)
                    if quality < 1 or quality > 100:
                        print("Invalid quality value. Using default value of 100.")
                        quality = 100
                except ValueError:
                    print("Invalid quality value. Using default value of 100.")
                    quality = 100
            else:
                quality = 100

            try:
                image_to_pdf(image_paths, output_path, quality)
                print(f"PDF saved as {output_path}")
            except Exception as e:
                print(f"Error occurred: {e}")

        elif option == "2":
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()