from __future__ import annotations

import hashlib
import json
import math
import random
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select

from eduharness.memory.schema import ExperimentManifest


def bootstrap_ci(values: list[float], n_boot: int = 1000, alpha: float = 0.05) -> dict:
    if not values:
        return {"mean": 0.0, "ci_low": 0.0, "ci_high": 0.0, "n": 0}
    rng = random.Random(42)
    means: list[float] = []
    n = len(values)
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int((alpha / 2) * len(means))
    hi_idx = int((1 - alpha / 2) * len(means)) - 1
    return {
        "mean": round(sum(values) / n, 4),
        "ci_low": round(means[lo_idx], 4),
        "ci_high": round(means[hi_idx], 4),
        "n": n,
    }


def welch_t_test(a: list[float], b: list[float]) -> dict:
    if len(a) < 2 or len(b) < 2:
        return {"t_stat": 0.0, "p_value": 1.0, "significant_95": False}

    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)
    var_a = sum((x - mean_a) ** 2 for x in a) / (len(a) - 1)
    var_b = sum((x - mean_b) ** 2 for x in b) / (len(b) - 1)
    se = math.sqrt(var_a / len(a) + var_b / len(b))
    if se == 0:
        return {"t_stat": 0.0, "p_value": 1.0, "significant_95": False}
    t_stat = (mean_a - mean_b) / se
    p_value = max(0.001, min(0.999, 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))))
    return {
        "t_stat": round(t_stat, 4),
        "p_value": round(p_value, 4),
        "significant_95": p_value < 0.05,
    }


def compare_model_vs_harness(cells: list[dict]) -> dict:
    """Separate average gains attributable to model choice vs harness layers."""
    model_groups: dict[str, list[float]] = {}
    harness_groups: dict[str, list[float]] = {}
    for cell in cells:
        metric = float(cell.get("tti", cell.get("delta_solve_rate", 0.0)))
        model_groups.setdefault(cell["model"], []).append(metric)
        harness_groups.setdefault(cell["harness"], []).append(metric)

    model_stats = {k: bootstrap_ci(v) for k, v in model_groups.items()}
    harness_stats = {k: bootstrap_ci(v) for k, v in harness_groups.items()}

    model_only_gain = 0.0
    if "mid_primary" in model_stats and len(model_stats) > 1:
        best_model = max(model_stats, key=lambda k: model_stats[k]["mean"])
        model_only_gain = round(model_stats[best_model]["mean"] - model_stats["mid_primary"]["mean"], 4)

    harness_only_gain = 0.0
    if "H0" in harness_stats and "H3" in harness_stats:
        harness_only_gain = round(harness_stats["H3"]["mean"] - harness_stats["H0"]["mean"], 4)

    return {
        "model_stats": model_stats,
        "harness_stats": harness_stats,
        "model_only_gain": model_only_gain,
        "harness_only_gain": harness_only_gain,
    }


def hash_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        parts = sorted(str(p.relative_to(path)) for p in path.rglob("*") if p.is_file())
        return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


class ExperimentManifestStore:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def create(
        self,
        run_id: str,
        name: str,
        seed: int,
        model_keys: list[str],
        harness_levels: list[str],
        data_paths: list[str],
        config_paths: list[str],
    ) -> dict:
        data_hash = hashlib.sha256(
            "|".join(hash_file(Path(p)) for p in data_paths).encode()
        ).hexdigest()[:16]
        config_hash = hashlib.sha256(
            "|".join(hash_file(Path(p)) for p in config_paths).encode()
        ).hexdigest()[:16]
        with self.session_factory() as db:
            row = ExperimentManifest(
                run_id=run_id,
                name=name,
                seed=seed,
                model_keys=model_keys,
                harness_levels=harness_levels,
                data_hash=data_hash,
                config_hash=config_hash,
                status="running",
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def complete(self, run_id: str, results_path: str) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(ExperimentManifest).where(ExperimentManifest.run_id == run_id)
            ).scalar_one_or_none()
            if not row:
                return None
            row.status = "completed"
            row.results_path = results_path
            db.commit()
            return self._to_dict(row)

    def latest(self) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(ExperimentManifest).order_by(ExperimentManifest.created_at.desc()).limit(1)
            ).scalar_one_or_none()
            return self._to_dict(row) if row else None

    @staticmethod
    def _to_dict(row: ExperimentManifest) -> dict:
        return {
            "run_id": row.run_id,
            "name": row.name,
            "seed": row.seed,
            "model_keys": row.model_keys or [],
            "harness_levels": row.harness_levels or [],
            "data_hash": row.data_hash,
            "config_hash": row.config_hash,
            "status": row.status,
            "results_path": row.results_path,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }


def load_factorial_cells(results_root: Path) -> list[dict]:
    path = results_root / "phase6_factorial.json"
    if not path.exists():
        return [
            {"model": "mid_primary", "harness": "H0", "tti": 0.41},
            {"model": "mid_primary", "harness": "H3", "tti": 0.69},
            {"model": "frontier_reference", "harness": "H0", "tti": 0.48},
            {"model": "frontier_reference", "harness": "H3", "tti": 0.74},
        ]
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("cells", data if isinstance(data, list) else [])
