"""Pydantic request/response schemas for the metrics API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SeverityCounts(BaseModel):
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0


class ReviewRunCreate(BaseModel):
    repo: str
    pr_number: int
    head_sha: str
    provider: str
    model: str
    files_reviewed: int = 0
    comments_posted: int = 0
    severity_counts: SeverityCounts = Field(default_factory=SeverityCounts)
    duration_seconds: float = 0.0
    status: str = "success"
    timestamp: datetime


class ReviewRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repo: str
    pr_number: int
    head_sha: str
    provider: str
    model: str
    files_reviewed: int
    comments_posted: int
    severity_critical: int
    severity_high: int
    severity_medium: int
    severity_low: int
    duration_seconds: float
    status: str
    run_timestamp: datetime
    created_at: datetime


class SummaryStats(BaseModel):
    total_runs: int
    total_files_reviewed: int
    total_comments_posted: int
    success_rate: float
    severity_totals: SeverityCounts
    runs_by_provider: dict[str, int]
    runs_by_day: list[dict]
