from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys
import tempfile
import os

app = FastAPI()

class CodeExecutionRequest(BaseModel):
    language: str  # "python" or "cpp"
    code: str

@app.post("/run")
def run_code(request: CodeExecutionRequest):
    if request.language == "python":
        try:
            result = subprocess.run(
                [sys.executable, "-c", request.code],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "Execution timed out (5s limit)"}

    elif request.language == "cpp":
        with tempfile.TemporaryDirectory() as temp_dir:
            cpp_file = os.path.join(temp_dir, "solution.cpp")
            exe_file = os.path.join(temp_dir, "solution.exe")

            with open(cpp_file, "w") as f:
                f.write(request.code)

            # Compile C++ code
            compile_res = subprocess.run(["g++", cpp_file, "-o", exe_file], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"error": "Compilation Error", "stderr": compile_res.stderr}

            # Run compiled executable
            try:
                run_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                return {"stdout": run_res.stdout, "stderr": run_res.stderr, "exit_code": run_res.returncode}
            except subprocess.TimeoutExpired:
                return {"error": "Execution timed out (5s limit)"}

    return {"error": "Unsupported language"}