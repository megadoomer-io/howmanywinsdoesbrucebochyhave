FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY howmanywinsdoesbrucebochyhave/ howmanywinsdoesbrucebochyhave/

FROM python:3.14-slim

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --no-create-home app

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/howmanywinsdoesbrucebochyhave/ howmanywinsdoesbrucebochyhave/
COPY templates/ templates/
COPY static/ static/

USER app
EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "howmanywinsdoesbrucebochyhave:app", "--host", "0.0.0.0", "--port", "8000"]
