"""Convert to CVAT XML."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Union

import datumaro as dm
import numpy as np
from sparrow_datums import AugmentedBoxTracking, FrameAugmentedBoxes
from xmltodict import unparse


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


def chunk_to_cvat(
    chunk_path: Union[str, Path], output_path: Union[str, Path], labels: list[str]
) -> None:
    """Convert a single AugmentedBoxTracking chunk to CVAT XML."""
    chunk_path = Path(chunk_path)
    output_path = Path(output_path)
    chunk = AugmentedBoxTracking.from_file(chunk_path)
    chunk = chunk.to_tlbr().to_absolute()
    annotations = {"version": "1.1"}
    tracks = []
    for j in range(chunk.shape[1]):
        boxes = chunk.array[:, j]
        indices = np.argwhere(np.isfinite(boxes[:, 0])).ravel()
        class_idx = boxes[indices[0], -1]
        label = labels[int(class_idx)]
        track = {"@id": str(j), "@label": label}
        box_records = []
        for i in indices:
            x1, y1, x2, y2 = boxes[i, :4]
            box_record = {
                "@frame": str(i),
                "@xtl": str(x1),
                "@ytl": str(y1),
                "@xbr": str(x2),
                "@ybr": str(y2),
                "@outside": "0",
                "@occluded": "0",
                "@keyframe": "1",
                "@z_order": "0",
            }
            box_records.append(box_record)
        box_records[-1]["@outside"] = "1"
        track["box"] = box_records
        tracks.append(track)
    annotations["track"] = tracks
    data = {"annotations": annotations}
    with open(output_path, "w") as f:
        f.write(unparse(data))
