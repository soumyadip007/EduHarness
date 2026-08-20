from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from api.services import get_active_model_key, registry, set_active_model_key

router = APIRouter(prefix="/api/config", tags=["config"])


class ActiveModelRequest(BaseModel):
    model_key: str


@router.get("/models")
def list_models() -> dict:
    return {
        "models": registry.list_models(),
        "active_model_key": get_active_model_key(),
    }


@router.put("/models/active")
def update_active_model(payload: ActiveModelRequest) -> dict:
    try:
        meta = set_active_model_key(payload.model_key)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"active_model_key": payload.model_key, "metadata": meta}
