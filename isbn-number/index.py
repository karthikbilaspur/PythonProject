import re
import requests
from dataclasses import dataclass

# ---------- ISBN Core ----------

def clean_isbn(isbn: str) -> str:
    """Remove hyphens/spaces and normalize X."""
    return re.sub(r"[-\s]", "", isbn or "").upper()

def isbn10_check_digit(first_9: str) -> str:
    """Calculate check digit for first 9 digits of ISBN-10."""
    if len(first_9) != 9 or not first_9.isdigit():
        raise ValueError("Need exactly 9 digits")
    total = sum((10 - i) * int(d) for i, d in enumerate(first_9))
    remainder = total % 11
    check = (11 - remainder) % 11
    return "X" if check == 10 else str(check)

def isbn13_check_digit(first_12: str) -> str:
    """Calculate check digit for first 12 digits of ISBN-13."""
    if len(first_12) != 12 or not first_12.isdigit():
        raise ValueError("Need exactly 12 digits")
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(first_12))
    return str((10 - (total % 10)) % 10)

def validate_isbn(isbn: str) -> bool:
    isbn = clean_isbn(isbn)

    if len(isbn) == 10:
        if not isbn[:9].isdigit():
            return False
        if not (isbn[9].isdigit() or isbn[9] == "X"):
            return False
        total = sum((10 - i) * int(d) for i, d in enumerate(isbn[:9]))
        total += 10 if isbn[9] == "X" else int(isbn[9])
        return total % 11 == 0

    if len(isbn) == 13:
        if not isbn.isdigit():
            return False
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(isbn[:12]))
        return (10 - (total % 10)) % 10 == int(isbn[12])

    return False

def convert_isbn10_to_13(isbn10: str) -> str | None:
    """0306406152 -> 9780306406157"""
    isbn10 = clean_isbn(isbn10)
    if len(isbn10) != 10 or not validate_isbn(isbn10):
        return None
    base = "978" + isbn10[:9]
    return base + isbn13_check_digit(base)

def convert_isbn13_to_10(isbn13: str) -> str | None:
    """9780306406157 -> 0306406152 (only if starts with 978)"""
    isbn13 = clean_isbn(isbn13)
    if len(isbn13) != 13 or not validate_isbn(isbn13):
        return None
    if not isbn13.startswith("978"):
        return None  # 979- books have no ISBN-10 equivalent
    base = isbn13[3:12]
    return base + isbn10_check_digit(base)

def format_isbn(isbn: str) -> str:
    """Best-effort pretty formatting: 978-0-306-40615-7"""
    isbn = clean_isbn(isbn)
    if len(isbn) == 13 and isbn.isdigit():
        # Generic grouping: prefix - group - publisher - title - check
        # Real grouping needs a registrant table, this is readable fallback
        return f"{isbn[:3]}-{isbn[3]}-{isbn[4:7]}-{isbn[7:12]}-{isbn[12]}"
    if len(isbn) == 10:
        return f"{isbn[0]}-{isbn[1:4]}-{isbn[4:9]}-{isbn[9]}"
    return isbn

def get_isbn_info(isbn: str) -> dict[str, str | bool | None]:
    """Return everything we know about an ISBN."""
    cleaned = clean_isbn(isbn)
    is_valid = validate_isbn(isbn)
    info: dict[str, str | bool | None] = {
        "input": isbn,
        "cleaned": cleaned,
        "type": "ISBN-13" if len(cleaned) == 13 else "ISBN-10" if len(cleaned) == 10 else "Unknown",
        "valid": is_valid,
        "formatted": format_isbn(isbn) if is_valid else None,
        "converted": None,
    }
    if is_valid:
        if len(cleaned) == 10:
            info["converted"] = convert_isbn10_to_13(cleaned)
        elif len(cleaned) == 13:
            info["converted"] = convert_isbn13_to_10(cleaned)
    return info

# ---------- Google Books Search ----------

@dataclass
class Book:
    title: str
    authors: list[str]
    published: str
    publisher: str
    isbns: list[str]
    description: str = ""

    def __str__(self):
        authors = ", ".join(self.authors) if self.authors else "Unknown author"
        isbns = ", ".join(self.isbns) if self.isbns else "No ISBN"
        return f"{self.title} — {authors} ({self.published})\n  ISBNs: {isbns}"

