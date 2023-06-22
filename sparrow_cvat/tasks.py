"""Tasks API calls."""
from __future__ import annotations

import math
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Optional, Union

from tqdm import tqdm

from .api import CVAT
from .auth import get_client
from .utils import VALID_IMAGE_FORMATS, VALID_VIDEO_FORMATS


def get_frames_info(task_id: int) -> list[dict[str, Any]]:
    """Get information about all frames in a task."""
    task_meta = CVAT.get(f"tasks/{task_id}/data/meta")
    return task_meta["frames"]


def create_task(name: str, project_id: int, segment_size: int = 25) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    payload = {"name": name, "project_id": project_id, "segment_size": segment_size}
    return CVAT.post("tasks", payload)


def delete_task(task_id: int) -> None:
    """Delete a task."""
    return CVAT.delete(f"tasks/{task_id}")


def list_tasks(project_id: int) -> list[int]:
    """List all tasks in a project."""
    project = CVAT.get(f"projects/{project_id}")
    return project["tasks"]


def download_annotations(
    task_id: int,
    output_path: Optional[Union[str, Path]] = None,
    media_type: str = "images",
) -> None:
    """Download CVAT XML annotations for a task."""
    if output_path is None:
        output_path = f"annotations_{task_id}.xml"
    assert media_type in ("images", "video"), "media_type must be 'images' or 'video'"
    data_format = f"CVAT for {media_type} 1.1"
    data = CVAT.download(
        f"tasks/{task_id}/annotations?format={data_format}&action=download"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_file = f"{tmpdir}/annotations.zip"
        with open(zip_file, "wb") as f:
            f.write(data)
        with zipfile.ZipFile(zip_file, "r") as f:
            f.extract("annotations.xml", tmpdir)
        with open(f"{tmpdir}/annotations.xml", "rb") as f:
            data = f.read()
    with open(output_path, "wb") as f:
        f.write(data)


def download_images(
    task_id: int, output_directory: Optional[Union[str, Path]] = None
) -> None:
    """Download CVAT images for a task."""
    if output_directory is None:
        output_directory = Path(f"images_{task_id}")
    output_directory = Path(output_directory)
    output_directory.mkdir(exist_ok=True, parents=True)
    data_format = "CVAT for images 1.1"
    data = CVAT.download(
        f"tasks/{task_id}/dataset?format={data_format}&action=download"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_file = f"{tmpdir}/annotations.zip"
        with open(zip_file, "wb") as f:
            f.write(data)
        with zipfile.ZipFile(zip_file, "r") as f:
            f.extractall(tmpdir)
        for tmp_image_path in tqdm(list((Path(tmpdir) / "images").glob("*"))):
            new_image_path = output_directory / tmp_image_path.name
            with open(tmp_image_path, "rb") as f1, open(new_image_path, "wb") as f2:
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
    """Upload images from a directory to a task."""
    image_directory = Path(image_directory)
    images = []
    for extension in VALID_IMAGE_FORMATS:
        images.extend(image_directory.glob(f"*{extension}"))
    upload_image_list(task_id, images)


def upload_video(project_id: int, video_path: Union[str, Path]) -> None:
    """Upload video to a new task."""
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    n_frames = math.ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    task = create_task(video_path.name, project_id, segment_size=n_frames + 1)
    upload_image_list(task["id"], [video_path])


def upload_videos(project_id: int, video_directory: Union[str, Path]) -> None:
    """Upload video from a directory to a set of new tasks (1 per video)."""
    video_directory = Path(video_directory)
    videos: list[Path] = []
    for extension in VALID_VIDEO_FORMATS:
        videos.extend(video_directory.glob(f"*{extension}"))
    for video_path in videos:
        upload_video(project_id, video_path)


def upload_image_list(task_id: int, image_list: list[Union[str, Path]]) -> None:
    """Upload a list of images to a task."""
    with get_client() as client:
        task = client.tasks.retrieve(task_id)
        task.upload_data(
            ResourceType.LOCAL,
            [str(i) for i in image_list],
            pbar=TqdmProgressReporter(tqdm()),
        )
