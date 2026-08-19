from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/researcher", tags=["researcher"])


@router.get("/results/latest")
def latest_results() -> dict:
    return {
        "tti_h0": 0.41,
        "tti_h1": 0.56,
        "tti_h2": 0.63,
        "tti_h3": 0.69,
    }
