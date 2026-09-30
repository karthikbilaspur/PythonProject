import pytest

from book_manager.service import LibraryService


@pytest.fixture
def svc():
    return LibraryService(":memory:", fine_per_day=0.5)


@pytest.fixture
def seeded(svc):
    book = svc.add_book("Clean Code", "Robert C. Martin", "978-0-13-235088-4", copies=2)
    member = svc.add_member("Asha", "asha@example.com")
    return svc, book, member
