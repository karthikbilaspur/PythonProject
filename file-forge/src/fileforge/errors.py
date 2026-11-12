class FileForgeError(Exception):
    """Expected, user-facing failure (bad input, wrong password, network error...)."""


class VaultError(FileForgeError):
    pass


class FetchError(FileForgeError):
    pass


class JournalError(FileForgeError):
    pass
