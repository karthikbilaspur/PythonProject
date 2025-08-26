from PIL import Image
import glob
import os

def convert_to_gif(image_folder, gif_name, duration, output_folder="output"):
    """
    Convert a series of images in a folder to a GIF.

    Args:
        image_folder (str): Path to the folder containing the images.
        gif_name (str): Name of the output GIF file.
        duration (int): Duration between frames in milliseconds.
        output_folder (str): Folder to save the output GIF. Defaults to "output".
    """
    # Check if the image folder exists
    if not os.path.exists(image_folder):
        print(f"Error: {image_folder} does not exist.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Change the file extension if necessary
    images = glob.glob(image_folder + "/*.jpg") + glob.glob(image_folder + "/*.png")

    if not images:
        print(f"No images found in {image_folder}.")
        return

    frames = []
    for image in images:
        try:
            with Image.open(image) as img:
                frames.append(img.convert("RGBA"))
        except Exception as e:
            print(f"Error processing {image}: {e}")

    if not frames:
        print("No frames to save.")
        return

    output_path = os.path.join(output_folder, gif_name)
    frames[0].save(output_path, format="GIF", append_images=frames[1:],
                   save_all=True, duration=duration, loop=0)
    print(f"GIF created successfully and saved to {output_path}!")


def main():
    image_folder = "Image-Slideshow"  # Path to the folder containing the images
    gif_name = "output.gif"  # Name of the output GIF file
    duration = 500  # Duration between frames in milliseconds

    convert_to_gif(image_folder, gif_name, duration)


if __name__ == "__main__":
    main()