# Getting started

## Installation

Install the published package with pip:

```bash
pip install easy-bbox
```

## Create a box

The explicit constructor uses the canonical internal representation:

```python
from easy_bbox import Bbox

box = Bbox(left=10, top=20, right=110, bottom=80)
```

Coordinates may be integers or floats. A box can have zero width or height, but its edges may not be reversed.

> Trying to create a bounding box with reversed edges (ie `top > bottom` or `left > right` will raise a `ValueError`)

```python
Bbox.from_tlbr((10, 20, 110, 80))
Bbox.from_tlwh((10, 20, 100, 60))
Bbox.from_cwh((60, 50, 100, 60))
```

## Convert at the boundary

```python
box.to_tlbr()                 # (left, top, right, bottom)
box.to_tlwh()                 # (left, top, width, height)
box.to_cwh()                  # (center_x, center_y, width, height)
box.to_norm_tlbr(640, 480)    # normalized corners
box.to_norm_cwh(640, 480)     # normalized center and size
box.to_polygon()              # four (x, y) corners
```

Aliases are available when they match your dataset vocabulary:

| Format         | Constructor       | Converter       |
| -------------- | ----------------- | --------------- |
| Pascal VOC     | `from_pascal_voc` | `to_pascal_voc` |
| XYXY           | `from_xyxy`       | `to_xyxy`       |
| COCO           | `from_coco`       | `to_coco`       |
| YOLO           | —                 | `to_yolo`       |
| Albumentations | —                 | `to_albu`       |

## Use Pydantic features

Because `Bbox` is a Pydantic model, it can be validated, serialized, and embedded in other models:

```python
payload = box.model_dump()
restored = Bbox.model_validate(payload)
assert restored == box
```
