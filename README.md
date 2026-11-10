# Multi-Language Remote Code Execution Engine

A production-grade, secure, and isolated Remote Code Execution (RCE) API built with Python, FastAPI, and Docker. Designed to mirror online judge platforms like HackerRank and LeetCode, this engine safely compiles and executes untrusted code inside sandboxed ephemeral containers with automated test-case evaluation and verdict generation.

---

## Features

- **Multi-Language Support**: Compiles and executes Python 3 and C++ (via `g++`) source code.
- **Test Case & Verdict Engine**: Evaluates submissions against multiple test cases and returns online judge verdicts:
  - **`AC`** (Accepted)
  - **`WA`** (Wrong Answer)
  - **`TLE`** (Time Limit Exceeded)
  - **`CE` / `RE`** (Compilation Error / Runtime Error)
- **Docker Container Sandboxing**: Executes user code inside ephemeral containers to isolate host file systems.
- **Network Isolation**: Blocks outbound and inbound network access using `--network none`.
- **Resource Limits**: Restricts memory (`128m`) and CPU cores (`0.5`) to prevent Denial-of-Service (DoS) and infinite loop exploits.
- **Stdin Streaming**: Streams source code directly into containers via `stdin` to eliminate volume mounting overhead on Windows host environments.
- **Interactive Documentation**: Auto-generated Swagger/OpenAPI documentation via FastAPI.

---

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Containerization**: Docker
- **Compiler Support**: GNU C++ Compiler (`g++`)

---

## API Endpoints

### `POST /run`
Evaluates source code against an array of test cases inside a sandboxed Docker container.

**Request Body:**
```json
{
  "language": "python",
  "code": "a, b = map(int, input().split())\nprint(a + b)",
  "test_cases": [
    {
      "input": "2 3",
      "expected_output": "5"
    },
    {
      "input": "10 20",
      "expected_output": "30"
    }
  ]
}