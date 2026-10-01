import cv2
import numpy as np

def blur_image(image, blur_type):
    """
    Blur an image using OpenCV.

    Args:
        image (numpy array): Input image.
        blur_type (str): Type of blur to apply (average, gaussian, median).

    Returns:
        numpy array: Blurred image.
    """
    if blur_type == "average":
        blurred_image = cv2.blur(image, (5, 5))
    elif blur_type == "gaussian":
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    elif blur_type == "median":
        blurred_image = cv2.medianBlur(image, 5)
    else:
        raise ValueError("Invalid blur type")

    return blurred_image

def main():
    # Load image
    image_path = "image.jpg"  # replace with your image path
    image = cv2.imread(image_path)

    # Blur image
    blur_type = "gaussian"  # choose from "average", "gaussian", "median"
    blurred_image = blur_image(image, blur_type)

    # Display original and blurred images
    cv2.imshow("Original", image)
    cv2.imshow("Blurred Image", blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save blurred image
    cv2.imwrite("blurred_image.jpg", blurred_image)

if __name__ == "__main__":
    main()