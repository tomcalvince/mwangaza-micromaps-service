## mwangaza-map-service

FastAPI geometry microservice for subdivision plot mapping.

### Prerequisites

- Docker + Docker Compose v2 (`docker compose`)
- An **external Postgres** database reachable from your Docker host

### Configuration

Create a `.env` file (not committed) based on `.env.example`:

```bash
cp .env.example .env
```

Required:
- `DATABASE_URL` (async SQLAlchemy URL), e.g. `postgresql+asyncpg://user:pass@host:5432/dbname`

Optional:
- `ENVIRONMENT` (`development` or `production`)

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

Service will be available at:
- `http://localhost:8000/health`

### Run with Docker (no Compose)

```bash
docker build -t mwangaza-map-service .
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/dbname" \
  -e ENVIRONMENT=development \
  mwangaza-map-service
```

### Run migrations (Alembic) against the external DB

```bash
docker compose run --rm api alembic upgrade head
```
