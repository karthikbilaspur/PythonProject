import argparse
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

# Optional imports - lazy so `organize` / `cpu` work without cv2 installed
try:
    import cv2 as cv2_module
    import numpy as np_module

    cv2: Any = cv2_module
    np: Any = np_module
except ImportError:
    cv2 = None
    np = None

try:
    import psutil as psutil_module

    psutil: Any = psutil_module
except ImportError:
    psutil = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _require_cv2():
    if cv2 is None or np is None:
        print("Error: opencv-python and numpy are required for this command. Run: pip install opencv-python numpy")
        sys.exit(1)

# ---------------------------------------------------------------------------
# 1. YOLO OBJECT DETECTION
# ---------------------------------------------------------------------------

def load_yolo(weights: str = "yolov3.weights", config: str = "yolov3.cfg", names: str = "coco.names"):
    _require_cv2()
    assert cv2 is not None
    assert np is not None
    if not Path(weights).exists() or not Path(config).exists() or not Path(names).exists():
        print(f"Missing YOLO files. Expected: {weights}, {config}, {names}")
        print("Download from https://pjreddie.com/darknet/yolo/ (or use yolov3-tiny for speed)")
        return None, None, None, None
    try:
        net = cv2.dnn.readNet(weights, config)
        with open(names, "r") as f:
            classes = [line.strip() for line in f if line.strip()]
        layer_names = net.getLayerNames()
        # OpenCV version-safe: getUnconnectedOutLayers() shape changed in 4.5+
        unconnected = net.getUnconnectedOutLayers()
        # flatten handles both [[1],[2]] and [1,2]
        output_layers = [layer_names[int(i) - 1] for i in np.array(unconnected).flatten()]
        # Stable colors - generated ONCE, not per frame
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        return net, classes, output_layers, colors
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None, None, None, None

def detect_objects(img: Any, net: Any, output_layers: list[str]) -> list[Any]:
    _require_cv2()
    assert cv2 is not None
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    return outs

def draw_boxes(img: Any, outs: list[Any], classes: list[str], colors: Any, conf_threshold: float = 0.5, nms_threshold: float = 0.4) -> None:
    _require_cv2()
    assert cv2 is not None
    assert np is not None

    class_ids: list[int] = []
    confidences: list[float] = []
    boxes: list[list[int]] = []
    h_img, w_img = img.shape[:2]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = int(np.argmax(scores))
            confidence = float(scores[class_id])
            if confidence > conf_threshold:
                center_x = int(detection[0] * w_img)
                center_y = int(detection[1] * h_img)
                w = int(detection[2] * w_img)
                h = int(detection[3] * h_img)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(confidence)
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    if len(indexes) > 0:
        # NMSBoxes returns [[0],[2]] in old OpenCV, [0,2] in new - flatten handles both
        for i in np.array(indexes).flatten():
            box_index = int(i)
            x, y, w, h = boxes[box_index]
            x, y, w, h = int(x), int(y), int(w), int(h)
            label = f"{classes[class_ids[box_index]]} {confidences[box_index]:.2f}"
            color = tuple(int(c) for c in colors[class_ids[box_index]])
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return img

def run_yolo(args: argparse.Namespace):
    _require_cv2()
    assert cv2 is not None
    net, classes, output_layers, colors = load_yolo(args.weights, args.config, args.names)
    if net is None or classes is None or output_layers is None or colors is None:
        return
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    print("Press 'q' to quit.")
    try:
        while True:
            ret, img = cap.read()
            if not ret:
                print("Cannot receive frame")
                break
            outs = detect_objects(img, net, output_layers)
            img = draw_boxes(img, outs, classes, colors, conf_threshold=args.conf)
            cv2.imshow("YOLO Detection - Press q to quit", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# ---------------------------------------------------------------------------
# 2. OCR
# ---------------------------------------------------------------------------

def ocr_to_text(image_path: str, tesseract_cmd: str | None = None, psm: str = "6") -> str | None:
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        print("Error: Pillow and pytesseract required. Run: pip install Pillow pytesseract")
        return None
    if tesseract_cmd:
        pytesseract.tesseract_cmd = tesseract_cmd
    # If tesseract not in PATH and no explicit path, warn early
    if not tesseract_cmd and shutil.which("tesseract") is None:
        print("Warning: 'tesseract' not found in PATH. Install Tesseract OCR or pass --tesseract <path>")
    try:
        img = Image.open(image_path)
        # Light preprocessing helps a lot: grayscale + upscale if small
        if img.mode != "L":
            img = img.convert("L")
        config = f"--psm {psm}" if psm else ""
        pytesseract_api: Any = pytesseract
        text: str = str(pytesseract_api.image_to_string(img, config=config))
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

def run_ocr(args: argparse.Namespace):
    text = ocr_to_text(args.image, tesseract_cmd=args.tesseract, psm=args.psm)
    if text is not None:
        print("\n--- OCR Result ---")
        print(text)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"\nSaved to {args.output}")

