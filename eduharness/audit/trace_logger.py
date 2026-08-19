from __future__ import annotations

import json
from pathlib import Path

from eduharness.audit.trace_schema import TraceRecord


class TraceLogger:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, record: TraceRecord) -> None:
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=True) + "\n")
