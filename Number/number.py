import cv2
import numpy as np

# Define constants
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MIN_AREA = 500
COLOR = (255, 0, 255)

# Load the cascade classifier
nPlateCascade = cv2.CascadeClassifier(
    'res/haarcascade_russian_plate_number.xml')

# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
cap.set(10, 150)

# Initialize the count
count = 0

while True:
    # Read a frame from the video capture
    success, img = cap.read()
    
    if not success:
        break

    # Convert the frame to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect number plates
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)

    # Draw rectangles around the number plates
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > MIN_AREA:
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR, 2)
            cv2.putText(img, "Number Plate", (x, y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, COLOR, 2)
            imgRoi = img[y:y+h, x:x+w]
            cv2.imshow("ROI", imgRoi)

    # Display the output
    cv2.imshow("Result", img)

    # Save the number plate image when 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        if 'imgRoi' in locals():
            cv2.imwrite('res/scanned/NoPlate_' + str(count) + '.jpg', imgRoi)
            cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, 'Scan Saved', (150, 265),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
            cv2.imshow("Result", img)
            cv2.waitKey(500)
            count += 1
        else:
            print("No number plate detected.")

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()