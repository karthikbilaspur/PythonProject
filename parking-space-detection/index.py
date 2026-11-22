import cv2
import numpy as np
from numpy.typing import NDArray
from typing import cast
from collections import deque

# -------------------- Tunable parameters --------------------
VIDEO_PATH = "parking_lot.mp4"

# (x, y, w, h) - top-left + size. Tune these for YOUR video.
# Tip: run once with DEBUG=True to see coordinates, or use the
# mouse callback in pick_spaces.py style tools to click boxes.
PARKING_SPACES = [
    (100, 100, 50, 50),  # Space 1
    (200, 100, 50, 50),  # Space 2
    (300, 100, 50, 50),  # Space 3
    (400, 100, 50, 50),  # Space 4
]

# Edge density = edge_pixels / roi_area. Above this -> Occupied.
# Start here and tune: empty asphalt ~0.01-0.05, car ~0.10-0.30.
# Depends on lighting / camera / Canny thresholds.
EDGE_DENSITY_THRESHOLD = 0.08

# Debounce: status flips only after this many consecutive frames agree.
# 5 frames @ 30fps ~= 0.16s - kills flicker without feeling laggy.
STABLE_FRAMES = 5

CANNY_LOW, CANNY_HIGH = 50, 150
BLUR_KERNEL = (5, 5)
LOOP_VIDEO = True  # Set False to exit at end of file.


def edge_density(edges: NDArray[np.uint8], x: int, y: int, w: int, h: int) -> float:
    """Edge pixels / ROI area, with ROI clipped to frame bounds."""
    fh, fw = edges.shape[:2]
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(fw, x + w), min(fh, y + h)
    if x2 <= x1 or y2 <= y1:
        return 0.0  # ROI completely outside frame
    roi = edges[y1:y2, x1:x2]
    area = roi.size
    if area == 0:
        return 0.0
    return float(np.count_nonzero(roi)) / float(area)


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"ERROR: Could not open video '{VIDEO_PATH}'.")
        print("Check the filename / path, and that the file exists.")
        return

    # Per-space state: current displayed status + history for debouncing.
    # history[i] holds last STABLE_FRAMES raw decisions (True=occupied).
    histories: list[deque[bool]] = [deque(maxlen=STABLE_FRAMES) for _ in PARKING_SPACES]
    statuses = [False] * len(PARKING_SPACES)  # False = Available, True = Occupied

    while True:
        ret, frame = cap.read()
        if not ret:
            if LOOP_VIDEO:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            print("End of video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
        edges = cv2.Canny(blurred, CANNY_LOW, CANNY_HIGH)

        free_count = 0

        for i, (x, y, w, h) in enumerate(PARKING_SPACES):
            density = edge_density(edges, x, y, w, h)
            raw_occupied = density > EDGE_DENSITY_THRESHOLD

            # --- Debounce: only flip after STABLE_FRAMES agree ---
            histories[i].append(raw_occupied)
            if len(histories[i]) == STABLE_FRAMES:
                # All recent frames agree -> adopt new status.
                if all(histories[i]):
                    statuses[i] = True
                elif not any(histories[i]):
                    statuses[i] = False
                # Mixed history -> keep previous status (don't flicker).

            occupied = statuses[i]
            if not occupied:
                free_count += 1

            # --- Draw ---
            color = (0, 0, 255) if occupied else (0, 255, 0)  # BGR
            label = f"Space {i+1}: {'Occupied' if occupied else 'Available'}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            # Text with black background so it stays readable.
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (x, y - th - 12), (x + tw + 4, y - 2), (0, 0, 0), -1)
            cv2.putText(frame, label, (x + 2, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # Debug: uncomment to see the density value per space.
            # cv2.putText(frame, f"{density:.3f}", (x, y + h + 15),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Header: overall count
        header = f"Available: {free_count}/{len(PARKING_SPACES)}"
        cv2.rectangle(frame, (10, 10), (260, 40), (0, 0, 0), -1)
        cv2.putText(frame, header, (20, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Parking Space Detection (q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()