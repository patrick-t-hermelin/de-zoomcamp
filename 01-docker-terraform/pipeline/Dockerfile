FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY 01-docker-terraform/pipeline/pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]