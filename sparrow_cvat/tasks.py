"""Tasks."""
import time
from pathlib import Path
from typing import Any, Optional, Union

from cvat_sdk.api_client import models

from .auth import get_api
from .utils import VALID_IMAGE_FORMATS


def create_task(
    name: str, org: Optional[str] = None, project_id: Optional[int] = None
) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    client = get_api()
    data = {"name": name}
    kwargs = {}
    if org is not None:
        kwargs["org"] = org
    if project_id is not None:
        data["project_id"] = project_id
    task, _ = client.tasks_api.create(data, **kwargs)
    return task.to_dict()


def upload_images(task_id: int, image_directory: Union[str, Path]) -> dict[str, Any]:
    """Upload images to a task."""
    client = get_api()
    image_directory = Path(image_directory)
    images = []
    for extension in VALID_IMAGE_FORMATS:
        images.extend(image_directory.glob(f"*{extension}"))
    task_data = models.DataRequest(
        image_quality=70,
        client_files=[open(path, "rb") for path in images],
    )
    _, response = client.tasks_api.create_data(
        task_id,
        data_request=task_data,
        _content_type="multipart/form-data",
        _check_status=False,
        _parse_response=False,
    )
    assert response.status == 202, response.msg
    for _ in range(100):
        status, _ = client.tasks_api.retrieve_status(task_id)
        if status.state.value in ["Finished", "Failed"]:
            break
        time.sleep(1)
    assert status.state.value == "Finished", status.message
    task, _ = client.tasks_api.retrieve(task_id)
    return task.to_dict()
