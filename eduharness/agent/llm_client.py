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
        self.last_call_metadata: dict = {}

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        import time

        start = time.perf_counter()
        provider = self.config.provider.lower()
        used_live_api = False
        if provider == "openai" and os.getenv("OPENAI_API_KEY"):
            result = self._chat_openai_compatible(
                "https://api.openai.com/v1/chat/completions",
                os.environ["OPENAI_API_KEY"],
                system_prompt,
                user_prompt,
            )
            used_live_api = True
        elif provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
            result = self._chat_anthropic(system_prompt, user_prompt)
            used_live_api = True
        elif provider == "groq" and os.getenv("GROQ_API_KEY"):
            result = self._chat_openai_compatible(
                "https://api.groq.com/openai/v1/chat/completions",
                os.environ["GROQ_API_KEY"],
                system_prompt,
                user_prompt,
            )
            used_live_api = True
        elif provider == "openrouter" and os.getenv("OPENROUTER_API_KEY"):
            result = self._chat_openai_compatible(
                "https://openrouter.ai/api/v1/chat/completions",
                os.environ["OPENROUTER_API_KEY"],
                system_prompt,
                user_prompt,
                extra_headers={"HTTP-Referer": "https://eduharness.local", "X-Title": "EduHarness"},
            )
            used_live_api = True
        elif provider == "ollama":
            result = self._chat_ollama(system_prompt, user_prompt)
            used_live_api = True
        else:
            result = self._fallback_response(user_prompt)

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        self.last_call_metadata = {
            "provider": provider,
            "model_id": self.config.model_id,
            "latency_ms": elapsed_ms,
            "tokens_used": {"prompt": len(user_prompt.split()), "completion": len(result.split())},
            "live_api": used_live_api,
        }
        return result

    def _chat_openai_compatible(
        self,
        url: str,
        api_key: str,
        system_prompt: str,
        user_prompt: str,
        extra_headers: dict[str, str] | None = None,
    ) -> str:
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
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)
        with httpx.Client(timeout=self.timeout_s) as client:
            resp = client.post(url, json=payload, headers=headers)
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

    def _chat_ollama(self, system_prompt: str, user_prompt: str) -> str:
        base_url = os.getenv("LOCAL_MODEL_BASE_URL", "http://localhost:11434").rstrip("/")
        payload = {
            "model": self.config.model_id,
            "stream": False,
            "options": {"temperature": self.config.temperature},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        with httpx.Client(timeout=self.timeout_s) as client:
            resp = client.post(f"{base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("message", {}).get("content", self._fallback_response(user_prompt))

    def _fallback_response(self, user_prompt: str) -> str:
        return (
            "Let's solve this step-by-step. "
            f"You asked: {user_prompt[:120]}"
        )
