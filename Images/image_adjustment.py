import cv2
import numpy as np

def load_image(image_path):
    """Loads an image from the specified path."""
    return cv2.imread(image_path)

def adjust_contrast(image, alpha, beta):
    """
    Adjusts the contrast of the image.

    Args:
        image: The input image.
        alpha: Contrast control (1.0-3.0).
        beta: Brightness control (0-100).

    Returns:
        The contrast-adjusted image.
    """
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb_image)
    y_contrasted = cv2.convertScaleAbs(y, alpha=alpha, beta=beta)
    contrasted_ycrcb_image = cv2.merge([y_contrasted, cr, cb])
    return cv2.cvtColor(contrasted_ycrcb_image, cv2.COLOR_YCrCb2BGR)

def display_images(original_image, contrasted_image):
    """Displays the original and contrast-adjusted images."""
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Contrasted Image', contrasted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(image, output_path):
    """Saves the image to the specified path."""
    cv2.imwrite(output_path, image)

def main():
    image_path = 'image.jpg'
    output_path = 'contrasted_image.jpg'
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)

    original_image = load_image(image_path)
    if original_image is None:
        print("Error: Could not load image.")
        return

    contrasted_image = adjust_contrast(original_image, alpha, beta)
    display_images(original_image, contrasted_image)
    save_image(contrasted_image, output_path)

if __name__ == "__main__":
    main()