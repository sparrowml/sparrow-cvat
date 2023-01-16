"""Convert to CVAT XML."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Union

import datumaro as dm
import numpy as np
from sparrow_datums import FrameAugmentedBoxes


def boxes_to_cvat(
    annotation_directory: Union[str, Path],
    output_path: Union[str, Path],
    labels: list[str],
) -> None:
    """Convert a directory of FrameAugmentedBoxes to CVAT XML."""
    annotation_directory = Path(annotation_directory)
    output_path = Path(output_path)
    dataset_items = []
    for annotation_path in annotation_directory.glob("*.json.gz"):
        boxes = FrameAugmentedBoxes.from_file(annotation_path)
        annotations = []
        for box in boxes.to_absolute():
            annotations.append(dm.Bbox(box.x, box.y, box.w, box.h, label=box.label))
        dataset_item = dm.DatasetItem(
            id=annotation_path.name.rstrip(".json.gz"),
            media=dm.Image(np.empty((boxes.image_height, boxes.image_width, 3))),
            annotations=annotations,
        )
        dataset_items.append(dataset_item)
    dataset = dm.Dataset.from_iterable(dataset_items, categories=list(labels))
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        dataset.export(tmp_dir, "cvat")
        with open(tmp_dir / "default.xml", "r") as f1, open(output_path, "w") as f2:
            f2.write(f1.read())
