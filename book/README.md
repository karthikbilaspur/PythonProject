# Book Manager

A medium-sized library system: books with copy counts, members, loans with due dates,
fines, overdue reports. SQLite storage, a CLI and a Flask API on top of one service layer.

```
src/book_manager/
  exceptions.py  domain errors (mapped to HTTP 400/404/409)
  validators.py  ISBN-10/13 checksum, email, text/int checks
  db.py          SQLite schema + connection
  service.py     LibraryService: every business rule lives here
  api.py         Flask app factory (optional API-key auth)
  cli.py         argparse CLI
tests/           pytest (in-memory DB, dates injected for deterministic fines)
```

## Rules enforced
- ISBN is validated (checksum) and unique; duplicate ISBN -> 409.
- Availability = total copies - active loans; checkout fails when 0 (transactional, race-safe).
- Max 3 active loans per member; same book can't be borrowed twice by one member.
- Loan default 14 days; fine = days late x `FINE_PER_DAY` (default 0.5) when returned.
- Copies can't be lowered below the number on loan; books with active loans can't be deleted.

## Run
```
pip install -r requirements-dev.txt
pip install -e .
pytest
```

CLI:
```
book-manager add-book "Clean Code" "Robert C. Martin" 978-0-13-235088-4 --copies 2
book-manager add-member Asha asha@example.com
book-manager checkout 1 1
book-manager overdue
book-manager return 1
book-manager list-books -q clean --available
```

API (dev server):
```
BOOKS_DB=books.db python -m book_manager.api        # add API_KEY=secret to require X-API-Key
```
Endpoints: `POST/GET /books`, `GET/PUT/DELETE /books/<id>`, `POST/GET /members`,
`GET /members/<id>/loans?active=true`, `POST /loans`, `POST /loans/<id>/return`, `GET /loans/overdue`, `GET /health`.

Env: `BOOKS_DB` (books.db), `FINE_PER_DAY` (0.5), `API_KEY` (optional).
