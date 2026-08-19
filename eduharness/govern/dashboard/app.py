from __future__ import annotations

from fastapi import FastAPI

from eduharness.govern.escalation_queue import EscalationQueue

app = FastAPI(title="EduHarness Teacher Dashboard", version="0.1.0")
queue = EscalationQueue()


@app.get("/queue")
def review_queue() -> dict:
    return {"items": queue.list_items(), "count": queue.size()}


@app.get("/evidence/{escalation_id}")
def evidence_viewer(escalation_id: str) -> dict:
    for item in queue.list_items():
        if item["escalation_id"] == escalation_id:
            return item
    return {"error": "not_found", "escalation_id": escalation_id}


@app.get("/actions")
def action_buttons() -> dict:
    return {"actions": ["approve", "rewrite", "freeze_topic", "patch_rule"]}


@app.get("/policy")
def patch_editor() -> dict:
    return {"message": "Policy editor endpoint placeholder"}


@app.get("/audit")
def audit_trail() -> dict:
    return {"message": "Audit trail endpoint placeholder"}
