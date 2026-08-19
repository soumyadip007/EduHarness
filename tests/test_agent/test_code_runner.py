from eduharness.agent.tools.code_runner import run_python_code


def test_run_python_code_success() -> None:
    result = run_python_code("print(2 + 3)")
    assert result.return_code == 0
    assert result.stdout.strip() == "5"
