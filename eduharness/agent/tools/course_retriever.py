from __future__ import annotations

from pathlib import Path


class CourseRetriever:
    def __init__(self, modules_dir: str | Path) -> None:
        self.modules_dir = Path(modules_dir)
        self.docs = self._load_docs()

    def _load_docs(self) -> list[tuple[str, str]]:
        docs: list[tuple[str, str]] = []
        if not self.modules_dir.exists():
            return docs
        for file in sorted(self.modules_dir.glob("*.md")):
            docs.append((file.name, file.read_text(encoding="utf-8")))
        return docs

    def retrieve(self, query: str, top_k: int = 2) -> str:
        tokens = set(query.lower().split())
        scored: list[tuple[int, str]] = []
        for name, content in self.docs:
            score = sum(1 for t in tokens if t in content.lower())
            if score > 0:
                scored.append((score, f"[{name}]\n{content}"))
        scored.sort(key=lambda x: x[0], reverse=True)
        return "\n\n".join(text for _, text in scored[:top_k])
