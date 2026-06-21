"""Vercel Python entrypoint: re-exports the FastAPI ASGI app for the @vercel/python builder."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402, F401
