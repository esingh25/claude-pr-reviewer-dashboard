"""Metrics ingestion (write, API-key protected) and read (public) endpoints."""

from collections import Counter

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import require_api_key
from app.database import get_db
from app.models import ReviewRun
from app.schemas import ReviewRunCreate, ReviewRunRead, SeverityCounts, SummaryStats

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.post(
    "", response_model=ReviewRunRead, status_code=201, dependencies=[Depends(require_api_key)]
)
def create_review_run(payload: ReviewRunCreate, db: Session = Depends(get_db)) -> ReviewRun:
    run = ReviewRun(
        repo=payload.repo,
        pr_number=payload.pr_number,
        head_sha=payload.head_sha,
        provider=payload.provider,
        model=payload.model,
        files_reviewed=payload.files_reviewed,
        comments_posted=payload.comments_posted,
        severity_critical=payload.severity_counts.critical,
        severity_high=payload.severity_counts.high,
        severity_medium=payload.severity_counts.medium,
        severity_low=payload.severity_counts.low,
        duration_seconds=payload.duration_seconds,
        status=payload.status,
        run_timestamp=payload.timestamp,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@router.get("", response_model=list[ReviewRunRead])
def list_review_runs(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    repo: str | None = None,
    provider: str | None = None,
    db: Session = Depends(get_db),
) -> list[ReviewRun]:
    query = db.query(ReviewRun)
    if repo:
        query = query.filter(ReviewRun.repo == repo)
    if provider:
        query = query.filter(ReviewRun.provider == provider)
    return query.order_by(ReviewRun.run_timestamp.desc()).offset(offset).limit(limit).all()


@router.get("/summary", response_model=SummaryStats)
def get_summary(db: Session = Depends(get_db)) -> SummaryStats:
    runs = db.query(ReviewRun).all()
    total_runs = len(runs)
    total_files = sum(r.files_reviewed for r in runs)
    total_comments = sum(r.comments_posted for r in runs)
    successes = sum(1 for r in runs if r.status == "success")
    success_rate = (successes / total_runs) if total_runs else 0.0

    severity_totals = SeverityCounts(
        critical=sum(r.severity_critical for r in runs),
        high=sum(r.severity_high for r in runs),
        medium=sum(r.severity_medium for r in runs),
        low=sum(r.severity_low for r in runs),
    )

    runs_by_provider = dict(Counter(r.provider for r in runs))

    by_day: dict[str, int] = {}
    for r in runs:
        day = r.run_timestamp.date().isoformat()
        by_day[day] = by_day.get(day, 0) + 1
    runs_by_day = [{"date": day, "count": count} for day, count in sorted(by_day.items())]

    return SummaryStats(
        total_runs=total_runs,
        total_files_reviewed=total_files,
        total_comments_posted=total_comments,
        success_rate=round(success_rate, 4),
        severity_totals=severity_totals,
        runs_by_provider=runs_by_provider,
        runs_by_day=runs_by_day,
    )
