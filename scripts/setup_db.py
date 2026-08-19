from __future__ import annotations

from eduharness.memory.schema import build_session_factory


if __name__ == "__main__":
    build_session_factory("sqlite:///eduharness.db")
    print("Initialized DB and ensured tables exist.")
