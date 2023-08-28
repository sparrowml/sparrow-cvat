"""Expose CLI."""
import fire

from .tasks import (
    complete_task,
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
        "complete-task": complete_task,
        "create-task": create_task,
        "delete-task": delete_task,
        "download-annotations": download_annotations,
        "download-images": download_images,
        "list-tasks": list_tasks,
        "upload-images": upload_images,
    }
    fire.Fire(commands)
