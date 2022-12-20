"""Tasks."""
import json
import random
import time
from pathlib import Path
from typing import Any, Optional, Union

from cvat_sdk.api_client import models
from tqdm import tqdm

from .auth import get_api
from .utils import VALID_IMAGE_FORMATS


def create_task(
    name: str,
    org: str,
    project_id: int,
    segment_size: int = 25,
) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    client = get_api()
    data = {"name": name, "project_id": project_id, "segment_size": segment_size}
    kwargs = {"org": org}
    task, _ = client.tasks_api.create(data, **kwargs)
    return task.to_dict()


def list_tasks(
    org: str, project_id: int, task_prefix: Optional[str] = None
) -> list[dict[str, Any]]:
    """List tasks."""
    client = get_api()
    filter_object = {"and": [{"==": [{"var": "project_id"}, project_id]}]}
    if task_prefix is not None:
        filter_object["and"].append({"in": [task_prefix, {"var": "name"}]})
    kwargs = {"org": org, "filter": json.dumps(filter_object)}
    has_next = True
    page = 1
    all_tasks = []
    while has_next:
        tasks, _ = client.tasks_api.list(**{**kwargs, "page": page})
        all_tasks.extend([t.to_dict() for t in tasks["results"]])
        has_next = tasks["next"] is not None
        page += 1
    return all_tasks


def upload_images(
    task_prefix: str,
    org: str,
    project_id: int,
    image_directory: Union[str, Path],
    image_quality: int = 70,
    task_size: int = 200,
) -> dict[str, Any]:
    """Upload images to a task."""
    client = get_api()
    random_hash = f"{random.getrandbits(32):08x}"
    image_directory = Path(image_directory)
    images = []
    for extension in VALID_IMAGE_FORMATS:
        images.extend(image_directory.glob(f"*{extension}"))
    n_tasks = len(images) // task_size + 1
    tasks = []
    for i in tqdm(range(n_tasks), total=n_tasks):
        image_batch = images[i * task_size : (i + 1) * task_size]
        task = create_task(f"{task_prefix}-{random_hash}-{i}", org, project_id)
        task_id = task["id"]
        task_data = models.DataRequest(
            image_quality=image_quality,
            client_files=[open(image, "rb") for image in image_batch],
        )
        _, response = client.tasks_api.create_data(
            task_id,
            data_request=task_data,
            _content_type="multipart/form-data",
            _check_status=False,
            _parse_response=False,
        )
        assert response.status == 202, response.status
        for _ in range(100):
            status, _ = client.tasks_api.retrieve_status(task_id)
            if status.state.value in ["Finished", "Failed"]:
                break
            time.sleep(1)
        assert status.state.value == "Finished", status.message
        tasks.append(task["url"])
    return tasks
