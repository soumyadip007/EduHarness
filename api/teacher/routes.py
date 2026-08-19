from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


@router.get("/queue")
def get_queue() -> dict:
    return {
        "items": [
            {"escalation_id": "sess-1-3", "priority": "high", "reason": "answer_inducing"},
            {"escalation_id": "sess-2-1", "priority": "medium", "reason": "mastery_drift"},
        ]
    }


@router.get("/reports/summary")
def summary() -> dict:
    return {"interventions_per_week": 7, "patch_success_rate": 0.82}
