import cv2
import numpy as np

# Load the video capture device (e.g. a camera)
cap = cv2.VideoCapture('parking_lot.mp4')

# Define the parking space coordinates (x, y, w, h)
parking_spaces = [
    (100, 100, 50, 50),  # Space 1
    (200, 100, 50, 50),  # Space 2
    (300, 100, 50, 50),  # Space 3
    (400, 100, 50, 50),  # Space 4
]

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using the Canny edge detection algorithm
    edges = cv2.Canny(blurred, 50, 150)

    # Iterate over the parking spaces
    for i, (x, y, w, h) in enumerate(parking_spaces):
        # Draw a rectangle around the parking space
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extract the region of interest (ROI) for the parking space
        roi = edges[y:y + h, x:x + w]

        # Count the number of edges in the ROI
        edge_count = np.count_nonzero(roi)

        # If the edge count is below a certain threshold, the space is likely occupied
        if edge_count < 1000:
            cv2.putText(frame, f"Space {i+1}: Occupied", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f"Space {i+1}: Available", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the output
    cv2.imshow('Parking Space Detection', frame)

    # Exit on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all windows
cap.release()
cv2.destroyAllWindows()