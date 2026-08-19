from eduharness.agent.llm_client import LLMClient, ModelConfig


def test_llm_fallback_response_when_no_keys() -> None:
    client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
    out = client.chat("system", "How do loops work?")
    assert "step-by-step" in out
