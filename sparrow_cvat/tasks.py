"""Tasks."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from cvat_sdk.core.helpers import TqdmProgressReporter
from cvat_sdk.core.proxies.tasks import ResourceType
from tqdm import tqdm

from .auth import get_client
from .utils import VALID_IMAGE_FORMATS


def create_task(
    name: str,
    org: str,
    project_id: int,
    segment_size: int = 25,
) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    data = {"name": name, "project_id": project_id, "segment_size": segment_size}
    kwargs = {"org": org}
    with get_client() as client:
        task, _ = client.tasks.api.create(data, **kwargs)
    return task.to_dict()


def delete_task(task_id: int) -> None:
    """Delete a task."""
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        task.remove()


def list_tasks(project_id: int) -> list[int]:
    """List all tasks in a project."""
    with get_client() as client:
        return client.projects.retrieve(project_id).tasks


def download_annotations(
    task_id: int, output_path: Optional[Union[str, Path]] = None
) -> None:
    """Download annotations for a task."""
    if output_path is None:
        output_path = f"{task_id}.zip"
    output_path = str(output_path)
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        task.export_dataset("CVAT for images 1.1", output_path, include_images=False)


def upload_annotations(task_id: int, annotations_path: Union[str, Path]) -> None:
    """Upload annotations for a task."""
    annotations_path = str(annotations_path)
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        task.import_annotations(
            "CVAT 1.1", annotations_path, pbar=TqdmProgressReporter(tqdm())
        )


def upload_images(task_id: int, image_directory: Union[str, Path]) -> None:
    """Upload images to a task."""
    image_directory = Path(image_directory)
    images = []
    for extension in VALID_IMAGE_FORMATS:
        images.extend(image_directory.glob(f"*{extension}"))
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        task.upload_data(
            ResourceType.LOCAL,
            [str(i) for i in images],
            pbar=TqdmProgressReporter(tqdm()),
        )
