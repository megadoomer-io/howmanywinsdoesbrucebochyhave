# Modernization Plan

Bring this repository up to megadoomer-io standards: modern Python, CI/CD, GHCR publishing, and no in-repo Kubernetes manifests.

## Current State

- **Runtime**: Python 3.7 (Dockerfile), Pipenv for dependencies
- **Framework**: Flask + gunicorn, scrapes baseball-reference.com
- **Packaging**: setup.py + setup.cfg + MANIFEST.in
- **CI**: tox (runs in Docker build), no GitHub Actions
- **Container image**: `mikedougherty/howmanywinsdoesbrucebochyhave:latest` on Docker Hub
- **K8s manifests**: `manifests/do/` (deployment, service, ingress) — now migrated to megadoomer-config
- **Repo owner**: `mikedougherty` (personal account)

## Phase 1: Transfer to megadoomer-io

- [ ] Transfer repo from `mikedougherty` to `megadoomer-io` on GitHub
- [ ] Rename to something shorter if desired (e.g., `howmanywins`)
- [ ] Update any references in megadoomer-config to the new repo location (AppProject sourceRepos, etc.)

## Phase 2: Python Modernization

- [ ] Upgrade to Python 3.13+
- [ ] Replace Pipenv + setup.py with `uv` and `pyproject.toml`
  - Move dependencies from Pipfile to pyproject.toml
  - Dependencies: flask, requests, lxml, cachetools, gunicorn
  - Dev dependencies: pytest, pytest-mock, ruff
- [ ] Remove: `Pipfile`, `Pipfile.lock`, `setup.py`, `setup.cfg`, `MANIFEST.in`, `tox.ini`
- [ ] Add type annotations throughout
- [ ] Replace `flake8` with `ruff` for linting and formatting
- [ ] Add `mypy` in strict mode
- [ ] Consider migrating from Flask to FastAPI
  - The app is tiny (one route), so migration would be straightforward
  - FastAPI provides built-in async support which would improve the scraping/caching pattern

## Phase 3: Dockerfile

- [ ] Multi-stage build: build stage installs deps, runtime stage copies only what's needed
- [ ] Use `uv` for dependency installation in the container
- [ ] Run as non-root user
- [ ] Set `readOnlyRootFilesystem: true` compatible (write only to /tmp if needed)
- [ ] Expose port 5000 (or switch to 8080 to match portal convention)
- [ ] Update megadoomer-config deployment if port changes

## Phase 4: CI/CD with GitHub Actions

- [ ] Add `.github/workflows/lint-and-test.yaml`
  - Run on pull requests
  - Steps: ruff check, ruff format --check, mypy, pytest
- [ ] Add `.github/workflows/publish.yaml`
  - Run on push to main
  - Build Docker image and push to GHCR (`ghcr.io/megadoomer-io/howmanywins`)
  - Tag format: `YYYYMMDDTHHmmss-<shortsha>` + `latest`
  - Update megadoomer-config image tag via `kustomize edit set image`
  - Requires `GH_TOKEN_MEGADOOMER_CONFIG_WRITE` secret (fine-grained PAT)
- [ ] Update megadoomer-config to reference the GHCR image instead of Docker Hub

## Phase 5: Remove In-Repo Kubernetes Manifests

- [ ] Delete `manifests/` directory entirely
  - All K8s config now lives in megadoomer-config under `applications/static/howmanywins/do/`
- [ ] Delete `docker-compose.yml` (or update it for local dev only)

## Phase 6: Repository Hygiene

- [ ] Add `CLAUDE.md` with project conventions (claude-first repo)
- [ ] Add `AGENTS.md` referencing standard agent instructions
- [ ] Update `.gitignore` for modern Python (`__pycache__`, `.venv`, `.mypy_cache`, `.ruff_cache`)
- [ ] Add `Makefile` with targets: `lint`, `format`, `test`, `build`, `run`
- [ ] Add or update `README.md` with current setup instructions

## Notes

- The app scrapes baseball-reference.com with a 15-minute TTL cache. Consider whether this is still the desired behavior or if a static page would suffice (Bochy retired in 2024 with 2,003 wins).
- If Bochy's career is truly over, the app could be simplified to a static site, eliminating the Python runtime entirely.
