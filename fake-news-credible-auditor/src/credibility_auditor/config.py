from __future__ import annotations

import copy
from pathlib import Path

import yaml

DEFAULTS: dict = {
    "model": {
        "name": "mrm8488/bert-tiny-finetuned-fake-news-detection",
        "real_labels": ["LABEL_1"],
        "max_confidence": 0.6,
        "chunk_words": 300,
        "overlap_words": 50,
        "max_chunks": 8,
    },
    "fetch": {"timeout": 15, "max_bytes": 5_000_000},
    "extraction": {"min_text_chars": 200},
    "weights": {"content_model": 1.0, "source": 1.5, "citations": 0.5},
    "scoring": {"min_evidence": 0.3, "unreliable_below": 0.4, "questionable_below": 0.7},
    "domains": {
        "trusted": ["reuters.com", "apnews.com", "bbc.com", "bbc.co.uk", "npr.org", "wikipedia.org"],
        "suspicious": ["infowars.com", "beforeitsnews.com", "worldnewsdailyreport.com", "naturalnews.com"],
    },
}


def _merge(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str | Path | None = None) -> dict:
    """Defaults, overridden by `path` or ./config.yaml if present."""
    cfg = copy.deepcopy(DEFAULTS)
    candidate = Path(path) if path else Path("config.yaml")
    if candidate.exists():
        with candidate.open(encoding="utf-8") as fh:
            _merge(cfg, yaml.safe_load(fh) or {})
    elif path:
        raise FileNotFoundError(f"Config file not found: {path}")
    return cfg
