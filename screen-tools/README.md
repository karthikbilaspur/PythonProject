# Screen Capture Tool

Tkinter app with 3 tabs: Screen Recorder, Screenshot, Delayed Screenshot.

## Requirements
```bash
pip install opencv-python numpy pillow pyautogui
```

## Run
```bash
python screen_capture_tool.py
```

## Features
- **Screen Recorder:** Start/Stop button. Saves `<timestamp>.avi` (XVID, 10 fps). Uses your real screen size, not hardcoded 1920x1080. Preview window: press Esc to stop.
- **Screenshot:** Saves `<timestamp>.png` instantly.
- **Delayed Screenshot:** Enter delay in seconds, click Take — screenshot is taken after the delay without freezing the UI.

## Fixes vs original version
- Recorder ran in the main thread and froze Tkinter — now runs in a background thread with a real Stop button.
- Colour conversion was `COLOR_BGR2RGB` (wrong) — PIL gives RGB, OpenCV wants BGR, so now `COLOR_RGB2BGR`.
- Hardcoded 1920x1080 replaced with `pyautogui.size()`.
- Delayed screenshot used blocking `time.sleep()` — now uses `root.after()`.

## Limitations
- `ImageGrab.grab()` works on Windows/macOS. On Linux (X11) you may need `scrot` or use `pyautogui.screenshot()` instead.
- `.avi` / XVID files are large; no audio is recorded.
- Recording the screen that shows the preview window will capture the preview itself.
