# howmanywinsdoesbrucebochyhave

A web app that displays Bruce Bochy's career managerial wins, scraped from baseball-reference.com.

Live at: https://howmanywinsdoesbrucebochyhave.com

## Development

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
# Install dependencies
uv sync --all-extras

# Run locally (with hot reload)
make run

# Run tests
make test

# Lint and type check
make lint

# Format code
make format
```

## Deployment

Pushes to `main` automatically build and publish a Docker image to GHCR, then update the deployment config in [megadoomer-config](https://github.com/megadoomer-io/megadoomer-config). ArgoCD handles the rollout.
