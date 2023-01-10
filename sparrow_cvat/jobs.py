"""Jobs API calls."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from tqdm import tqdm

from .auth import get_client, get_ui_host


def list_jobs(task_id: int) -> list[int]:
    """List all tasks in a project."""
    with get_client() as client:
        return [job.id for job in client.tasks.retrieve(task_id).get_jobs()]


def update_stage(job_id: int, stage: str) -> None:
    """Update the stage of a job."""
    with get_client() as client:
        job = client.jobs.retrieve(job_id)
        job.update({"stage": stage})


def complete_task(task_id: int) -> None:
    """Complete a task."""
    job_ids = list_jobs(task_id)
    for job_id in tqdm(job_ids):
        update_stage(job_id, "acceptance")


def download_filename_urls(
    task_id: int, oputput_path: Optional[Union[str, Path]] = None
) -> None:
    """Create a CSV with the filename and URL for each image."""
    if oputput_path is None:
        oputput_path = f"filenames_{task_id}.csv"
    records = []
    host = get_ui_host()
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        for job in tqdm(task.get_jobs()):
            job_meta = job.get_meta()
            start_frame_id = job_meta["start_frame"]
            for i, frame in enumerate(job_meta["frames"]):
                route = f"tasks/{task_id}/jobs/{job.id}?frame={start_frame_id + i}"
                record = dict(filename=frame["name"], url=os.path.join(host, route))
                records.append(record)
    df = pd.DataFrame(records)
    df.to_csv(oputput_path, index=False)
