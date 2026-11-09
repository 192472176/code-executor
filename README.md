# Multi-Language Remote Code Execution Engine

A fast, lightweight code execution REST API built with Python, FastAPI, and Subprocess. Designed to model the infrastructure core of online assessment platforms like HackerRank.

## Features
- **Multi-Language Support**: Executes arbitrary Python 3 and C++ code.
- **Isolated Workspace**: Uses dynamic temporary directories (`tempfile`) for C++ source compilation and binary execution.
- **Resource Constraints**: Implements subprocess timeout enforcement (5s execution cap) to mitigate infinite loops.
- **Interactive Documentation**: Auto-generated Swagger/OpenAPI documentation provided via FastAPI.

## Tech Stack
- **Language**: Python 3.12
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Compiler Support**: GNU C++ Compiler (`g++`)

## API Endpoints

### `POST /run`
Executes provided code in the specified language environment.

**Request Body:**
```json
{
  "language": "python",
  "code": "print('Hello World!')"
}
```
**Response Body:**
```json
{
  "stdout": "Hello World!\n",
  "stderr": "",
  "exit_code": 0
}
```
## Setup & Running Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/192472176/code-executor.git
   cd code-executor
