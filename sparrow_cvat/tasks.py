"""Tasks."""
from typing import Any, Optional

from .auth import get_api


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
