# D1: two stages. The workshop installs the toolboxes; only the finished result goes live.
FROM python:3.12-slim AS workshop
COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /bin/uv
RUN uv venv /venv && uv pip install --python /venv/bin/python fastapi==0.141.1 uvicorn==0.53.0

FROM python:3.12-slim AS lunchbox
COPY --from=workshop /venv /venv
WORKDIR /app
COPY meter.py service.py ./
CMD ["/venv/bin/uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
