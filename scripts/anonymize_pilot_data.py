from __future__ import annotations

import csv
import hashlib
from pathlib import Path


def anon_id(raw: str) -> str:
    return "p_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:10]


def anonymize_csv(in_path: Path, out_path: Path, id_column: str = "student_id") -> None:
    rows = list(csv.DictReader(in_path.read_text(encoding="utf-8").splitlines()))
    if not rows:
        out_path.write_text("", encoding="utf-8")
        return
    for r in rows:
        if id_column in r:
            r[id_column] = anon_id(r[id_column])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    sample_in = Path("evaluation/data/results/sample_pilot_raw.csv")
    sample_out = Path("evaluation/data/results/sample_pilot_anon.csv")
    if not sample_in.exists():
        sample_in.write_text("student_id,pre_score,post_score\ns1,42,66\ns2,55,71\n", encoding="utf-8")
    anonymize_csv(sample_in, sample_out)
    print(f"Anonymized file written: {sample_out}")
