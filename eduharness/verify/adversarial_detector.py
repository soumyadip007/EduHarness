from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"\bignore (your|all|previous) (rules|instructions)\b", re.I),
    re.compile(r"\bjust give me (the )?(answer|solution|code)\b", re.I),
    re.compile(r"\bpretend you are (my )?(friend|teammate)\b", re.I),
    re.compile(r"\bi am in an exam\b", re.I),
]


def adversarial_score(text: str) -> float:
    if not text.strip():
        return 0.0
    hits = sum(1 for p in PATTERNS if p.search(text))
    return min(1.0, hits / 2.0)


def is_adversarial(text: str, threshold: float = 0.5) -> bool:
    return adversarial_score(text) >= threshold
