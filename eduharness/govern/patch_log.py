from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class PatchLog:
    def __init__(self, file_path: str | Path = "evaluation/data/results/patch_log.jsonl") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, patch_record: dict) -> None:
        patch_record = dict(patch_record)
        patch_record.setdefault("timestamp", datetime.now(UTC).isoformat())
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(patch_record, ensure_ascii=True) + "\n")
