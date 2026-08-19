from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import UTC, datetime

from api.teacher.realtime import broadcaster
from eduharness.govern.patch_log import PatchLog
from eduharness.govern.patch_pipeline import apply_teacher_action

router = APIRouter(prefix="/api/teacher", tags=["teacher"])

CONTRACT_PATH = Path("configs/contracts/default_contract.yaml")
PATCH_LOG_PATH = Path("evaluation/data/results/patch_log.jsonl")
_patch_log = PatchLog(PATCH_LOG_PATH)
_queue_items: dict[str, dict] = {
    "sess-1-3": {"escalation_id": "sess-1-3", "priority": "high", "reason": "answer_inducing"},
    "sess-2-1": {"escalation_id": "sess-2-1", "priority": "medium", "reason": "mastery_drift"},
}


class QueueActionRequest(BaseModel):
    action: str
    note: str | None = None
    teacher_id: str = "teacher1"
    rewrite_text: str | None = None


class ContractUpdateRequest(BaseModel):
    yaml_text: str


@router.get("/queue")
def get_queue() -> dict:
    return {"items": list(_queue_items.values())}


@router.get("/queue/{item_id}")
def get_queue_item(item_id: str) -> dict:
    if item_id in _queue_items:
        return _queue_items[item_id]
    return {
        "escalation_id": item_id,
        "student_input": "Please give me the final answer.",
        "verify_action": "withhold",
        "reason": "answer_inducing",
    }


@router.post("/queue/{item_id}/action")
async def queue_action(item_id: str, payload: QueueActionRequest) -> dict:
    action_result = apply_teacher_action(
        action=payload.action,
        escalation_id=item_id,
        teacher_id=payload.teacher_id,
        contract_path=str(CONTRACT_PATH),
        patch_log=_patch_log,
        rewrite_text=payload.rewrite_text,
    )
    _queue_items.pop(item_id, None)
    await broadcaster.publish({"event": "queue_updated", "item_id": item_id, "action": payload.action})
    return {"escalation_id": item_id, "note": payload.note, **action_result}


@router.post("/queue/simulate")
async def simulate_queue_item() -> dict:
    item_id = f"sim-{int(datetime.now(UTC).timestamp())}"
    _queue_items[item_id] = {"escalation_id": item_id, "priority": "high", "reason": "simulated_escalation"}
    await broadcaster.publish({"event": "queue_updated", "item_id": item_id, "action": "created"})
    return _queue_items[item_id]


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
    events: list[dict] = []
    if PATCH_LOG_PATH.exists():
        for idx, line in enumerate(PATCH_LOG_PATH.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            record = yaml.safe_load(line)
            if isinstance(record, dict):
                events.append(
                    {
                        "id": f"a{idx}",
                        "action": record.get("action", "unknown"),
                        "by": record.get("teacher_id", "teacher1"),
                        "at": record.get("timestamp", ""),
                    }
                )
    return {"events": events}


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
