# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run backend API
uvicorn src.api.main:app --reload

# Run frontend UI (separate terminal)
streamlit run src/ui/app.py

# Run with Docker (both services together)
docker-compose up --build

# Run all mock tests (no API keys needed — use this in CI)
.\venv\python.exe -m pytest tests/test_tools.py -v -m "not real_api"

# Run a single test
.\venv\python.exe -m pytest tests/test_tools.py::TestCalculator::test_simple_multiplication -v

# Run real API tests (requires .env with keys)
.\venv\python.exe -m pytest tests/test_tools.py -v -m "real_api"
```

## Architecture

The agent follows a **ReAct loop**: user query → LLM decides tool(s) → tools execute → result fed back to LLM → repeat until final answer.

```
User Query
    ↓
POST /chat  (src/api/main.py)
    ↓
run_agent() (src/agent/agent_loop.py)
    ↓ iterates up to MAX_ITERATIONS
LLM (GPT-4o-mini) ──tool_calls──→ execute_tool() (src/agent/tool_registry.py)
                                        ↓
                              get_weather / calculator / web_search
                                   (src/tools/)
    ↓ no more tool_calls
Final Answer → ChatResponse
```

**Key files:**

- `src/agent/agent_loop.py` — the loop itself; `run_agent()` is the core entry point
- `src/agent/tool_registry.py` — `AVAILABLE_TOOLS` dict maps tool name strings to functions; `execute_tool()` dispatches calls
- `src/agent/tool_schemas.py` — OpenAI function-calling schemas; LLM reads these to decide which tool to call and with what args
- `src/config/settings.py` — singleton `settings` instance; all env vars loaded here once via `python-dotenv`
- `src/api/main.py` — FastAPI app; calls `settings.validate()` at startup and exits if any API key is missing

## Adding a New Tool

1. Create `src/tools/mytool_tool.py` with a single function returning `str`
2. Add the OpenAI function schema to `src/agent/tool_schemas.py` (in `TOOLS_SCHEMA` list)
3. Register in `src/agent/tool_registry.py` → `AVAILABLE_TOOLS`
4. Add mock + real test classes to `tests/test_tools.py` (follow the template at the bottom of that file)

## Testing Strategy

- **Mock tests** (`TestXxxMock`) — patch `requests.get/post`, always run in CI, no API keys needed
- **Real tests** (`TestXxxReal`) — marked `@pytest.mark.real_api`, auto-skipped in CI via `-m "not real_api"`
- **Calculator** — pure Python, no mocking needed
- CI runs: `pytest tests/test_tools.py -v --tb=short -m "not real_api"` (see `.github/workflows/ci.yml`)

## Environment Variables

Required in `.env`:
```
OPENAI_API_KEY=
OPENWEATHER_API_KEY=
TAVILY_API_KEY=
MAX_ITERATIONS=5
LOG_LEVEL=INFO
```

`settings.validate()` raises `ValueError` and exits the process if any key is empty — so the API will not start with missing keys.

## Deployment

- **Backend** deployed on Render (auto-deploys on push to `main` after CI passes)
- **Frontend** deployed on Render separately; uses `BACKEND_URL` env var to reach the API
- Docker Compose runs both locally on ports `8000` (API) and `8501` (UI)
- Swagger docs available at `http://localhost:8000/docs` when running locally

## Knowledge Graph — MANDATORY RULE

**BEFORE any task**, ALWAYS read:
`graphify-out/GRAPH_REPORT.md`

- This is your PRIMARY source for codebase understanding
- Do NOT scan directories or read random files first
- Only open specific files if graph report is insufficient
  AND user explicitly asks
