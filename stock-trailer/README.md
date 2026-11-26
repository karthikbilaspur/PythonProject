# Real-Time Stock Tracker - Improved (yfinance)

index Run
bash
pip install -r requirements.txt
python stock_tracker.py

Enter AAPL / RELIANCE.NS / TCS.NS -> Start Tracking

index What Was Fixed

| Original Bug | Fix |

|---|---|
| `Stop` did `thread.join()` on UI thread -> froze | No join on UI, just `stop_event.set()` |
| Thread not daemon -> app wouldn't close | `daemon=True` |
| `history(1d,1m)` every 5s -> slow/heavy | `fast_info.lastPrice` first, history as fallback |
| `iloc[-1]` crashed on empty data | Checks `empty` -> returns None + status |
| Graph grew forever, x-axis strings | Keeps last 60 points, real datetime axis |
| `time.sleep(5)` blocked Stop for 5s | Sleep in 0.5s chunks, Stop reacts instantly |
| No High/Low/Change | Added High/Low/Change + last update time |

index Features

- Live price every 5s, change ▲/▼ + %
- Live chart (last 60 points)
- Indian stocks: `RELIANCE.NS`, `TCS.NS`, `INFY.NS` (`.NS` = NSE)

index Notes
yfinance = unofficial Yahoo Finance data, may be delayed / rate-limited.
This is a learning tool, not financial advice.
