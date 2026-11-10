import subprocess
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DOCKER_IMAGE = "execution-sandbox"

class TestCase(BaseModel):
    input: str
    expected_output: str

class CodeExecutionRequest(BaseModel):
    language: str
    code: str
    test_cases: List[TestCase]

class TestCaseResult(BaseModel):
    test_case: int
    verdict: str  # AC, WA, TLE, RE, CE
    stdout: str
    stderr: str
    expected_output: str

class ExecutionResponse(BaseModel):
    overall_verdict: str
    passed_count: int
    total_count: int
    results: List[TestCaseResult]

def run_single_test_case(language: str, code: str, input_data: str) -> tuple[str, str, int, bool]:
    if language == "python":
        docker_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            DOCKER_IMAGE,
            "python3", "-c", code
        ]
    elif language == "cpp":
        docker_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            DOCKER_IMAGE,
            "sh", "-c", f"cat << 'EOF' > code.cpp\n{code}\nEOF\ng++ code.cpp -o app && ./app"
        ]

    try:
        run_res = subprocess.run(
            docker_cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=8
        )
        return run_res.stdout, run_res.stderr, run_res.returncode, False
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", -1, True

@app.post("/run", response_model=ExecutionResponse)
def run_code(request: CodeExecutionRequest):
    if request.language not in ["python", "cpp"]:
        return ExecutionResponse(
            overall_verdict="RE",
            passed_count=0,
            total_count=len(request.test_cases),
            results=[]
        )

    results = []
    passed_count = 0
    overall_verdict = "AC"

    for idx, tc in enumerate(request.test_cases, start=1):
        stdout, stderr, exit_code, is_timeout = run_single_test_case(
            request.language, request.code, tc.input
        )

        if is_timeout:
            verdict = "TLE"
        elif exit_code != 0:
            verdict = "CE" if "compilation" in stderr.lower() or "error" in stderr.lower() else "RE"
        else:
            actual_clean = stdout.strip()
            expected_clean = tc.expected_output.strip()
            if actual_clean == expected_clean:
                verdict = "AC"
                passed_count += 1
            else:
                verdict = "WA"

        if verdict != "AC" and overall_verdict == "AC":
            overall_verdict = verdict

        results.append(
            TestCaseResult(
                test_case=idx,
                verdict=verdict,
                stdout=stdout,
                stderr=stderr,
                expected_output=tc.expected_output
            )
        )

    return ExecutionResponse(
        overall_verdict=overall_verdict,
        passed_count=passed_count,
        total_count=len(request.test_cases),
        results=results
    )