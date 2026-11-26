# index Stock Trader Agent - Improved (Alpha Vantage)

Run
bash
pip install -r requirements.txt
index Set key (or paste in GUI):
index Windows: set ALPHA_VANTAGE_API_KEY=your_key
index Mac/Linux: export ALPHA_VANTAGE_API_KEY=your_key
python index.py
Get free key: https://www.alphavantage.co/support/indexapi-key (25 requests/day)

indexindex What Was Fixed

| Original Bug | Fix |
|---

| Fetch button never `.pack()`ed -> invisible | Packed + visible |
| Network on main thread -> UI froze | Background thread |
| Hardcoded `YOUR_API_KEY` -> always failed | Env var + GUI key box + warning |
| No error handling | Bad symbol / API limit / no internet -> messagebox |
| Plot crashed if no data / column renamed | Validates + finds close column dynamically |
| Only `print(head)` | Table (last 20 rows) + Stats + Embedded chart |

indexindex Features

- Symbol + API key + Period (compact/full)
- Stats: Latest Close, Change %, High, Rows
- Table + embedded Matplotlib chart in same window

indexindex Notes

- Indian stocks: use `RELIANCE.BSE` / `TCS.BSE` on Alpha Vantage
- Free tier is slow - wait 60s if you hit limit
