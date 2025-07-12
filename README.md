# Disco E-Discovery Platform

## Setup

```bash
docker compose -f ops/docker-compose.yml build --no-cache
docker compose -f ops/docker-compose.yml up -d
```

Access API at `http://localhost:8000/health` and UI at `http://localhost:3000`.

### Tests

Run:

```bash
pytest
```

### Rollback

Use `docker compose -f ops/docker-compose.yml down -v` to stop and remove containers and volumes.
