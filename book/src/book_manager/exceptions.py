"""Domain errors. The API maps each to an HTTP status; the CLI prints them."""


class LibraryError(Exception):
    status = 400


class ValidationError(LibraryError):
    status = 400


class NotFoundError(LibraryError):
    status = 404


class ConflictError(LibraryError):
    status = 409
