# FileForge

A safe-by-default file toolkit that merges and fixes a set of standalone scripts (JPEG carver, downloaders,
encryptors, watchdog monitor, organizers, semantic file search) into one tested package.

**Safety principles:** destructive commands are dry-run by default, nothing is ever overwritten
(collisions become `name (1).ext`), every applied move is journaled and can be undone, and encryption
writes to a new file and never edits in place.

## Layout

```

fileforge/
├── pyproject.toml
├── src/fileforge/
│   ├── cli.py          # typer CLI (all commands)
│   ├── util.py         # hashing, safe paths, file iteration
│   ├── journal.py      # move journal + undo
│   ├── organize.py     # rule-based organizer (dry run, by-date, YAML rules)
│   ├── dedupe.py       # size -> partial hash -> full hash; quarantine instead of delete
│   ├── vault.py        # scrypt + chunked AES-256-GCM, tamper/truncation detection
│   ├── carve.py        # JPEG/PNG/PDF/ZIP carving by parsing formats; mmap, validation, reports
│   ├── search.py       # incremental SQLite index, BM25 + optional embeddings, RRF fusion
│   ├── fetch.py        # resumable downloads, retries, checksum
│   ├── watch.py        # live event log + auto-organize finished downloads
│   └── integrity.py    # hash baseline / verify
└── tests/              # 49 tests
```

## Install

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"                                # core + tests
pip install -e ".[search]"                             # optional: dense embeddings (sentence-transformers)
pip install -e ".[docs]"                               # optional: PDF/DOCX text extraction for search
pytest
```

Python 3.10+. Journals and the default search index live in `~/.fileforge` (override with `FILEFORGE_HOME`).

## Commands

```bash
# Organize (dry run first; --apply to move; every run is undoable)
fileforge organize ~/Downloads                  # preview
fileforge organize ~/Downloads --apply [-r] [--by-date] [--rules rules.yaml]
fileforge undo                                  # undo the latest run (or: undo --list / undo <journal>)

# Duplicates (reports by default; nothing is deleted)
fileforge dedupe ~/Pictures
fileforge dedupe ~/Pictures --quarantine ~/Pictures/_dupes

# Encrypted vault (prompts for password; original kept unless --remove-original)
fileforge vault encrypt secrets.pdf             # -> secrets.pdf.ffv
fileforge vault decrypt secrets.pdf.ffv

# Forensic carving from a disk image, a file, or a directory
fileforge carve disk.img -o carved [--kinds jpeg,png] [--keep-invalid]   # writes report.json + report.csv

# Content search
fileforge search index ~/Documents              # dense + BM25 (needs [search]); add --bm25-only for keywords only
fileforge search query "home office tax deduction" -k 5

# Resumable downloads
fileforge fetch URL [URL...] -d downloads [--sha256 HASH] [-j 3]

# Watch a folder (Ctrl+C to stop); keep Downloads tidy automatically
fileforge watch ~/Downloads --auto-organize

# Integrity monitoring (exit code 1 on any change: cron/CI friendly)
fileforge integrity baseline ~/important -o baseline.json
fileforge integrity verify ~/important -b baseline.json
```

Custom organizer rules (`rules.yaml`):
```yaml
Invoices: [pdf, xlsx]
Photos: [jpg, jpeg, png, heic]
```

## What was fixed relative to the original scripts

- **Encryption:** random per-file salt and nonce stored in the header (the old scripts used a zero IV and lost
  their salt), authenticated AES-GCM with chunking for large files, wrong-password and tampering errors,
  atomic writes. The decorative neural-net "key generation" is gone; password strength is a plain rule check
  (plus `zxcvbn` if installed).
- **Organizers:** removed the meaningless sentiment-on-filename and VGG-argmax categorization; added dry run,
  collision handling, unknown-type fallback and undo.
- **Carver:** formats are parsed, so embedded thumbnails no longer truncate a JPEG, and candidates are
  validated with Pillow/zipfile. Input is memory-mapped instead of read entirely into RAM.
- **Search:** indexes file *contents* (chunked), updates incrementally, and fuses keyword and semantic ranking.
- **Downloader:** HTTP status handling, resume, retries, safe filenames from `Content-Disposition`.

## Design notes and limits

- Search uses brute-force cosine over stored vectors: fine up to tens of thousands of chunks; swap in FAISS or
  Chroma beyond that. Changing the embedding model triggers an automatic rebuild.
- The carver is signature-based: fragmented files and encrypted/compressed containers are not reconstructed,
  and Office files are reported as `zip`. Add formats by writing a `finder(buf, start, limit)` and
  registering it in `carve.SIGNATURES`.
- `--remove-original` deletes normally; it is not a secure erase.
- `fetch` downloads sequentially per file (no segmented parallelism) and does not block private/loopback
  addresses; add SSRF protection before exposing it as a service.
- Watching uses OS events via `watchdog`; network drives may deliver events unreliably.
