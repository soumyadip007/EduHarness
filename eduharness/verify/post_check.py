from __future__ import annotations


def post_check_output(verify_action: str, output: str) -> str:
    text = output.lower()
    if verify_action.startswith("withhold") and any(k in text for k in ("here is the full code", "final answer", "def ")):
        return "block"
    if verify_action.startswith("hint") and "final answer" in text:
        return "rewrite"
    return "pass"
