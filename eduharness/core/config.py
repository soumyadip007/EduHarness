from pathlib import Path

import yaml

from eduharness.core.exceptions import ConfigError


class ConfigLoader:
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)

    def load_yaml(self, relative_path: str) -> dict:
        path = self.base_dir / relative_path
        if not path.exists():
            raise ConfigError(f"Config not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ConfigError(f"Expected mapping in config: {path}")
        return data
