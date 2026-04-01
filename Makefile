.PHONY: lint format test build run

lint:
	uv run ruff check
	uv run ruff format --check
	uv run mypy howmanywinsdoesbrucebochyhave/ test/

format:
	uv run ruff check --fix
	uv run ruff format

test:
	uv run pytest -v

build:
	docker build -t howmanywins .

run:
	uv run uvicorn howmanywinsdoesbrucebochyhave:app --host 0.0.0.0 --port 8000 --reload
