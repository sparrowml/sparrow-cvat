"""Expose CLI."""
import fire

from .auth import get_token
from .dataset_manifest import create_manifest
from .tasks import create_task, list_tasks, upload_images


def main() -> None:
    """Call CLI commands."""
    fire.Fire(
        {
            "get-token": get_token,
            "create-task": create_task,
            "create-manifest": create_manifest,
            "list-tasks": list_tasks,
            "upload-images": upload_images,
        }
    )
