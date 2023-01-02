"""Expose CLI."""
import fire

from .dataset_manifest import create_manifest
from .tasks import (
    create_task,
    download_annotations,
    list_tasks,
    upload_annotations,
    upload_images,
)


def main() -> None:
    """Call CLI commands."""
    fire.Fire(
        {
            "download-annotations": download_annotations,
            "create-task": create_task,
            "create-manifest": create_manifest,
            "list-tasks": list_tasks,
            "upload-annotations": upload_annotations,
            "upload-images": upload_images,
        }
    )
