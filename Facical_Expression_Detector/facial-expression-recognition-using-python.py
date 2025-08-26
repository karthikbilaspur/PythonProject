
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def load_facial_expression_model(model_path):
    try:
        model = load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def detect_faces(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return faces

def predict_facial_expression(model, face_roi):
    try:
        prediction = model.predict(face_roi)
        expression_index = np.argmax(prediction)
        return expression_index
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None

def main():
    model_path = 'facial_expression_model.h5'
    model = load_facial_expression_model(model_path)
    if model is None:
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    expressions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        faces = detect_faces(frame, face_cascade)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            face_roi = frame[y:y+h, x:x+w]
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            face_roi = cv2.resize(face_roi, (48, 48))
            face_roi = face_roi.astype('float32') / 255
            face_roi = np.expand_dims(face_roi, axis=0)
            face_roi = np.expand_dims(face_roi, axis=-1)
            
            expression_index = predict_facial_expression(model, face_roi)
            if expression_index is not None and expression_index < len(expressions):
                expression = expressions[expression_index]
                cv2.putText(frame, expression, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        cv2.imshow('Facial Expression Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()