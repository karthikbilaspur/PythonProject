from PIL import Image
import os

class ImageProcessor:
    def __init__(self, input_image):
        self.input_image = input_image
        self.image = None

    def open_image(self):
        try:
            self.image = Image.open(self.input_image)
        except Exception as e:
            print(f"Error opening image: {e}")
            return False
        return True

    def resize_image(self, output_image, new_size):
        if not self.image:
            print("Image not opened.")
            return
        try:
            resized_image = self.image.resize(new_size)
            resized_image.save(output_image)
            print("Image resized and saved successfully.")
        except Exception as e:
            print(f"Error resizing image: {e}")

    def rotate_image(self, output_image, degrees):
        if not self.image:
            print("Image not opened.")
            return
        try:
            rotated_image = self.image.rotate(degrees)
            rotated_image.save(output_image)
            print("Image rotated and saved successfully.")
        except Exception as e:
            print(f"Error rotating image: {e}")

    def flip_image(self, output_image, flip_mode):
        if not self.image:
            print("Image not opened.")
            return
        try:
            flipped_image = self.image.transpose(flip_mode)
            flipped_image.save(output_image)
            print("Image flipped and saved successfully.")
        except Exception as e:
            print(f"Error flipping image: {e}")


def main():
    input_file = 'input_image.jpg'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    resized_file = os.path.join(output_dir, 'resized_image.jpg')
    rotated_file = os.path.join(output_dir, 'rotated_image.jpg')
    flipped_file = os.path.join(output_dir, 'flipped_image.jpg')

    new_size = (800, 600)
    degrees_to_rotate = 90
    flip_mode = Image.FLIP_LEFT_RIGHT

    processor = ImageProcessor(input_file)
    if processor.open_image():
        processor.resize_image(resized_file, new_size)
        processor.rotate_image(rotated_file, degrees_to_rotate)
        processor.flip_image(flipped_file, flip_mode)


if __name__ == "__main__":
    main()