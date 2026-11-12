from PIL import Image
import glob
import os
from typing import cast

# Pillow changed the resampling constants location in newer versions.
# Keep compatibility with both old and new installations.
LANCZOS = cast(int, getattr(getattr(Image, "Resampling", Image), "LANCZOS"))

def convert_to_gif(
    image_folder: str,
    gif_name: str,
    duration: int = 500,
    output_folder: str = "output",
    max_size: tuple[int, int] = (800, 800),
) -> None:
    """
    Convert a series of images in a folder to a GIF.

    Args:
        image_folder (str): Path to the folder containing the images.
        gif_name (str): Name of the output GIF file.
        duration (int): Duration between frames in milliseconds.
        output_folder (str): Folder to save the output GIF.
        max_size (tuple): Max (width, height) to resize frames to.
    """
    if not os.path.exists(image_folder):
        print(f"Error: {image_folder} does not exist.")
        return

    os.makedirs(output_folder, exist_ok=True)

    # Sorted so frames play in order: 1, 2, 3... not 1, 10, 2
    images = sorted(
        glob.glob(os.path.join(image_folder, "*.jpg")) +
        glob.glob(os.path.join(image_folder, "*.jpeg")) +
        glob.glob(os.path.join(image_folder, "*.png"))
    )

    if not images:
        print(f"No images found in {image_folder}.")
        return

    frames: list[Image.Image] = []
    base_size = None

    for image_path in images:
        try:
            with Image.open(image_path) as img:
                # Handle transparency by compositing on white
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert("RGB")

                # Use first image as canonical size, resize rest to match
                if base_size is None:
                    base_size = img.size
                    # Optional: downscale if too big
                    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                        img.thumbnail(max_size, LANCZOS)
                        base_size = img.size
                else:
                    img = img.resize(base_size, LANCZOS)

                frames.append(img.copy())
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    if not frames:
        print("No frames to save.")
        return

    output_path = os.path.join(output_folder, gif_name)
    frames[0].save(
        output_path,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0,
        optimize=True
    )
    print(f"GIF created successfully and saved to {output_path}!")

def main():
    convert_to_gif(
        image_folder="Image-Slideshow",
        gif_name="output.gif",
        duration=500
    )

if __name__ == "__main__":
    main()