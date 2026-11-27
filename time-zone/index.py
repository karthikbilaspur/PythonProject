import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import time

# ---------- Language data ----------
# name -> code (deep-translator / ISO codes)
LANGUAGES = {
    'English': 'en', 'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar',
    'Bengali': 'bn', 'Chinese': 'zh-CN', 'Dutch': 'nl', 'French': 'fr',
    'German': 'de', 'Gujarati': 'gu', 'Hindi': 'hi', 'Italian': 'it',
    'Japanese': 'ja', 'Kannada': 'kn', 'Korean': 'ko', 'Malayalam': 'ml',
    'Marathi': 'mr', 'Nepali': 'ne', 'Portuguese': 'pt', 'Punjabi': 'pa',
    'Russian': 'ru', 'Spanish': 'es', 'Tamil': 'ta', 'Telugu': 'te',
    'Thai': 'th', 'Turkish': 'tr', 'Urdu': 'ur', 'Vietnamese': 'vi',
}

# Offline fallback for the 3 signal words, so detector still works with no internet
OFFLINE_SIGNALS = {
    'en': ('Red', 'Yellow', 'Green'),
    'hi': ('लाल', 'पीला', 'हरा'), 'es': ('Rojo', 'Amarillo', 'Verde'),
    'fr': ('Rouge', 'Jaune', 'Vert'), 'de': ('Rot', 'Gelb', 'Grün'),
    'ta': ('சிவப்பு', 'மஞ்சள்', 'பச்சை'), 'te': ('ఎరుపు', 'పసుపు', 'ఆకుపచ్చ'),
    'kn': ('ಕೆಂಪು', 'ಹಳದಿ', 'ಹಸಿರು'), 'ml': ('ചുവപ്പ്', 'മഞ്ഞ', 'പച്ച'),
    'bn': ('লাল', 'হলুদ', 'সবুজ'), 'mr': ('लाल', 'पिवळा', 'हिरवा'),
    'gu': ('લાલ', 'પીળો', 'લીલો'), 'pa': ('ਲਾਲ', 'ਪੀਲਾ', 'ਹਰਾ'),
    'ur': ('سرخ', 'پیلا', 'سبز'), 'ar': ('أحمر', 'أصفر', 'أخضر'),
    'ja': ('赤', '黄', '緑'), 'ko': ('빨강', '노랑', '초록'),
    'zh-CN': ('红', '黄', '绿'), 'ru': ('Красный', 'Жёлтый', 'Зелёный'),
    'pt': ('Vermelho', 'Amarelo', 'Verde'), 'it': ('Rosso', 'Giallo', 'Verde'),
    'nl': ('Rood', 'Geel', 'Groen'), 'tr': ('Kırmızı', 'Sarı', 'Yeşil'),
    'th': ('แดง', 'เหลือง', 'เขียว'), 'vi': ('Đỏ', 'Vàng', 'Xanh lá'),
    'ne': ('रातो', 'पहेँलो', 'हरियो'),
}