def search_books(
    title: str | None = None,
    author: str | None = None,
    isbn: str | None = None,
    max_results: int = 5,
) -> list[Book]:
    """Search Google Books API."""
    query_parts: list[str] = []
    if title:
        query_parts.append(f"intitle:{title}")
    if author:
        query_parts.append(f"inauthor:{author}")
    if isbn:
        query_parts.append(f"isbn:{clean_isbn(isbn)}")

    if not query_parts:
        return []

    try:
        resp = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": " ".join(query_parts), "maxResults": max_results},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"Search failed: {e}")
        return []
    except ValueError:
        print("Search failed: invalid response from API")
        return []

    books: list[Book] = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        isbns: list[str] = []
        for ident in info.get("industryIdentifiers", []):
            if ident.get("type") in ("ISBN_10", "ISBN_13"):
                isbns.append(ident.get("identifier", ""))

        books.append(Book(
            title=info.get("title", "Unknown title"),
            authors=info.get("authors", []),
            published=info.get("publishedDate", "Unknown"),
            publisher=info.get("publisher", "Unknown"),
            isbns=isbns,
            description=info.get("description", "")[:300],
        ))
    return books

def lookup_by_isbn(isbn: str) -> Book | None:
    results = search_books(isbn=isbn, max_results=1)
    return results[0] if results else None

# ---------- CLI ----------

def print_isbn_info(isbn: str):
    info = get_isbn_info(isbn)
    print(f"\nInput:     {info['input']}")
    print(f"Cleaned:   {info['cleaned']}")
    print(f"Type:      {info['type']}")
    print(f"Valid:     {'✅ Yes' if info['valid'] else '❌ No'}")
    if info['valid']:
        print(f"Formatted: {info['formatted']}")
        if info['converted']:
            other = "ISBN-13" if info['type'] == "ISBN-10" else "ISBN-10"
            print(f"As {other}: {info['converted']}")
        else:
            print("As ISBN-10: N/A (979- prefix has no ISBN-10 equivalent)")

def batch_validate():
    print("\nEnter ISBNs (one per line, blank line to finish):")
    lines: list[str] = []
    while True:
        line = input().strip()
        if not line:
            break
        lines.append(line)

    if not lines:
        print("Nothing to check.")
        return

    print(f"\n{'ISBN':<20} {'Valid':<8} {'Type':<8} {'Converted'}")
    print("-" * 60)
    for isbn in lines:
        info = get_isbn_info(isbn)
        print(f"{info['cleaned']:<20} {'Yes' if info['valid'] else 'No':<8} {info['type']:<8} {info['converted'] or '-'}")

    valid_count = sum(1 for i in lines if validate_isbn(i))
    print(f"\n{valid_count}/{len(lines)} valid")

def main():
    while True:
        print("\n=== ISBN Toolkit ===")
        print("1. Validate / Inspect ISBN")
        print("2. Convert ISBN-10 <-> ISBN-13")
        print("3. Search by Title / Author")
        print("4. Lookup by ISBN (get book details)")
        print("5. Batch Validate (multiple ISBNs)")
        print("6. Quit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            isbn = input("Enter ISBN: ")
            print_isbn_info(isbn)

        elif choice == "2":
            isbn = input("Enter ISBN-10 or ISBN-13: ")
            info = get_isbn_info(isbn)
            if not info['valid']:
                print("❌ Invalid ISBN, can't convert.")
            elif not info['converted']:
                print("This ISBN-13 (979-) has no ISBN-10 equivalent.")
            else:
                print(f"{info['cleaned']} ({info['type']}) -> {info['converted']}")

        elif choice == "3":
            title = input("Title (optional): ").strip()
            author = input("Author (optional): ").strip()
            if not title and not author:
                print("Enter at least a title or author.")
                continue
            books = search_books(title or None, author or None, max_results=5)
            if not books:
                print("No books found.")
            else:
                for i, b in enumerate(books, 1):
                    print(f"\n[{i}] {b}")
                    if b.description:
                        print(f"    {b.description}...")

        elif choice == "4":
            isbn = input("Enter ISBN to lookup: ")
            if not validate_isbn(isbn):
                print("❌ Invalid ISBN.")
                continue
            book = lookup_by_isbn(isbn)
            if book:
                print(f"\nFound: {book}")
                if book.description:
                    print(f"\nDescription: {book.description}...")
                print(f"Publisher: {book.publisher}")
            else:
                print("No book found for that ISBN.")

        elif choice == "5":
            batch_validate()

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try 1-6")

if __name__ == "__main__":
    main()