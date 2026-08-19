from eduharness.agent.tools.course_retriever import CourseRetriever


def test_retrieve_returns_matching_content() -> None:
    retriever = CourseRetriever("course_content/modules")
    out = retriever.retrieve("for loop")
    assert "loops" in out.lower()
