import cv2
import numpy as np

def detect_blobs(image):
    """
    Detect blobs in an image using OpenCV's SimpleBlobDetector.

    Args:
        image (numpy array): Input image.

    Returns:
        list: List of keypoints (blobs) detected in the image.
    """
    # Create a SimpleBlobDetector object
    params = cv2.SimpleBlobDetector_Params()

    # Set blob detection parameters
    params.minThreshold = 10
    params.maxThreshold = 200
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 1000
    params.filterByCircularity = True
    params.minCircularity = 0.5
    params.filterByConvexity = True
    params.minConvexity = 0.5
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(image)

    return keypoints

def main():
    # Load image
    image_path = "image.jpg"  # replace with your image path
    image = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect blobs
    keypoints = detect_blobs(gray)

    # Draw detected blobs
    image_with_blobs = cv2.drawKeypoints(image, keypoints, None, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display image with blobs
    cv2.imshow("Blobs", image_with_blobs)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()