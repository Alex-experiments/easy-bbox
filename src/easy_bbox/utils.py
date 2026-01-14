"""
utils.py

Contains utility functions for bounding box operations.
"""

from typing import List, Optional, Sequence, Tuple

from easy_bbox.bbox import Bbox


def nms(
    bboxes: List[Bbox],
    scores: List[float],
    iou_threshold: float = 0.5,
) -> List[Tuple[Bbox, float]]:
    """Perform Non-Maximum Suppression on a list of bounding boxes.

    Args:
        bboxes (List[Bbox]): List of bounding boxes.
        scores (List[float]): List of confidence scores for each bounding box.
        iou_threshold (float, optional): IoU threshold for suppression. Defaults to 0.5.

    Returns:
        List[Tuple[Bbox, float]]: List of selected bounding boxes and their scores.

    Raises:
        ValueError: If the length of bboxes and scores do not match.
    """
    if len(bboxes) != len(scores):
        raise ValueError("The length of bboxes and scores must be the same.")

    # Sort the bounding boxes by their confidence scores in descending order
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    selected_indices: List[int] = []

    while sorted_indices:
        current_index = sorted_indices[0]
        selected_indices.append(current_index)

        # Compare the current bounding box with the rest
        current_bbox = bboxes[current_index]
        remaining_indices: List[int] = []

        for index in sorted_indices[1:]:
            other_bbox = bboxes[index]
            iou = current_bbox.iou(other_bbox)

            if iou <= iou_threshold:
                remaining_indices.append(index)

        sorted_indices = remaining_indices

    # Return the selected bounding boxes and their scores
    return [(bboxes[i], scores[i]) for i in selected_indices]


def bbox_union(bboxes: Sequence[Bbox]) -> Bbox:
    """Calculate the union of a list of bounding boxes.

    Args:
        bboxes (Sequence[Bbox]): A sequence of bounding boxes.

    Returns:
        Bbox: The bounding box that represents the union of all input bounding boxes.

    Raises:
        ValueError: If the input list of bounding boxes is empty.
    """
    if not bboxes:
        raise ValueError("A non empty Bbox list is needed.")

    return Bbox(
        left=min(b.left for b in bboxes),
        top=min(b.top for b in bboxes),
        right=max(b.right for b in bboxes),
        bottom=max(b.bottom for b in bboxes),
    )


def bbox_intersection(bboxes: Sequence[Bbox]) -> Optional[Bbox]:
    """Calculate the intersection of a list of bounding boxes.

    Args:
        bboxes (Sequence[Bbox]): A sequence of bounding boxes.

    Returns:
        Optional[Bbox]: The bounding box that represents the intersection of all input bounding
            boxes. If the resulting bounding box is not valid, returns None.

    Raises:
        ValueError: If the input list of bounding boxes is empty.
    """
    if not bboxes:
        raise ValueError("A non empty Bbox list is needed.")

    left = max(b.left for b in bboxes)
    top = max(b.top for b in bboxes)
    right = min(b.right for b in bboxes)
    bottom = min(b.bottom for b in bboxes)

    if left > right or top > bottom:
        return None

    return Bbox(left=left, top=top, right=right, bottom=bottom)
