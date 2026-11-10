# Multi-Language Remote Code Execution Engine

A production-grade, secure, and isolated Remote Code Execution (RCE) API built with Python, FastAPI, and Docker. Designed to mirror online judge platforms like HackerRank and LeetCode, this engine safely compiles and executes untrusted code inside sandboxed ephemeral containers with strict resource and security constraints.

---

## Features

- **Multi-Language Support**: Compiles and executes Python 3 and C++ (via `g++`) source code.
- **Docker Container Sandboxing**: Executes user code inside ephemeral containers to isolate host file systems.
- **Network Isolation**: Blocks outbound and inbound network access using `--network none`.
- **Resource Limits**: Restricts memory (`128m`) and CPU cores (`0.5`) to prevent Denial-of-Service (DoS) and infinite loop exploits.
- **Stdin Streaming**: Streams source code directly into containers via `stdin` to eliminate volume mounting overhead on Windows host environments.
- **Execution Telemetry**: Captures standard output (`stdout`), standard error (`stderr`), and process exit codes.
- **Interactive Documentation**: Provides auto-generated Swagger/OpenAPI documentation via FastAPI.

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
Executes provided source code within a sandboxed Docker container.

**Request Body:**
```json
{
  "language": "python",
  "code": "print('Hello World!')"
}