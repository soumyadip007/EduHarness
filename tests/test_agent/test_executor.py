from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever


def test_executor_returns_response() -> None:
    client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
    retriever = CourseRetriever("course_content/modules")
    executor = AgentExecutor(client, retriever)
    out = executor.run(ExecutorInput(student_input="Explain loops in python"))
    assert len(out) > 10
