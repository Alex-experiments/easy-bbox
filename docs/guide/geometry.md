# Geometry

`Bbox` includes the operations most detection and cropping pipelines need.

## Intersection, union, and IoU

```python
from easy_bbox import Bbox

left = Bbox.from_tlbr((0, 0, 100, 100))
right = Bbox.from_tlbr((50, 25, 150, 125))

intersection = left & right       # or left.intersection(right)
union = left | right              # or left.union(right)
score = left.iou(right)
```

`intersection()` returns `None` when boxes do not meet. It can return a zero-area box when they only touch; `overlaps()` is the convenience method for testing a non-zero-area intersection.

For a collection, use the top-level helpers:

```python
from easy_bbox import bbox_intersection, bbox_union

common = bbox_intersection([left, right])
outline = bbox_union([left, right])
```

Both helpers reject an empty sequence with `ValueError`.

## Containment and distance

```python
outer.contains(inner)
inner.is_inside(outer)
box.contains_point(x=25, y=40)
box.distance_to_point(x=500, y=40)
box.distance_to_bbox(other)
```

Point containment includes the edges. Distances are zero for points inside a box, and for boxes that overlap or touch. Choose Manhattan (`DistanceMetric.L1`) or Euclidean (`DistanceMetric.L2`, the default):

```python
from easy_bbox.bbox import DistanceMetric

box.distance_to_point(500, 40, dist=DistanceMetric.L1)
```

## Non-Maximum Suppression

`nms()` sorts boxes by score, keeps the highest-scoring candidate, and removes remaining boxes whose IoU exceeds the threshold:

```python
from easy_bbox import nms

kept = nms(
    bboxes=[left, right],
    scores=[0.95, 0.72],
    iou_threshold=0.5,
)
# [(highest-scoring-box, score), ...]
```

The returned pairs preserve each selected box's score. `bboxes` and `scores` must have the same length.
