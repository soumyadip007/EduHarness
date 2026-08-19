from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/teacher", tags=["teacher"])

CONTRACT_PATH = Path("configs/contracts/default_contract.yaml")


class QueueActionRequest(BaseModel):
    action: str
    note: str | None = None


class ContractUpdateRequest(BaseModel):
    yaml_text: str


@router.get("/queue")
def get_queue() -> dict:
    return {
        "items": [
            {"escalation_id": "sess-1-3", "priority": "high", "reason": "answer_inducing"},
            {"escalation_id": "sess-2-1", "priority": "medium", "reason": "mastery_drift"},
        ]
    }


@router.get("/queue/{item_id}")
def get_queue_item(item_id: str) -> dict:
    return {
        "escalation_id": item_id,
        "student_input": "Please give me the final answer.",
        "verify_action": "withhold",
        "reason": "answer_inducing",
    }


@router.post("/queue/{item_id}/action")
def queue_action(item_id: str, payload: QueueActionRequest) -> dict:
    return {"escalation_id": item_id, "applied": True, "action": payload.action, "note": payload.note}


@router.get("/students")
def students() -> dict:
    return {
        "students": [
            {"id": "student-demo-session", "risk": "medium", "sessions": 4},
            {"id": "s1", "risk": "low", "sessions": 2},
        ]
    }


@router.get("/students/{student_id}")
def student_detail(student_id: str) -> dict:
    return {"id": student_id, "mastery": {"loops": 0.52, "functions": 0.41}, "open_escalations": 1}


@router.get("/audit")
def audit() -> dict:
    return {
        "events": [
            {"id": "a1", "action": "approve", "by": "teacher1", "at": "2026-08-19T22:00:00Z"},
            {"id": "a2", "action": "patch_rule", "by": "teacher1", "at": "2026-08-19T22:05:00Z"},
        ]
    }


@router.get("/contract")
def get_contract() -> dict:
    return {"yaml_text": CONTRACT_PATH.read_text(encoding="utf-8") if CONTRACT_PATH.exists() else ""}


@router.put("/contract")
def update_contract(payload: ContractUpdateRequest) -> dict:
    data = yaml.safe_load(payload.yaml_text) or {}
    CONTRACT_PATH.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return {"updated": True}


@router.post("/contract/rollback")
def rollback_contract() -> dict:
    return {"rolled_back": False, "message": "Rollback placeholder in local prototype"}


@router.get("/reports/summary")
def summary() -> dict:
    return {"interventions_per_week": 7, "patch_success_rate": 0.82}