# ---------------------------------------------------------------------------
# 3. ORB FEATURE MATCHING
# ---------------------------------------------------------------------------

def _resize_keep_aspect(img: Any, max_dim: int = 800) -> Any:
    h, w = img.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)
    if scale < 1.0:
        return cv2.resize(img, (int(w * scale), int(h * scale)))
    return img

def run_orb(args: argparse.Namespace):
    _require_cv2()
    image = cv2.imread(args.image1)
    test_image = cv2.imread(args.image2)
    if image is None:
        print(f"Error loading image: {args.image1}"); return
    if test_image is None:
        print(f"Error loading test image: {args.image2}"); return

    image = _resize_keep_aspect(image)
    test_image = _resize_keep_aspect(test_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    test_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(gray, None)
    kp2, des2 = orb.detectAndCompute(test_gray, None)

    print(f"Keypoints in image 1: {len(kp1) if kp1 else 0}")
    print(f"Keypoints in image 2: {len(kp2) if kp2 else 0}")

    if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
        print("No descriptors found in one of the images - cannot match.")
        return

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    # Good matches: distance < 50 is a common heuristic for ORB
    good = [m for m in matches if m.distance < 50]
    print(f"Total matches: {len(matches)} | Good matches (dist < 50): {len(good)}")

    result = cv2.drawMatches(image, kp1, test_image, kp2, matches[:100], None, flags=2)
    if args.show:
        cv2.imshow('image VS test_image', np.concatenate((image, test_image), axis=1))
        kp_img = image.copy()
        cv2.drawKeypoints(image, kp1, kp_img, color=(0, 255, 0))
        cv2.imshow('keypoints', kp_img)
        cv2.imshow('ORB Matches', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_name = Path(args.image1).stem
    output = output_dir / f"{image_name}(featureMatched).jpg"
    cv2.imwrite(str(output), result)
    print(f"Saved result to {output}")

# ---------------------------------------------------------------------------
# 4. FILE ORGANIZER
# ---------------------------------------------------------------------------

def organize_files(directory: Path, dry_run: bool = False):
    directory = Path(directory)
    if not directory.is_dir():
        print(f"Invalid directory: {directory}")
        return
    # Collect first - don't mutate while iterating
    files = [f for f in directory.iterdir() if f.is_file()]
    if not files:
        print("No files to organize.")
        return
    # Count
    from collections import Counter
    counts: Counter[str] = Counter()
    for f in files:
        ext = f.suffix[1:].lower() if f.suffix else "no_extension"
        counts[ext] += 1
    for ext, count in sorted(counts.items(), key=lambda item: item[0]):
        print(f"There are {count} file(s) with extension '{ext}'")
    print()
    for f in files:
        ext = f.suffix[1:].lower() if f.suffix else "no_extension"
        dest_dir = directory / ext
        dest = dest_dir / f.name
        if dry_run:
            print(f"[DRY-RUN] Would move {f.name} -> {ext}/")
            continue
        dest_dir.mkdir(exist_ok=True)
        # Avoid overwriting if same name exists
        if dest.exists() and dest.resolve() != f.resolve():
            dest = dest_dir / f"{f.stem}_copy{f.suffix}"
        print(f"Moving {f.name} to {ext}/")
        f.rename(dest)
    print("\nDone!")

def run_organize(args: argparse.Namespace):
    if args.directory:
        directory = Path(args.directory)
    else:
        inp = input("Type path of directory (or press Enter for current directory, or 'quit'): ").strip()
        if inp.lower() == "quit":
            return
        directory = Path(inp) if inp else Path.cwd()
    print(f"Organizing files in {directory}...\n")
    organize_files(directory, dry_run=args.dry_run)

# ---------------------------------------------------------------------------
# 5. CPU MONITOR
# ---------------------------------------------------------------------------

def alert_high_cpu_usage():
    current = platform.system()
    msg = "High CPU usage detected!"
    try:
        if current == "Darwin":
            subprocess.run(["say", msg], check=False)
        elif current == "Windows":
            powershell_command = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.MessageBox]::Show(" 
                "$args[0], 'Alert', 0, [System.Windows.Forms.MessageBoxIcon]::Warning)"
            )
            subprocess.run(["powershell", "-Command", powershell_command, msg], check=False)
        elif current == "Linux":
            # notify-send may not exist on servers - fallback to log only
            if shutil.which("notify-send"):
                subprocess.run(["notify-send", msg], check=False)
            else:
                print(f"ALERT: {msg} (notify-send not available)")
        else:
            print(f"ALERT: {msg}")
    except Exception as e:
        logger.error(f"Alert failed: {e}")

def run_cpu_monitor(args: argparse.Namespace) -> None:
    if psutil is None:
        print("Error: psutil required. Run: pip install psutil"); return
    threshold, interval, cooldown = args.threshold, args.interval, args.cooldown
    logger.info(f"Monitoring CPU - threshold: {threshold}%, check every {interval}s, alert cooldown: {cooldown}s")
    last_alert = 0
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            logger.info(f"Current CPU Usage: {cpu}%")
            if cpu > threshold:
                now = time.time()
                if now - last_alert >= cooldown:
                    logger.warning("CPU usage exceeds threshold!")
                    alert_high_cpu_usage()
                    last_alert = now
                else:
                    logger.warning(f"CPU still high ({cpu}%) - alert suppressed (cooldown)")
            time.sleep(max(0, interval - 1))  # interval=1 already spent in cpu_percent()
    except KeyboardInterrupt:
        logger.info("Stopping CPU monitor...")

# ---------------------------------------------------------------------------
# CLI / MENU
# ---------------------------------------------------------------------------

def interactive_menu():
    while True:
        print("""
=== index Menu ===
1. YOLO Object Detection (webcam)
2. OCR - Image to Text
3. ORB Feature Matching (compare 2 images)
4. File Organizer (sort by extension)
5. CPU Monitor
0. Quit
""")
        choice = input("Choose (0-5): ").strip()
        if choice == "0" or choice.lower() in ("q", "quit", "exit"):
            break
        elif choice == "1":
            run_yolo(argparse.Namespace(weights="yolov3.weights", config="yolov3.cfg", names="coco.names", camera=0, conf=0.5))
        elif choice == "2":
            p = input("Image path: ").strip()
            if p: run_ocr(argparse.Namespace(image=p, tesseract=None, psm="6", output=None))
        elif choice == "3":
            p1 = input("First image path: ").strip()
            p2 = input("Second image path: ").strip()
            if p1 and p2: run_orb(argparse.Namespace(image1=p1, image2=p2, output_dir="./ORB Algorithm", show=True))
        elif choice == "4":
            run_organize(argparse.Namespace(directory=None, dry_run=False))
        elif choice == "5":
            run_cpu_monitor(argparse.Namespace(threshold=80, interval=10, cooldown=300))
        else:
            print("Invalid choice.")

def main():
    parser = argparse.ArgumentParser(description="index: YOLO + OCR + ORB + Organizer + CPU Monitor")
    sub = parser.add_subparsers(dest="command")

    p_yolo = sub.add_parser("yolo", help="Webcam YOLO object detection")
    p_yolo.add_argument("--weights", default="yolov3.weights")
    p_yolo.add_argument("--config", default="yolov3.cfg")
    p_yolo.add_argument("--names", default="coco.names")
    p_yolo.add_argument("--camera", type=int, default=0)
    p_yolo.add_argument("--conf", type=float, default=0.5)

    p_ocr = sub.add_parser("ocr", help="OCR image to text")
    p_ocr.add_argument("image")
    p_ocr.add_argument("--tesseract", default=None, help="Path to tesseract.exe if not in PATH")
    p_ocr.add_argument("--psm", default="6")
    p_ocr.add_argument("--output", default=None, help="Save text to file")

    p_orb = sub.add_parser("orb", help="ORB feature matching between 2 images")
    p_orb.add_argument("image1")
    p_orb.add_argument("image2")
    p_orb.add_argument("--output-dir", default="./ORB Algorithm")
    p_orb.add_argument("--show", action="store_true", help="Show windows")

    p_org = sub.add_parser("organize", help="Organize files by extension")
    p_org.add_argument("directory", nargs="?", default=None)
    p_org.add_argument("--dry-run", action="store_true")

    p_cpu = sub.add_parser("cpu", help="Monitor CPU usage")
    p_cpu.add_argument("--threshold", type=int, default=80)
    p_cpu.add_argument("--interval", type=int, default=10)
    p_cpu.add_argument("--cooldown", type=int, default=300, help="Seconds between alerts")

    sub.add_parser("menu", help="Interactive menu")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        print("\nTip: try 'python multitool.py menu'")
        return

    if args.command == "yolo": run_yolo(args)
    elif args.command == "ocr": run_ocr(args)
    elif args.command == "orb": run_orb(args)
    elif args.command == "organize": run_organize(args)
    elif args.command == "cpu": run_cpu_monitor(args)
    elif args.command == "menu": interactive_menu()

if __name__ == "__main__":
    main()
