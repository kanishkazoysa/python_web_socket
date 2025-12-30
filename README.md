# Python FastAPI Backend

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health check: `GET /health`
- WebSocket echo: `ws://localhost:8000/ws`
# python_web_socket
