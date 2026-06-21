"""FastAPI app: CORS, table creation, route registration."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes_metrics import router as metrics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Claude PR Reviewer Dashboard API")

allowed_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(metrics_router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
