"""Tasks API calls."""
from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path
from typing import Any, Optional, Union

from cvat_sdk.core.helpers import TqdmProgressReporter
from cvat_sdk.core.proxies.tasks import ResourceType
from tqdm import tqdm

from .auth import get_client
from .utils import VALID_IMAGE_FORMATS


def create_task(name: str, project_id: int, segment_size: int = 25) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    data = {"name": name, "project_id": project_id, "segment_size": segment_size}
    with get_client() as client:
        task, _ = client.tasks.api.create(data)
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
    """Download CVAT XML annotations for a task."""
    if output_path is None:
        output_path = f"annotations_{task_id}.xml"
    with get_client() as client, tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        output_zip = tmp_dir / "download.zip"
        task = client.tasks.retrieve(task_id)
        task.export_dataset("CVAT for images 1.1", output_zip, include_images=False)
        with zipfile.ZipFile(output_zip, "r") as zip:
            zip.extract("annotations.xml", tmp_dir)
        xml_path = tmp_dir / "annotations.xml"
        with open(xml_path, "r") as f1, open(output_path, "w") as f2:
            f2.write(f1.read())


def download_images(
    task_id: int, output_directory: Optional[Union[str, Path]] = None
) -> None:
    """Download CVAT images for a task."""
    if output_directory is None:
        output_directory = Path(f"images_{task_id}")
    output_directory = Path(output_directory)
    output_directory.mkdir(exist_ok=True, parents=True)
    with get_client() as client, tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        output_zip = tmp_dir / "download.zip"
        task = client.tasks.retrieve(task_id)
        print("Downloading images...")
        task.export_dataset("CVAT for images 1.1", output_zip, include_images=True)
        with zipfile.ZipFile(output_zip, "r") as zip:
            zip.extractall(tmp_dir)
        print("Moving extracted images...")
        for image_path in tqdm(list((tmp_dir / "images").glob("*"))):
            with open(image_path, "rb") as f1, open(
                output_directory / image_path.name, "wb"
            ) as f2:
                f2.write(f1.read())


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
