"""FastAPI application entry point.

Run with `uvicorn src.api.main:app`. Endpoints live in `src.api.routers`.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.config import PRODUCTION_ORIGINS
from src.api.routers import auth, jobs, payments, public

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "front_end"

app = FastAPI(
    title="LinkedIn Job Description Generator",
    version="0.1.0",
)

# Two CORS layers, kept in the original order: a permissive one first, then
# a production-origin one added afterwards (Starlette runs the last-added
# middleware first).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=PRODUCTION_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments.router)
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(public.router)

# Serve the static frontend at "/". Must be mounted after all API routes.
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
