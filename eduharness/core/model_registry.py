from __future__ import annotations

import os
from pathlib import Path

import yaml

from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.core.exceptions import ConfigError

DEFAULT_REGISTRY_PATH = Path("configs/models/model_registry.yaml")
ACTIVE_MODEL_ENV = "ACTIVE_MODEL_KEY"


class ModelRegistry:
    """Load model profiles from YAML and resolve runtime ModelConfig."""

    def __init__(self, registry_path: str | Path = DEFAULT_REGISTRY_PATH) -> None:
        self.registry_path = Path(registry_path)
        self._models: dict[str, dict] = {}
        self.reload()

    def reload(self) -> None:
        if not self.registry_path.exists():
            raise ConfigError(f"Model registry not found: {self.registry_path}")
        data = yaml.safe_load(self.registry_path.read_text(encoding="utf-8")) or {}
        models = data.get("models", {})
        if not isinstance(models, dict) or not models:
            raise ConfigError("Model registry must define at least one model under 'models'")
        self._models = models

    def list_models(self) -> list[dict]:
        return [
            {
                "key": key,
                "provider": cfg.get("provider", ""),
                "model_id": cfg.get("model_id", ""),
                "temperature": cfg.get("temperature", 0.2),
                "max_tokens": cfg.get("max_tokens", 700),
                "label": cfg.get("label", key),
                "open_source": bool(cfg.get("open_source", False)),
            }
            for key, cfg in self._models.items()
        ]

    def keys(self) -> list[str]:
        return list(self._models.keys())

    def validate_key(self, key: str) -> None:
        if key not in self._models:
            raise ConfigError(f"Unknown model key '{key}'. Available: {', '.join(self.keys())}")

    def get_active_key(self, override: str | None = None) -> str:
        key = override or os.getenv(ACTIVE_MODEL_ENV) or next(iter(self._models))
        self.validate_key(key)
        return key

    def get_config(self, key: str | None = None) -> ModelConfig:
        resolved = self.get_active_key(key)
        raw = self._models[resolved]
        return ModelConfig(
            provider=str(raw.get("provider", "openai")),
            model_id=str(raw.get("model_id", "gpt-4o-mini")),
            temperature=float(raw.get("temperature", 0.2)),
            max_tokens=int(raw.get("max_tokens", 700)),
        )

    def get_client(self, key: str | None = None) -> LLMClient:
        return LLMClient(self.get_config(key))

    def metadata(self, key: str | None = None) -> dict:
        resolved = self.get_active_key(key)
        cfg = self._models[resolved]
        return {
            "model_key": resolved,
            "provider": cfg.get("provider", ""),
            "model_id": cfg.get("model_id", ""),
            "open_source": bool(cfg.get("open_source", False)),
        }


_registry: ModelRegistry | None = None


def get_model_registry() -> ModelRegistry:
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
