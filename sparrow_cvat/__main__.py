"""Expose CLI."""
import fire

from .tasks import (
    create_task,
    delete_task,
    download_annotations,
    download_images,
    list_tasks,
    upload_annotations,
    upload_images,
    upload_video,
    upload_videos,
)


def main() -> None:
    """Call CLI commands."""
    fire.Fire(
        {
            "delete-task": delete_task,
            "download-annotations": download_annotations,
            "download-images": download_images,
            "create-task": create_task,
            "list-tasks": list_tasks,
            "upload-annotations": upload_annotations,
            "upload-images": upload_images,
            "upload-video": upload_video,
            "upload-videos": upload_videos,
        }
    )
