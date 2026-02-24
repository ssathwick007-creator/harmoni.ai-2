# harmoni.ai-2

A minimal runnable starter service so this repository works out-of-the-box.

## What is included

- A small HTTP service with JSON responses.
- Endpoints:
  - `GET /` : service info
  - `GET /health` : health check
- Unit tests for the core endpoints.

## Quick start

### 1) Run the service

```bash
PYTHONPATH=src python -m harmoni_ai --host 127.0.0.1 --port 8000
```

Then open:
- <http://127.0.0.1:8000/>
- <http://127.0.0.1:8000/health>

### 2) Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Next recommended steps

1. Add request/response schemas for real product APIs.
2. Add structured logging and configuration via environment variables.
3. Add CI (format/lint/test) so every commit is validated automatically.
4. Add Docker support once runtime dependencies are finalized.


## UI preview

A clean standalone UI is available at `ui/index.html` and does not modify backend behavior.

Open it directly in a browser:

```bash
xdg-open ui/index.html
```
