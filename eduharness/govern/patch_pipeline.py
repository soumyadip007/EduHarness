from __future__ import annotations

from pathlib import Path

import yaml

from eduharness.govern.patch_log import PatchLog


ALLOWED_ACTIONS = {"approve", "rewrite", "freeze_topic", "patch_rule"}


def apply_teacher_action(
    action: str,
    escalation_id: str,
    teacher_id: str,
    contract_path: str,
    patch_log: PatchLog,
    rewrite_text: str | None = None,
    patch_rule: dict | None = None,
) -> dict:
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Unsupported action: {action}")

    result = {"action": action, "escalation_id": escalation_id, "teacher_id": teacher_id, "applied": True}

    if action == "rewrite":
        result["rewrite_text"] = rewrite_text or ""

    if action == "patch_rule":
        if not patch_rule or "path" not in patch_rule or "value" not in patch_rule:
            raise ValueError("patch_rule requires path and value")

        contract_file = Path(contract_path)
        data = yaml.safe_load(contract_file.read_text(encoding="utf-8")) or {}

        path_parts = patch_rule["path"].split(".")
        node = data
        for part in path_parts[:-1]:
            if part not in node or not isinstance(node[part], dict):
                node[part] = {}
            node = node[part]

        node[path_parts[-1]] = patch_rule["value"]
        contract_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        result["patched_path"] = patch_rule["path"]

    patch_log.append(result)
    return result
