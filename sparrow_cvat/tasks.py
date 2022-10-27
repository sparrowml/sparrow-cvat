"""Tasks."""
from typing import Any, Optional

from .api import post
from .auth import get_auth_headers


def create_task(
    name: str, org: Optional[str] = None, project_id: Optional[int] = None
) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    route = "/api/tasks"
    data = {"name": name}
    if org is not None:
        route += f"?org={org}"
    if project_id is not None:
        data["project_id"] = project_id
    return post(route, data, headers=get_auth_headers())