def translate_text(text: str, dest_code: str) -> str:
    """Try deep-translator, fall back to offline dict for signal words, else return original."""
    if not text.strip():
        return ""
    try:
        from deep_translator import GoogleTranslator  # type: ignore[import-untyped]
        from typing import Any
        translator: Any = GoogleTranslator(source='auto', target=dest_code)
        return translator.translate(text)
    except Exception:
        # Offline fallback: only for Red/Yellow/Green
        low = text.strip().lower()
        mapping = {'red': 0, 'yellow': 1, 'green': 2}
        if low in mapping and dest_code in OFFLINE_SIGNALS:
            return OFFLINE_SIGNALS[dest_code][mapping[low]]
        return f"[offline] {text}"


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multilingual Traffic Signal Detector + Translator")
        self.root.geometry("760x560")
        self.root.minsize(700, 500)

        self.target_lang = tk.StringVar(value="Hindi")
        self.signal_labels = OFFLINE_SIGNALS['hi']  # (red, yellow, green)
        self.detector_running = False
        self.cap = None
        self.frame_queue: queue.Queue[object] = queue.Queue(maxsize=2)
        self.video_path = tk.StringVar(value="No file chosen — will use webcam")

        self._build_ui()
        self._refresh_signal_labels()  # translate Red/Yellow/Green to current language

    # ---------------- UI ----------------
    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Tab 1: Translator ---
        t1 = ttk.Frame(notebook, padding=12)
        notebook.add(t1, text="  Translator  ")
        t1.columnconfigure(0, weight=1); t1.columnconfigure(1, weight=1)

        ttk.Label(t1, text="Translate to:").grid(row=0, column=0, sticky="w", pady=4)
        self.lang_combo = ttk.Combobox(t1, textvariable=self.target_lang,
                                       values=list(LANGUAGES.keys()),
                                       state="readonly", width=20)
        self.lang_combo.grid(row=0, column=1, sticky="ew", pady=4)
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_signal_labels())

        ttk.Label(t1, text="Enter text:").grid(row=1, column=0, sticky="w")
        ttk.Label(t1, text="Translation:").grid(row=1, column=1, sticky="w")
        self.in_text = tk.Text(t1, height=10, wrap="word")
        self.in_text.grid(row=2, column=0, sticky="nsew", padx=(0, 6))
        self.out_text = tk.Text(t1, height=10, wrap="word", state="disabled")
        self.out_text.grid(row=2, column=1, sticky="nsew", padx=(6, 0))

        btns = ttk.Frame(t1); btns.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btns, text="Translate", command=self.do_translate).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear_translator).pack(side="left", padx=4)
        ttk.Button(btns, text="Swap → Detector language ✓", command=self._refresh_signal_labels).pack(side="left", padx=4)

        self.trans_status = ttk.Label(t1, text="", foreground="gray")
        self.trans_status.grid(row=4, column=0, columnspan=2, sticky="w")

        # --- Tab 2: Detector ---
        t2 = ttk.Frame(notebook, padding=12)
        notebook.add(t2, text="  Traffic Signal Detector  ")
        t2.columnconfigure(0, weight=1)

        ttk.Label(t2, text="Detects Red / Yellow / Green lights and labels them in the language above.",
                  wraplength=680).grid(row=0, column=0, sticky="w", pady=(0, 8))

        src = ttk.Frame(t2); src.grid(row=1, column=0, sticky="ew", pady=4)
        ttk.Button(src, text="Choose Video File…", command=self.choose_video).pack(side="left")
        ttk.Label(src, textvariable=self.video_path).pack(side="left", padx=8)
        ttk.Button(src, text="Use Webcam", command=self.use_webcam).pack(side="left", padx=4)

        ctrl = ttk.Frame(t2); ctrl.grid(row=2, column=0, sticky="w", pady=8)
        self.start_btn = ttk.Button(ctrl, text="▶ Start Detection", command=self.start_detection)
        self.start_btn.pack(side="left", padx=(0, 6))
        ttk.Button(ctrl, text="■ Stop", command=self.stop_detection).pack(side="left")

        # Live status: big label showing current signal
        self.signal_var = tk.StringVar(value="—  Press Start  —")
        ttk.Label(t2, textvariable=self.signal_var, font=("", 22, "bold")).grid(row=3, column=0, pady=12)
        self.detail_var = tk.StringVar(value="Detected: none  |  Language: Hindi")
        ttk.Label(t2, textvariable=self.detail_var, foreground="gray").grid(row=4, column=0, sticky="w")
        ttk.Label(t2, text="Tip: point your webcam at a traffic-light image / video on your phone to test it.\n"
                           "Press Q in the OpenCV window to close it, or Stop here.",
                  wraplength=680, foreground="gray").grid(row=5, column=0, sticky="w", pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- Translator ----------------
    def do_translate(self):
        text = self.in_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showerror("Translator", "Please fill the box first.")
            return
        code = LANGUAGES[self.target_lang.get()]
        self.trans_status.config(text="Translating…")
        # Run in thread so UI doesn't freeze
        threading.Thread(target=self._translate_bg, args=(text, code), daemon=True).start()

    def _translate_bg(self, text: str, code: str) -> None:
        out = translate_text(text, code)
        self.root.after(0, lambda: self._show_translation(out))

    def _show_translation(self, out: str) -> None:
        self.out_text.config(state="normal")
        self.out_text.delete("1.0", "end")
        self.out_text.insert("end", out)
        self.out_text.config(state="disabled")
        self.trans_status.config(text="Done.")

    def clear_translator(self):
        self.in_text.delete("1.0", "end")
        self.out_text.config(state="normal"); self.out_text.delete("1.0", "end"); self.out_text.config(state="disabled")

    def _refresh_signal_labels(self):
        code = LANGUAGES[self.target_lang.get()]
        # Translate the 3 signal words in background
        def bg():
            labels = (translate_text("Red", code), translate_text("Yellow", code),
                      translate_text("Green", code))
            self.root.after(0, lambda: self._set_labels(labels))
        threading.Thread(target=bg, daemon=True).start()

    def _set_labels(self, labels: tuple[str, str, str]) -> None:
        self.signal_labels = labels
        self.detail_var.set(f"Detected: none  |  Language: {self.target_lang.get()}  |  "
                            f"Labels: {labels[0]} / {labels[1]} / {labels[2]}")
        self.trans_status.config(text=f"Detector labels now in {self.target_lang.get()}.")

    # ---------------- Detector ----------------
    def choose_video(self):
        path = filedialog.askopenfilename(title="Choose video",
            filetypes=[("Video", "*.mp4 *.avi *.mov *.mkv"), ("All", "*.*")])
        if path:
            self.video_path.set(path)

    def use_webcam(self):
        self.video_path.set("WEBCAM")

    def start_detection(self):
        if self.detector_running:
            return
        from importlib.util import find_spec
        if find_spec("cv2") is None:
            messagebox.showerror("Missing dependency", "Install OpenCV first:\n pip install opencv-python")
            return
        self.detector_running = True
        self.start_btn.config(state="disabled")
        threading.Thread(target=self._detection_loop, daemon=True).start()

    def stop_detection(self):
        self.detector_running = False
        self.start_btn.config(state="normal")
        self.signal_var.set("—  Stopped  —")

    def _detection_loop(self):
        import cv2
        import numpy as np
        from numpy.typing import NDArray

        src = self.video_path.get()
        cap = cv2.VideoCapture(0 if src == "WEBCAM" else src)
        if not cap.isOpened():
            self.root.after(0, lambda: messagebox.showerror("Detector", f"Could not open: {src}"))
            self.root.after(0, self.stop_detection)
            return
        self.cap = cap

        # FIX from original: red wraps around hue 0, needs TWO ranges.
        # Also added min-area filter so tiny noise isn't boxed.
        ranges: dict[int, tuple[tuple[NDArray[np.uint8], NDArray[np.uint8]], ...]] = {
            0: ((np.array([0, 120, 70], dtype=np.uint8), np.array([10, 255, 255], dtype=np.uint8)),
                (np.array([170, 120, 70], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8))),  # Red (x2)
            1: ((np.array([20, 100, 100], dtype=np.uint8), np.array([30, 255, 255], dtype=np.uint8)),),    # Yellow
            2: ((np.array([40, 100, 100], dtype=np.uint8), np.array([85, 255, 255], dtype=np.uint8)),),    # Green
        }
        kernel = np.ones((5, 5), np.uint8)
        MIN_AREA = 500
        last_seen = "none"
        last_time = time.time()

        while self.detector_running:
            ret, frame = cap.read()
            if not ret:
                break
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            detected: list[int] = []

            for idx, range_list in ranges.items():
                lo, hi = range_list[0]
                mask = cv2.inRange(hsv, lo, hi)
                for lo, hi in range_list[1:]:
                    m = cv2.inRange(hsv, lo, hi)
                    mask = cv2.bitwise_or(mask, m)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv2.contourArea(c) < MIN_AREA:
                        continue  # ignore noise
                    x, y, w, h = cv2.boundingRect(c)
                    # Roughly circular / signal-like? skip very flat boxes
                    if h == 0 or not (0.3 < w / h < 3.0):
                        continue
                    detected.append(idx)
                    colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), colors[idx], 2)
                    cv2.putText(frame, self.signal_labels[idx], (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[idx], 2)

            # Update Tkinter label (throttled, from main thread via after)
            current = self.signal_labels[detected[0]] if detected else "—"
            if current != last_seen or time.time() - last_time > 1:
                last_seen, last_time = current, time.time()
                self.root.after(0, lambda c=current, d=len(detected): self._update_signal(c, d))

            cv2.imshow("Multilingual Traffic Signal Detection  (press Q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.root.after(0, self.stop_detection)

    def _update_signal(self, label: str, count: int) -> None:
        self.signal_var.set(label)
        self.detail_var.set(f"Detected: {count} signal(s)  |  Language: {self.target_lang.get()}  |  "
                            f"Labels: {self.signal_labels[0]} / {self.signal_labels[1]} / {self.signal_labels[2]}")

    def on_close(self):
        self.detector_running = False
        if self.cap is not None:
            try: self.cap.release()
            except Exception: pass
        try:
            import cv2; cv2.destroyAllWindows()
        except Exception: pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()