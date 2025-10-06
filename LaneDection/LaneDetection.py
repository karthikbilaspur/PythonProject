import cv2
import numpy as np

def detect_lanes(image):
    """
    Detect lanes in an image.

    Args:
        image: Input image.

    Returns:
        Image with detected lanes.
    """
    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Define ROI
    height, width = edges.shape
    roi_vertices = np.array([[(0, height), (width / 2, height / 2), (width, height)]], dtype=np.int32)
    roi = cv2.bitwise_and(edges, cv2.fillPoly(np.zeros_like(edges), roi_vertices, 255))

    # Hough transform to detect lines
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)

    # Draw detected lines
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Combine original image with detected lines
    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)

    return result

def detect_lanes_video(video_path):
    """
    Detect lanes in a video.

    Args:
        video_path: Path to the video file.
    """
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        lanes_image = detect_lanes(frame)
        cv2.imshow('Lanes', lanes_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'path_to_your_video.mp4'
detect_lanes_video(video_path)