from __future__ import annotations


def fallback_response(reason: str = "teacher_unavailable") -> str:
    return (
        "I cannot continue this request right now under current policy. "
        "Please proceed with guided hints or wait for teacher review. "
        f"(fallback: {reason})"
    )
