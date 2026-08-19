from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class ModelConfig:
    provider: str
    model_id: str
    temperature: float = 0.2
    max_tokens: int = 700


class LLMClient:
    """Minimal provider-agnostic chat client.

    Uses real APIs when keys are present, otherwise returns a deterministic
    local fallback so tests and local scaffolding can run without keys.
    """

    def __init__(self, config: ModelConfig, timeout_s: float = 30.0) -> None:
        self.config = config
        self.timeout_s = timeout_s

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        provider = self.config.provider.lower()
        if provider == "openai" and os.getenv("OPENAI_API_KEY"):
            return self._chat_openai(system_prompt, user_prompt)
        if provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
            return self._chat_anthropic(system_prompt, user_prompt)
        return self._fallback_response(user_prompt)

    def _chat_openai(self, system_prompt: str, user_prompt: str) -> str:
        payload: dict[str, Any] = {
            "model": self.config.model_id,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        }
        with httpx.Client(timeout=self.timeout_s) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _chat_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        payload: dict[str, Any] = {
            "model": self.config.model_id,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        headers = {
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        with httpx.Client(timeout=self.timeout_s) as client:
            resp = client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        return data["content"][0]["text"]

    def _fallback_response(self, user_prompt: str) -> str:
        return (
            "Let's solve this step-by-step. "
            f"You asked: {user_prompt[:120]}"
        )
