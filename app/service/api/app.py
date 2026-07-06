from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import get_ptd_repository, router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alt dev server
        "http://10.9.21.12",  # Production (IP)
        "https://10.9.21.12",  # Production (IP, HTTPS)
        "http://vs268.dei.isep.ipp.pt",  # Production (hostname)
        "https://vs268.dei.isep.ipp.pt",  # Production (hostname, HTTPS)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def preload_ptd_data() -> None:
    pt_repo = get_ptd_repository()
    await asyncio.to_thread(pt_repo.preload)


app.include_router(router)