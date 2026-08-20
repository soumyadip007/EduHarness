from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import UTC, datetime

from api.services import (
    CONTRACT_PATH,
    escalation_store,
    get_active_model_key,
    patch_log,
    policy_versioning,
    registry,
    session_factory,
    session_store,
    teacher_reply_store,
)
from api.teacher.realtime import broadcaster
from eduharness.govern.patch_pipeline import apply_teacher_action
from eduharness.reports.pdf_report import generate_summary_pdf

router = APIRouter(prefix="/api/teacher", tags=["teacher"])

SENSITIVE_ACTIONS = {"rewrite", "patch_rule", "freeze_topic"}


class QueueActionRequest(BaseModel):
    action: str
    note: str | None = None
    teacher_id: str = "teacher1"
    rewrite_text: str | None = None
    rationale: str | None = None


class AssignRequest(BaseModel):
    owner_id: str


class ContractUpdateRequest(BaseModel):
    yaml_text: str
    created_by: str = "teacher1"


@router.get("/queue")
def get_queue(owner_id: str | None = None) -> dict:
    return {"items": escalation_store.list_open(owner_id=owner_id)}


@router.get("/queue/{item_id}")
def get_queue_item(item_id: str) -> dict:
    item = escalation_store.get(item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Escalation not found")


@router.post("/queue/{item_id}/assign")
def assign_queue_item(item_id: str, payload: AssignRequest) -> dict:
    item = escalation_store.assign(item_id, payload.owner_id)
    if not item:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return item


@router.post("/queue/{item_id}/action")
async def queue_action(item_id: str, payload: QueueActionRequest) -> dict:
    item = escalation_store.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Escalation not found")
    if payload.action in SENSITIVE_ACTIONS and not (payload.rationale or payload.note):
        raise HTTPException(status_code=400, detail="Rationale required for sensitive actions")

    action_result = apply_teacher_action(
        action=payload.action,
        escalation_id=item_id,
        teacher_id=payload.teacher_id,
        contract_path=str(CONTRACT_PATH),
        patch_log=patch_log,
        rewrite_text=payload.rewrite_text,
        rationale=payload.rationale or payload.note,
    )

    if payload.action == "rewrite" and payload.rewrite_text:
        teacher_reply_store.enqueue(
            escalation_id=item_id,
            session_id=item["session_id"],
            turn_number=int(item.get("turn_number", 0)),
            teacher_id=payload.teacher_id,
            reply_text=payload.rewrite_text,
        )

    escalation_store.resolve(
        escalation_id=item_id,
        action=payload.action,
        teacher_id=payload.teacher_id,
        rationale=payload.rationale or payload.note,
    )
    await broadcaster.publish({"event": "queue_updated", "item_id": item_id, "action": payload.action})
    return {"escalation_id": item_id, "note": payload.note, **action_result}


@router.post("/queue/simulate")
async def simulate_queue_item() -> dict:
    item_id = f"sim-{int(datetime.now(UTC).timestamp())}"
    item = escalation_store.push(
        escalation_id=item_id,
        session_id="simulated-session",
        turn_number=0,
        payload={"student_input": "Simulated escalation", "verify_action": "withhold"},
        priority="high",
        reason="simulated_escalation",
    )
    await broadcaster.publish({"event": "queue_updated", "item_id": item_id, "action": "created"})
    return item


@router.get("/students")
def students() -> dict:
    return {"students": session_store.list_students()}


@router.get("/students/mastery-heatmap")
def mastery_heatmap() -> dict:
    from sqlalchemy import select

    from eduharness.memory.schema import LearnerState

    with session_factory() as db:
        rows = db.execute(select(LearnerState)).scalars().all()
    heatmap_rows = [{"studentId": row.student_id, "mastery": dict(row.mastery or {})} for row in rows]
    return {"rows": heatmap_rows}


@router.get("/students/{student_id}")
def student_detail(student_id: str) -> dict:
    return session_store.get_student_detail(student_id, escalation_store)


@router.get("/audit")
def audit() -> dict:
    events: list[dict] = []
    patch_path = Path("evaluation/data/results/patch_log.jsonl")
    if patch_path.exists():
        for idx, line in enumerate(patch_path.read_text(encoding="utf-8").splitlines(), start=1):
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
                        "rationale": record.get("rationale", ""),
                    }
                )
    return {"events": events}


@router.get("/contract")
def get_contract() -> dict:
    return {"yaml_text": CONTRACT_PATH.read_text(encoding="utf-8") if CONTRACT_PATH.exists() else ""}


@router.put("/contract")
def update_contract(payload: ContractUpdateRequest) -> dict:
    data = yaml.safe_load(payload.yaml_text) or {}
    yaml_text = yaml.safe_dump(data, sort_keys=False)
    version = policy_versioning.save_version(yaml_text, created_by=payload.created_by)
    return {"updated": True, "version": version}


@router.get("/contract/versions")
def contract_versions() -> dict:
    return {"versions": policy_versioning.list_versions()}


@router.post("/contract/rollback")
def rollback_contract(version_tag: str | None = None) -> dict:
    return policy_versioning.rollback(version_tag)


@router.get("/reports/summary")
def summary() -> dict:
    kpis = escalation_store.kpi_summary()
    kpis["active_model_key"] = get_active_model_key()
    kpis["model_metadata"] = registry.metadata(get_active_model_key())
    return kpis


@router.get("/reports/pdf")
def summary_pdf() -> Response:
    summary_data = summary()
    model_meta = summary_data.pop("model_metadata", registry.metadata(get_active_model_key()))
    pdf_bytes = generate_summary_pdf(
        title="EduHarness Teacher Summary Report",
        summary=summary_data,
        model_metadata=model_meta,
        output_path="evaluation/data/results/teacher_summary_report.pdf",
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="teacher_summary_report.pdf"'},
    )
