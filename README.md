## mwangaza-map-service

FastAPI geometry microservice for subdivision plot mapping.

### Prerequisites

- Docker + Docker Compose v2 (`docker compose`)
- An **external Postgres** database reachable from your Docker host
- An **external RustFS** (or other S3-compatible) instance for project plan images

### Configuration

Create a `.env` file (not committed) based on `.env.example`:

```bash
cp .env.example .env
```

Required:
- `DATABASE_URL` (async SQLAlchemy URL), e.g. `postgresql+asyncpg://user:pass@host:5432/dbname`
- `S3_ENDPOINT_URL` — RustFS API URL (e.g. `http://rustfs-host:9000`)
- `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`

Optional:
- `ENVIRONMENT` (`development` or `production`)
- `S3_PREFIX` (default `project-plans`)
- `S3_ADDRESSING_STYLE` (default `path`; use if presigned URLs fail)
- `PLAN_IMAGE_MAX_BYTES` (default 10 MB)

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

Service will be available at:
- `http://localhost:8000/health`

### Run with Docker (no Compose)

```bash
docker build -t mwangaza-map-service .
docker run --rm -p 8000:8000 --env-file .env mwangaza-map-service
```

### Run migrations (Alembic) against the external DB

```bash
docker compose run --rm api alembic upgrade head
```

### API: multiple plots per project

Each plot is identified by `external_plot_id` within a project. You can create many plots per project:

```bash
# Create plot 1
curl -X POST "http://localhost:8000/projects/1/plots" \
  -H "Content-Type: application/json" \
  -d '{"external_plot_id": 101, "polygon_points": [{"x":0.1,"y":0.1},{"x":0.5,"y":0.1},{"x":0.3,"y":0.4}]}'

# Create plot 2 (different external_plot_id)
curl -X POST "http://localhost:8000/projects/1/plots" \
  -H "Content-Type: application/json" \
  -d '{"external_plot_id": 102, "polygon_points": [{"x":0.6,"y":0.1},{"x":0.9,"y":0.1},{"x":0.75,"y":0.4}]}'

# List all plots
curl "http://localhost:8000/projects/1/plots"
```

Duplicate `external_plot_id` on the same project returns `409 Conflict`.

### API: project plan image (RustFS)

Upload a reference plan image for a project (stored in RustFS, metadata in Postgres):

```bash
curl -X POST "http://localhost:8000/projects/1/plan-image" \
  -F "file=@plan.png"

curl "http://localhost:8000/projects/1/plan-image"

curl -X DELETE "http://localhost:8000/projects/1/plan-image"
```

`GET` returns metadata plus a presigned download URL (short-lived).

Ensure the bucket named in `S3_BUCKET` exists in RustFS before uploading.
