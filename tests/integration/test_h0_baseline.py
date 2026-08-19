from eduharness.agent.executor import AgentExecutor
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
from eduharness.session.manager import SessionManager


def test_h0_end_to_end(tmp_path) -> None:
    client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
    retriever = CourseRetriever("course_content/modules")
    executor = AgentExecutor(client, retriever)
    logger = TraceLogger(tmp_path / "trace.jsonl")
    manager = SessionManager(executor, logger)

    resp = manager.handle_message("sessionA", 1, "What is a for loop?")
    assert resp.response
    assert (tmp_path / "trace.jsonl").exists()
