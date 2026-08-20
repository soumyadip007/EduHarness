from __future__ import annotations

from pathlib import Path

from eduharness.audit.trace_logger import TraceLogger
from eduharness.core.app_settings import AppSettingsStore
from eduharness.core.model_registry import get_model_registry
from eduharness.core.session_store import SessionStore
from eduharness.govern.escalation_store import EscalationStore
from eduharness.govern.patch_log import PatchLog
from eduharness.govern.policy_versioning import PolicyVersioning
from eduharness.govern.teacher_reply_store import TeacherReplyStore
from eduharness.memory.schema import build_session_factory
from eduharness.session.manager import SessionManager
from evaluation.analysis.stats import ExperimentManifestStore

DB_URL = "sqlite:///eduharness.db"
CONTRACT_PATH = Path("configs/contracts/default_contract.yaml")
PATCH_LOG_PATH = "evaluation/data/results/patch_log.jsonl"
ACTIVE_MODEL_SETTING = "active_model_key"

session_factory = build_session_factory(DB_URL)
registry = get_model_registry()
settings_store = AppSettingsStore(session_factory)
escalation_store = EscalationStore(session_factory)
session_store = SessionStore(session_factory)
teacher_reply_store = TeacherReplyStore(session_factory)
policy_versioning = PolicyVersioning(session_factory, CONTRACT_PATH)
patch_log = PatchLog(PATCH_LOG_PATH)
manifest_store = ExperimentManifestStore(session_factory)
trace_logger = TraceLogger("evaluation/data/results/api_student_trace.jsonl")


def get_active_model_key() -> str:
    stored = settings_store.get(ACTIVE_MODEL_SETTING, "")
    if stored:
        try:
            registry.validate_key(stored)
            return stored
        except Exception:
            pass
    return registry.get_active_key()


def set_active_model_key(key: str) -> dict:
    registry.validate_key(key)
    settings_store.set(ACTIVE_MODEL_SETTING, key)
    return registry.metadata(key)


_manager: SessionManager | None = None


def get_session_manager() -> SessionManager:
    global _manager
    if _manager is None:
        _manager = SessionManager(trace_logger=trace_logger, model_key=get_active_model_key())
    return _manager
