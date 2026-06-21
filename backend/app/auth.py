"""API-key auth dependency for the write (ingestion) endpoint. Read endpoints stay public."""

import os

from fastapi import Header, HTTPException, status


def require_api_key(x_api_key: str = Header(default="")) -> None:
    expected = os.environ.get("INGEST_API_KEY")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server is not configured with INGEST_API_KEY",
        )
    if x_api_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
