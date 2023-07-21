"""Expose CLI."""
import fire

from .jobs import complete_task, download_filename_urls, list_jobs
from .tasks import (  # upload_annotations,; upload_video,; upload_videos,
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
        "delete-task": delete_task,
        "download-annotations": download_annotations,
        "download-filename-urls": download_filename_urls,
        "download-images": download_images,
        "create-task": create_task,
        "list-jobs": list_jobs,
        "list-tasks": list_tasks,
        # "upload-annotations": upload_annotations,
        "upload-images": upload_images,
        # "upload-video": upload_video,
        # "upload-videos": upload_videos,
    }
    fire.Fire(commands)
