import cv2

# List all available cameras
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is available")
        cap.release()

# Open the camera
camera_index = int(input("Enter the camera index: "))
cap = cv2.VideoCapture(camera_index)

while True:
    ret, frame = cap.read()
    cv2.imshow('Press "c" to capture, "q" to quit', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        cv2.imwrite('image.jpg', frame)
        print("Image captured and saved as image.jpg")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()