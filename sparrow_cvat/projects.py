"""Projects API calls."""
from __future__ import annotations

from typing import Any

from .auth import get_client


def get_frames_info(project_id: int) -> list[dict[str, Any]]:
    """Get information about all frames in a task."""
    with get_client() as client:
        frames_info = []
        for task in client.projects.retrieve(project_id).get_tasks():
            frames_info.extend(task.get_frames_info())
        return frames_info
