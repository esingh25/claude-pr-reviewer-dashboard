"""ORM model for a single review run's metrics record."""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class ReviewRun(Base):
    __tablename__ = "review_runs"

    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String, nullable=False, index=True)
    pr_number = Column(Integer, nullable=False)
    head_sha = Column(String, nullable=False)
    provider = Column(String, nullable=False, index=True)
    model = Column(String, nullable=False)
    files_reviewed = Column(Integer, nullable=False, default=0)
    comments_posted = Column(Integer, nullable=False, default=0)
    severity_critical = Column(Integer, nullable=False, default=0)
    severity_high = Column(Integer, nullable=False, default=0)
    severity_medium = Column(Integer, nullable=False, default=0)
    severity_low = Column(Integer, nullable=False, default=0)
    duration_seconds = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default="success")
    run_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
