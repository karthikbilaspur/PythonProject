# GitHub Repository Search

Search a public GitHub repo's files by keyword (recursive).

 Requirements

```bash
pip install requests
```

 Run

```bash
python github_search.py
```

 How to use

1. Enter Repository Owner (e.g. `torvalds`), Repository Name (e.g. `linux`), Keyword (e.g. `readme`).
2. Click **Search (recursive)** — it walks subfolders too, not just the top level.
3. Results show `path (url)` for every matching file.

 Rate limits
Unauthenticated GitHub API = 60 requests/hour. Large repos walk many folders and can hit it. Set a token for 5,000/hour:

```bash
# Windows PowerShell
$env:GITHUB_TOKEN="ghp_..."
# Linux/macOS
export GITHUB_TOKEN="ghp_..."
python github_search.py
```

 Fixes vs original version

- Original only listed top-level `/contents` — now recursive.
- Added User-Agent, timeout, and clear errors for 404 (missing/private repo) and 403 (rate limit).
- Input validation: empty owner/repo/keyword now shows an error instead of a broken request.
