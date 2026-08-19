from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class CodeRunResult:
    stdout: str
    stderr: str
    return_code: int


def run_python_code(source_code: str, timeout_s: int = 5) -> CodeRunResult:
    proc = subprocess.run(
        ["python3", "-c", source_code],
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )
    return CodeRunResult(stdout=proc.stdout, stderr=proc.stderr, return_code=proc.returncode)
