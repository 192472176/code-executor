import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodeExecutionRequest(BaseModel):
    language: str
    code: str

DOCKER_IMAGE = "execution-sandbox"

@app.post("/run")
def run_code(request: CodeExecutionRequest):
    if request.language not in ["python", "cpp"]:
        return {"error": "Unsupported language"}

    if request.language == "python":
        docker_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            DOCKER_IMAGE,
            "python3", "-"
        ]
    elif request.language == "cpp":
        docker_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            DOCKER_IMAGE,
            "sh", "-c", "cat > code.cpp && g++ code.cpp -o app && ./app"
        ]

    try:
        run_res = subprocess.run(
            docker_cmd,
            input=request.code,
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "stdout": run_res.stdout,
            "stderr": run_res.stderr,
            "exit_code": run_res.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out (5s limit)"}