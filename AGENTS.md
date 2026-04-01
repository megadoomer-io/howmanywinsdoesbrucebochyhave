# howmanywinsdoesbrucebochyhave

This is a claude-first repository. Claude is the primary developer; humans provide direction and review.

## What This App Does

A Flask web app that scrapes Bruce Bochy's career wins from baseball-reference.com and displays the count. Results are cached with a 15-minute TTL. Bochy retired in 2024 with 2,003 career wins, so the number is now static — consider simplifying to a static site.

Live at: https://howmanywinsdoesbrucebochyhave.com

## Current State (Legacy)

This codebase predates modern Python tooling and needs significant modernization. See `docs/plans/2026-04-01-modernization.md` for the full plan.

| Aspect | Current | Target |
|--------|---------|--------|
| Python | 3.7 | 3.13+ |
| Package manager | Pipenv + setup.py | uv + pyproject.toml |
| Linting | flake8 | ruff |
| Type checking | None | mypy (strict) |
| CI | None (tox in Docker build) | GitHub Actions |
| Container registry | Docker Hub (`mikedougherty/`) | GHCR (`ghcr.io/megadoomer-io/`) |
| Tests | Placeholder only (`assert True`) | Real tests with mocked HTTP |
| Framework | Flask + gunicorn | Consider FastAPI |

## Project Structure

```
howmanywinsdoesbrucebochyhave/
  __init__.py                    # App factory, exports create_app()
  __version__.py                 # Version string
  howmanywinsdoesbrucebochyhave.py  # Main app: scraping, parsing, Flask route
config/
  gunicorn.py                    # Gunicorn config (empty)
templates/
  index.html                     # Jinja2 template (wins count + refresh time)
static/
  css/styles.css                 # Minimal styling
test/
  test_howmanywinsdoesbrucebochyhave.py  # Placeholder test
manifests/                       # DEPRECATED: K8s manifests now in megadoomer-config
```

## Deployment

- **Cluster**: DigitalOcean (`megadoomer-do`)
- **Namespace**: `howmanywins`
- **K8s config**: `megadoomer-config` repo at `applications/static/howmanywins/do/`
- **Routing**: Gateway API HTTPRoute → `megadoomer-gateway` (https-howmanywins listener)
- **TLS**: cert-manager Certificate in `gateway-system` namespace
- **DNS**: `external-dns` annotation on the HTTPRoute
- **Image**: `mikedougherty/howmanywinsdoesbrucebochyhave:latest` (Docker Hub, no CI — manual push)
- **Port**: 5000 (Flask/gunicorn)

Pushing to main does NOT auto-deploy. There is no CI/CD pipeline yet. Image updates require manual `docker build` and `docker push`.

## Running Locally

```bash
# Current (legacy) way:
pipenv install --dev
pipenv run python -m howmanywinsdoesbrucebochyhave

# Or via Docker:
docker build -t howmanywins .
docker run -p 5000:5000 howmanywins
```

## Key Dependencies

- `flask` — web framework
- `requests` — HTTP client for scraping baseball-reference.com
- `lxml` — HTML parsing (XPath queries)
- `cachetools` — TTL cache decorator (15-minute cache on scraped data)
- `gunicorn` — WSGI server

## Modernization Priority

When starting work on this repo, follow the plan in `docs/plans/2026-04-01-modernization.md`. The phases are designed to be executed in order, with each phase leaving the app in a deployable state.

**Phase 1** (repo transfer) may need to happen first since it affects GitHub URLs, but Phases 2-6 can proceed independently of the transfer.
