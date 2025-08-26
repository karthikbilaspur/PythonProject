import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load the CascadeClassifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Load the facial recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Load the facial expression analysis model
expression_model = load_model('expression_model.h5')

def detect_faces_in_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Recognize the face
        id, confidence = recognizer.predict(roi_gray)
        if confidence < 50:
            cv2.putText(img, f"ID: {id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        else:
            cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Detect eyes in the face
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        # Detect smile in the face
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)

        # Analyze facial expression
        roi = cv2.resize(roi_color, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        prediction = expression_model.predict(roi)
        expression = np.argmax(prediction)
        if expression == 0:
            cv2.putText(img, "Angry", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 1:
            cv2.putText(img, "Disgust", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 2:
            cv2.putText(img, "Fear", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 3:
            cv2.putText(img, "Happy", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 4:
            cv2.putText(img, "Neutral", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 5:
            cv2.putText(img, "Sad", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        elif expression == 6:
            cv2.putText(img, "Surprise", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Display the output
    cv2.imshow('Faces', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_faces_from_camera():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Recognize the face
            id, confidence = recognizer.predict(roi_gray)
            if confidence < 50:
                cv2.putText(frame, f"ID: {id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            # Detect eyes in the face
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

            # Detect smile in the face
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)

            # Analyze facial expression
            roi = cv2.resize(roi_color, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            prediction = expression_model.predict(roi)
            expression = np.argmax(prediction)
            if expression == 0:
                cv2.putText(frame, "Angry", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 1:
                cv2.putText(frame, "Disgust", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 2:
                cv2.putText(frame, "Fear", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 3:
                cv2.putText(frame, "Happy", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 4:
                cv2.putText(frame, "Neutral", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 5:
                cv2.putText(frame, "Sad", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            elif expression == 6:
                cv2.putText(frame, "Surprise", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Display the output
        cv2.imshow('Faces', frame)

        # Exit on key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Face Detection Options:")
    print("1. Detect faces in an image")
    print("2. Detect faces from camera")
    option = input("Enter your option: ")

    if option == "1":
        image_path = input("Enter the image path: ")
        detect_faces_in_image(image_path)
    elif option == "2":
        detect_faces_from_camera()
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()