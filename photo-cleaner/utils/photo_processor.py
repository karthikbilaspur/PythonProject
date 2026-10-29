import cv2
import os
import shutil
from typing import Any, TypedDict


class PhotoAssessment(TypedDict):
    has_face: bool
    eyes_open: bool
    is_best: bool
    reason: str

# Safe processor - uses OpenCV only, no scraping
# For production, replace detect with face_recognition or mediapipe for better accuracy

opencv: Any = cv2  # OpenCV's Python bindings may not include type information.
face_cascade = opencv.CascadeClassifier(opencv.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = opencv.CascadeClassifier(opencv.data.haarcascades + 'haarcascade_eye.xml')

def is_good_photo(image_path: str) -> PhotoAssessment:
    """Returns dict: has_face, eyes_open, is_best"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"has_face": False, "eyes_open": False, "is_best": False, "reason": "Invalid image"}
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60,60))
        
        if len(faces) == 0:
            return {"has_face": False, "eyes_open": False, "is_best": False, "reason": "No face"}
        
        # Check eyes for first face
        (x,y,w,h) = faces[0]
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        eyes_open = len(eyes) >= 1
        
        is_best = eyes_open and len(faces) >= 1
        return {
            "has_face": True, 
            "eyes_open": eyes_open, 
            "is_best": is_best,
            "reason": "Best" if is_best else "Eyes closed or blurry"
        }
    except Exception as e:
        return {"has_face": False, "eyes_open": False, "is_best": False, "reason": str(e)}

def process_folder(
    input_folder: str,
    best_folder: str,
    user_id: Any,
    db: Any,
    PhotoJob: Any,
) -> list[dict[str, Any]]:
    os.makedirs(best_folder, exist_ok=True)
    results = []
    for fname in os.listdir(input_folder):
        fpath = os.path.join(input_folder, fname)
        if not os.path.isfile(fpath):
            continue
        if not fname.lower().endswith(('.jpg','.jpeg','.png')):
            continue
        
        res = is_good_photo(fpath)
        job_result = "BEST" if res["is_best"] else ("NO_FACE" if not res["has_face"] else "REJECTED")
        
        # Save to DB
        job = PhotoJob(user_id=user_id, filename=fname, result=job_result, emotion=res["reason"])
        db.session.add(job)
        
        if res["is_best"]:
            shutil.copy(fpath, os.path.join(best_folder, fname))
        
        results.append({"filename": fname, **res, "job_result": job_result})
    
    db.session.commit()
    return results
