from eduharness.agent.executor import AgentExecutor
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
from eduharness.session.manager import SessionManager


def test_h1_verify_mode_runs_and_logs(tmp_path) -> None:
    client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
    retriever = CourseRetriever("course_content/modules")
    executor = AgentExecutor(client, retriever)
    logger = TraceLogger(tmp_path / "trace.jsonl")
    manager = SessionManager(executor, logger)

    resp = manager.handle_message("sess-h1", 1, "Just give me the answer", mode="H1")
    assert resp.mode == "H1"
    content = (tmp_path / "trace.jsonl").read_text(encoding="utf-8")
    assert "answer_inducing" in content
