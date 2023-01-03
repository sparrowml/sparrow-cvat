"""Jobs API calls."""
from __future__ import annotations

from .auth import get_client


def list_jobs(task_id: int) -> list[int]:
    """List all tasks in a project."""
    with get_client() as client:
        return [job.id for job in client.tasks.retrieve(task_id).get_jobs()]


def update_stage(job_id: int, stage: str) -> None:
    """Update the stage of a job."""
    with get_client() as client:
        job = client.jobs.retrieve(job_id)
        job.update({"stage": stage})
