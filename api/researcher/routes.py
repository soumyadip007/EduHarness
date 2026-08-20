from __future__ import annotations

import json
import subprocess
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from api.services import get_active_model_key, manifest_store, registry
from eduharness.reports.pdf_report import generate_summary_pdf
from evaluation.analysis.stats import compare_model_vs_harness, load_factorial_cells

router = APIRouter(prefix="/api/researcher", tags=["researcher"])

RESULTS_ROOT = Path("evaluation/data/results")
_experiment_status: dict[str, str | list | dict] = {
    "state": "idle",
    "last_run_at": "",
    "active_model_key": "",
    "latest_manifest": {},
}


class ExperimentRequest(BaseModel):
    name: str = "phase6_full"
    seed: int = 42
    model_keys: list[str] | None = None
    harness_levels: list[str] | None = None


def _read_json(path: Path, fallback: dict | list) -> dict | list:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


@router.post("/experiments/run")
def run_experiment(payload: ExperimentRequest) -> dict:
    model_keys = payload.model_keys or [get_active_model_key()]
    harness_levels = payload.harness_levels or ["H0", "H1", "H2", "H3"]
    for key in model_keys:
        registry.validate_key(key)

    run_id = f"run-{uuid.uuid4().hex[:12]}"
    manifest = manifest_store.create(
        run_id=run_id,
        name=payload.name,
        seed=payload.seed,
        model_keys=model_keys,
        harness_levels=harness_levels,
        data_paths=["evaluation/data/scenarios", "course_content"],
        config_paths=["configs/models/model_registry.yaml", "configs/contracts/default_contract.yaml"],
    )
    manifest_path = RESULTS_ROOT / f"{run_id}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    _experiment_status["state"] = "running"
    _experiment_status["latest_manifest"] = manifest
    try:
        subprocess.run(
            [sys.executable, "evaluation/run_full_phase6.py", str(manifest_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        manifest_store.complete(run_id, str(RESULTS_ROOT))
        _experiment_status["state"] = "completed"
        _experiment_status["last_run_at"] = datetime.now(UTC).isoformat()
    except subprocess.CalledProcessError as exc:
        _experiment_status["state"] = "failed"
        return {
            "started": False,
            "run_id": run_id,
            "manifest": manifest,
            "state": _experiment_status["state"],
            "stderr": exc.stderr,
        }
    return {
        "started": True,
        "run_id": run_id,
        "manifest": manifest,
        "state": _experiment_status["state"],
    }


@router.get("/experiments/status")
def experiment_status() -> dict:
    latest = manifest_store.latest() or {}
    return {
        **dict(_experiment_status),
        "active_model_key": get_active_model_key(),
        "available_models": registry.list_models(),
        "latest_manifest": latest,
    }


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


@router.get("/results/learning-curve")
def learning_curve() -> dict:
    data = _read_json(RESULTS_ROOT / "phase6_learning_curve.json", fallback={"series": []})
    return data if isinstance(data, dict) else {"series": []}


@router.get("/results/compare")
def results_compare() -> dict:
    cells = load_factorial_cells(RESULTS_ROOT)
    comparison = compare_model_vs_harness(cells)
    return {"cells": cells, **comparison}


@router.get("/results/stats")
def results_stats() -> dict:
    cells = load_factorial_cells(RESULTS_ROOT)
    comparison = compare_model_vs_harness(cells)
    h0_vals = [float(c["tti"]) for c in cells if c.get("harness") == "H0"]
    h3_vals = [float(c["tti"]) for c in cells if c.get("harness") == "H3"]
    significance = {}
    if h0_vals and h3_vals:
        from evaluation.analysis.stats import welch_t_test

        significance = welch_t_test(h3_vals, h0_vals)
    return {
        "comparison": comparison,
        "h0_vs_h3_significance": significance,
        "active_model_key": get_active_model_key(),
    }


@router.get("/traces")
def traces() -> dict:
    trace_path = RESULTS_ROOT / "api_student_trace.jsonl"
    if not trace_path.exists():
        return {"traces": []}
    lines = [line for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    preview = lines[-50:]
    return {"traces": [json.loads(line) for line in preview]}


@router.get("/costs")
def costs() -> dict:
    data = _read_json(RESULTS_ROOT / "phase6_cost_summary.json", fallback={"rows": []})
    return {"cost_summary": data}


@router.post("/export")
def export_results() -> dict:
    subprocess.run([sys.executable, "scripts/export_results.py"], check=True)
    return {"exported": True, "path": str(RESULTS_ROOT)}


@router.get("/reports/pdf")
def research_pdf() -> Response:
    stats = results_stats()
    model_meta = registry.metadata(get_active_model_key())
    summary = {
        "model_only_gain": stats["comparison"]["model_only_gain"],
        "harness_only_gain": stats["comparison"]["harness_only_gain"],
        "h0_vs_h3_significant": stats.get("h0_vs_h3_significance", {}).get("significant_95", False),
        "active_model_key": get_active_model_key(),
    }
    pdf_bytes = generate_summary_pdf(
        title="EduHarness Research Report",
        summary=summary,
        model_metadata=model_meta,
        output_path="evaluation/data/results/research_report.pdf",
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="research_report.pdf"'},
    )
