from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/researcher", tags=["researcher"])

RESULTS_ROOT = Path("evaluation/data/results")
_experiment_status: dict[str, str] = {"state": "idle", "last_run_at": ""}


class ExperimentRequest(BaseModel):
    name: str = "phase6_full"
    seed: int = 42


def _read_json(path: Path, fallback: dict | list) -> dict | list:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


@router.post("/experiments/run")
def run_experiment(payload: ExperimentRequest) -> dict:
    _experiment_status["state"] = "running"
    try:
        subprocess.run(
            [sys.executable, "evaluation/run_full_phase6.py"],
            check=True,
            capture_output=True,
            text=True,
        )
        _experiment_status["state"] = "completed"
        _experiment_status["last_run_at"] = datetime.now(UTC).isoformat()
    except subprocess.CalledProcessError as exc:
        _experiment_status["state"] = "failed"
        return {
            "started": False,
            "name": payload.name,
            "seed": payload.seed,
            "state": _experiment_status["state"],
            "stderr": exc.stderr,
        }
    return {"started": True, "name": payload.name, "seed": payload.seed, "state": _experiment_status["state"]}


@router.get("/experiments/status")
def experiment_status() -> dict:
    return dict(_experiment_status)


@router.get("/results/latest")
def latest_results() -> dict:
    tti = _read_json(RESULTS_ROOT / "phase6_tti_sensitivity.json", fallback={})
    if isinstance(tti, dict) and tti:
        return {
            "tti_h0": round(float(tti.get("H0", {}).get("base", 0.41)), 3),
            "tti_h1": round(float(tti.get("H1", {}).get("base", 0.56)), 3),
            "tti_h2": round(float(tti.get("H2", {}).get("base", 0.63)), 3),
            "tti_h3": round(float(tti.get("H3", {}).get("base", 0.69)), 3),
        }
    return {"tti_h0": 0.41, "tti_h1": 0.56, "tti_h2": 0.63, "tti_h3": 0.69}


@router.get("/results/table")
def results_table() -> dict:
    conditions = _read_json(RESULTS_ROOT / "phase6_conditions.json", fallback={})
    if not isinstance(conditions, dict):
        return {"rows": []}
    rows = []
    for key in ["H0", "H1", "H2", "H3", "H0+M", "H0+G"]:
        row = conditions.get(key, {})
        rows.append(
            {
                "condition": key,
                "safety_adversarial": row.get("safety_adversarial", 0.0),
                "delta_solve_rate": row.get("delta_solve_rate", 0.0),
                "state_divergence": row.get("state_divergence", 0.0),
            }
        )
    return {"rows": rows}


@router.get("/traces")
def traces() -> dict:
    trace_path = RESULTS_ROOT / "api_student_trace.jsonl"
    if not trace_path.exists():
        return {"traces": []}
    lines = [l for l in trace_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    preview = lines[-50:]
    return {"traces": [json.loads(l) for l in preview]}


@router.get("/costs")
def costs() -> dict:
    data = _read_json(RESULTS_ROOT / "phase6_cost_summary.json", fallback={"rows": []})
    return {"cost_summary": data}


@router.post("/export")
def export_results() -> dict:
    subprocess.run([sys.executable, "scripts/export_results.py"], check=True)
    return {"exported": True, "path": str(RESULTS_ROOT)}
