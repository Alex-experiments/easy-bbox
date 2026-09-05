# Coordinate formats

A coordinate format is just an ordering and interpretation of four numbers. Easy Bbox uses a single canonical representation internally so that format conversion does not leak into geometry code.

## The four common layouts

Assume a box with `left=10`, `top=20`, `right=110`, and `bottom=80`:

| Name                  | Values                                           | Meaning                               |
| --------------------- | ------------------------------------------------ | ------------------------------------- |
| TLBR / XYXY           | `(10, 20, 110, 80)`                              | left, top, right, bottom              |
| TLWH / COCO           | `(10, 20, 100, 60)`                              | left, top, width, height              |
| CWH                   | `(60, 50, 100, 60)`                              | center x, center y, width, height     |
| normalized TLBR       | `(0.015625, 0.0417, 0.1719, 0.1667)` for 640×480 | TLBR divided by image dimensions      |
| normalized CWH / YOLO | `(0.09375, 0.1042, 0.15625, 0.125)` for 640×480  | center and size divided by dimensions |

```python
from easy_bbox import Bbox

box = Bbox.from_tlbr((10, 20, 110, 80))
assert box.to_coco() == (10, 20, 100, 60)
assert box.to_yolo(640, 480) == (0.09375, 0.10416666666666667, 0.15625, 0.125)
```

## Image coordinates and edge semantics

Boxes use a top-left origin: x increases to the right and y increases downward. The library follows the useful array-slicing convention that the right and bottom edges are excluded for integer boxes. Thus a box from `(0, 0)` to `(32, 64)` covers a 32×64 region.

The geometry methods treat touching edges as an intersection with zero area. Use `overlaps()` when you need a meaningful, non-zero-area overlap.

## Normalization

Use image dimensions only when converting to or from normalized coordinates. Normalized output is useful for YOLO and Albumentations integrations:

```python
width, height = 1920, 1080
box = Bbox.from_tlbr((480, 270, 1440, 810))

box.to_albu(width, height)  # normalized corners
box.to_yolo(width, height)  # normalized center and size
```
