"""Expose CLI."""
import fire

from .tasks import (
    create_task,
    delete_task,
    download_annotations,
    download_images,
    list_tasks,
    upload_images,
)


def main() -> None:
    """Call CLI commands."""
    commands = {
        "delete-task": delete_task,
        "download-annotations": download_annotations,
        "download-images": download_images,
        "create-task": create_task,
        "list-tasks": list_tasks,
        "upload-images": upload_images,
    }
    fire.Fire(commands)
