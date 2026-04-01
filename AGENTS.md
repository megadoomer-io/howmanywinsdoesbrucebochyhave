# howmanywinsdoesbrucebochyhave

This is a claude-first repository. Claude is the primary developer; humans provide direction and review.

## What This App Does

A FastAPI web app that scrapes Bruce Bochy's career wins from baseball-reference.com and displays the count. Results are cached with a 15-minute TTL.

Live at: https://howmanywinsdoesbrucebochyhave.com

## Tech Stack

| Aspect | Value |
|--------|-------|
| Python | 3.14+ |
| Package manager | uv (pyproject.toml) |
| Framework | FastAPI + uvicorn (port 8000) |
| Linting | ruff |
| Type checking | mypy (strict) |
| Testing | pytest + httpx (async) |
| CI | GitHub Actions (lint-and-test on PRs, publish on push to main) |
| Container registry | GHCR (`ghcr.io/megadoomer-io/howmanywinsdoesbrucebochyhave`) |
| Default branch | main |

## Project Structure

```
howmanywinsdoesbrucebochyhave/
  __init__.py                       # App factory, exports create_app() and app
  howmanywinsdoesbrucebochyhave.py   # Main app: scraping, parsing, FastAPI route
templates/
  index.html                        # Jinja2 template (wins count + refresh time)
static/
  css/styles.css                    # Giants-themed styling
test/
  conftest.py                       # Fixtures: sample HTML, cache clearing
  test_howmanywinsdoesbrucebochyhave.py  # Parsing, caching, and route tests
.github/workflows/
  lint-and-test.yaml                # PR checks: ruff, mypy, pytest
  publish.yaml                      # Build + push to GHCR, update megadoomer-config
docs/plans/                         # Implementation plans
```

## Deployment

- **Cluster**: DigitalOcean (`megadoomer-do`)
- **Namespace**: `howmanywins`
- **K8s config**: `megadoomer-config` repo at `applications/static/howmanywins/do/`
- **Routing**: Gateway API HTTPRoute -> `megadoomer-gateway`
- **TLS**: cert-manager Certificate in `gateway-system` namespace
- **DNS**: `external-dns` annotation on the HTTPRoute
- **Image**: `ghcr.io/megadoomer-io/howmanywinsdoesbrucebochyhave` (CI auto-publishes on push to main)
- **Port**: 8000 (uvicorn)

Pushing to main triggers CI which builds, publishes to GHCR, and updates the image tag in megadoomer-config. ArgoCD auto-syncs the deployment.

## Running Locally

```bash
# Install dependencies
uv sync --all-extras

# Run dev server
make run

# Run tests
make test

# Lint + type check
make lint

# Format code
make format

# Build Docker image
make build
```

## Key Dependencies

- `fastapi` + `uvicorn` -- web framework and ASGI server
- `requests` -- HTTP client for scraping baseball-reference.com
- `lxml` -- HTML parsing (XPath queries)
- `cachetools` -- TTL cache decorator (15-minute cache on scraped data)
- `jinja2` -- template rendering
