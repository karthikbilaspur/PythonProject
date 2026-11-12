class AuditError(Exception):
    """Base class for expected, user-facing audit failures."""


class FetchError(AuditError):
    """The page could not be downloaded or is not HTML."""


class ExtractionError(AuditError):
    """No usable article text could be extracted."""
