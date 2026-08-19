from eduharness.agent.executor import AgentExecutor
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
from eduharness.session.manager import SessionManager


def test_h2_persists_state_across_turns(tmp_path) -> None:
    client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
    retriever = CourseRetriever("course_content/modules")
    executor = AgentExecutor(client, retriever)
    logger = TraceLogger(tmp_path / "trace.jsonl")
    manager = SessionManager(executor, logger)

    manager.handle_message("student-1", 1, "I need help with loops", mode="H2")
    manager.handle_message("student-1", 2, "I understand loops now", mode="H2")

    content = (tmp_path / "trace.jsonl").read_text(encoding="utf-8")
    assert '"layer_label": "memory"' in content
    assert '"memory_update": {' in content
