from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import UTC, datetime


PRIORITY_MAP = {"high": 0, "medium": 1, "low": 2}


@dataclass(order=True)
class QueueItem:
    sort_key: tuple[int, float] = field(init=False, repr=False)
    priority: str
    created_at: datetime
    escalation_id: str
    payload: dict

    def __post_init__(self) -> None:
        self.sort_key = (PRIORITY_MAP.get(self.priority, 2), self.created_at.timestamp())


class EscalationQueue:
    def __init__(self) -> None:
        self._heap: list[QueueItem] = []

    def push(self, escalation_id: str, payload: dict, priority: str = "medium") -> None:
        item = QueueItem(
            priority=priority,
            created_at=datetime.now(UTC),
            escalation_id=escalation_id,
            payload=payload,
        )
        heapq.heappush(self._heap, item)

    def pop(self) -> QueueItem | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def size(self) -> int:
        return len(self._heap)

    def list_items(self) -> list[dict]:
        return [
            {
                "escalation_id": i.escalation_id,
                "priority": i.priority,
                "created_at": i.created_at.isoformat(),
                "payload": i.payload,
            }
            for i in sorted(self._heap)
        ]
