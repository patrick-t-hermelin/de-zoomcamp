FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]