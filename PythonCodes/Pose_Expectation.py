import cv2
import mediapipe as mp
import numpy as np
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False, model_complexity=2)

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)

def track_joint_movement(results):
    left_shoulder = [results.pose_landmarks.landmark[11].x, results.pose_landmarks.landmark[11].y]
    right_shoulder = [results.pose_landmarks.landmark[12].x, results.pose_landmarks.landmark[12].y]
    left_elbow = [results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y]
    right_elbow = [results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y]
    left_wrist = [results.pose_landmarks.landmark[15].x, results.pose_landmarks.landmark[15].y]
    right_wrist = [results.pose_landmarks.landmark[16].x, results.pose_landmarks.landmark[16].y]
    
    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    
    return left_angle, right_angle

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            left_angle, right_angle = track_joint_movement(results)
            cv2.putText(img, f"Left Angle: {int(left_angle)}", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
            cv2.putText(img, f"Right Angle: {int(right_angle)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
            
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)
                cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()