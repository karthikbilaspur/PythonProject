"""Shared settings, logging and safety helpers used by every module."""
import logging
import os
from dataclasses import dataclass, field

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"),
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")

# A resource is touched ONLY if it carries auto-cleanup=true (opt-in),
# and is never touched if it also carries retain=true (always wins).
OPT_IN_TAG = os.getenv("OPT_IN_TAG", "auto-cleanup")
RETAIN_TAG = os.getenv("RETAIN_TAG", "retain")


def env_flag(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes"}


def default_dry_run() -> bool:
    """Dry-run is ON unless DRY_RUN=false is set explicitly."""
    return env_flag("DRY_RUN", True)


def tag_map(tags) -> dict:
    """Convert [{'Key':..,'Value':..}] (EC2 'Tags' / RDS 'TagList') to a lowercase dict."""
    return {t["Key"].lower(): str(t["Value"]).lower() for t in (tags or [])}


def is_eligible(tags) -> bool:
    """Opt-in tag present and no retain tag."""
    tm = tag_map(tags)
    return tm.get(OPT_IN_TAG.lower()) == "true" and tm.get(RETAIN_TAG.lower()) != "true"


@dataclass
class CleanupResult:
    """Structured outcome so callers can tell 'nothing to do' from 'failed'."""
    acted: list = field(default_factory=list)     # deleted / stopped (or would be, in dry-run)
    skipped: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    def merge(self, other: "CleanupResult") -> "CleanupResult":
        self.acted += other.acted
        self.skipped += other.skipped
        self.errors += other.errors
        return self

    def to_dict(self) -> dict:
        return {"acted": self.acted, "skipped": self.skipped, "errors": self.errors}
