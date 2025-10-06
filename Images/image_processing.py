import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_image()

    def load_image(self):
        try:
            return cv2.imread(self.image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def display_images(self, images):
        for title, image in images.items():
            cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convert_to_grayscale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def apply_blur(self):
        return cv2.GaussianBlur(self.image, (5, 5), 0)

    def apply_edge_detection(self):
        return cv2.Canny(self.image, 100, 200)

    def save_images(self, images):
        for title, image in images.items():
            cv2.imwrite(f"{title.lower().replace(' ', '_')}.jpg", image)

    def process_images(self):
        if self.image is None:
            return

        gray_image = self.convert_to_grayscale()
        blurred_image = self.apply_blur()
        edges = self.apply_edge_detection()

        images = {
            "Original Image": self.image,
            "Grayscale Image": gray_image,
            "Blurred Image": blurred_image,
            "Edges": edges
        }

        self.display_images(images)
        self.save_images(images)

def main():
    image_path = input("Enter the image path: ")
    processor = ImageProcessor(image_path)
    processor.process_images()

if __name__ == "__main__":
    main()