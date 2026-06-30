from __future__ import annotations

from fastapi import FastAPI

from .routes import router
from ..core.logging import configure_logging
from ..core.config import settings

configure_logging()

app = FastAPI(
    title="PTD Capacity Estimation API",
    description=(
        "API for predicting transformer substation capacity (regression) and utilisation category (classification). "
        "Models are versioned and loaded from the `models/` directory. "
        "Supports multiple training profiles (leve, regular, pesado)."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(router)