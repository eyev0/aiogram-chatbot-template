from __future__ import annotations

from sqlalchemy.dialects import postgresql

from app.models.db import BaseModel, db


class APSchedulerJob(BaseModel):
    __tablename__ = "apscheduler_jobs"

    id = db.Column(db.VARCHAR(length=191), primary_key=True)
    next_run_time = db.Column(postgresql.DOUBLE_PRECISION(precision=53), index=True)
    job_state = db.Column(postgresql.BYTEA(), nullable=False)


class APSchedulerJobsRelatedModel(BaseModel):
    __abstract__ = True

    job_id = db.Column(
        db.ForeignKey(
            f"{APSchedulerJob.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
