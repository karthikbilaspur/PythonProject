import cv2
import numpy as np

def bleed_image(image, bleed_amount):
    """
    Apply bleeding effect to an image.

    Args:
        image (numpy array): Input image.
        bleed_amount (int): Amount of bleeding to apply.

    Returns:
        numpy array: Image with bleeding effect.
    """
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Increase saturation to create bleeding effect
    hsv[..., 1] = np.clip(hsv[..., 1].astype(np.int16) + bleed_amount, 0, 255).astype(np.uint8)

    # Convert back to BGR color space
    bled_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return bled_image

def main():
    # Load image
    image_path = "jupiter_giant_red_spot.jpg"  # replace with your image path
    image = cv2.imread(image_path)

    # Apply bleeding effect
    bleed_amount = 50
    bled_image = bleed_image(image, bleed_amount)

    # Display original and bled images
    cv2.imshow("Original", image)
    cv2.imshow("Bled Image", bled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save bled image
    cv2.imwrite("bled_jupiter_giant_red_spot.jpg", bled_image)

if __name__ == "__main__":
    main()