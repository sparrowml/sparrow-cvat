"""Expose CLI."""
import fire

from .dataset_manifest import create_manifest
from .jobs import complete_task, download_filename_urls, list_jobs
from .tasks import (
    create_task,
    delete_task,
    download_annotations,
    list_tasks,
    upload_annotations,
    upload_images,
)


def main() -> None:
    """Call CLI commands."""
    fire.Fire(
        {
            "complete-task": complete_task,
            "delete-task": delete_task,
            "download-annotations": download_annotations,
            "download-filename-urls": download_filename_urls,
            "create-task": create_task,
            "create-manifest": create_manifest,
            "list-jobs": list_jobs,
            "list-tasks": list_tasks,
            "upload-annotations": upload_annotations,
            "upload-images": upload_images,
        }
    )
