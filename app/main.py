# Fast api entry point, registers routes and starts the server
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import plots, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Mwangaza Map Service",
    description="Geometry microservice for subdivision plot mapping",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plots.router)
app.include_router(projects.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}