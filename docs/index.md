# Bounding boxes, without the busywork

**Easy Bbox** is a small, typed Python library for the everyday geometry behind computer-vision pipelines. Create one box, move it, compare it, convert it, and keep going—without juggling four separate coordinate conventions.

<div class="grid cards" markdown>

-   :material-shape-rectangle-plus:{ .lg .middle } __Create boxes your way__

    ---

    Start with Pascal VOC, COCO, center-width-height, or a regular Python sequence.

    [:octicons-arrow-right-24: Learn the formats](guide/formats.md)

-   :material-vector-square:{ .lg .middle } __Use familiar geometry__

    ---

    Intersections, unions, IoU, containment, overlap, and distances are all first-class operations.

    [:octicons-arrow-right-24: Explore geometry](guide/geometry.md)

-   :material-arrow-expand-all:{ .lg .middle } __Transform safely__

    ---

    Shift, scale, pad, expand, and clip boxes with immutable-style methods that return new boxes.

    [:octicons-arrow-right-24: See transformations](guide/transformations.md)

-   :material-api:{ .lg .middle } __Keep your pipeline typed__

    ---

    `Bbox` is a Pydantic model, ships with `py.typed`, and has explicit return types.

    [:octicons-arrow-right-24: Browse the API](reference/api.md)

</div>

## Install

```bash
pip install easy-bbox
```

## A useful first five minutes

```python
from easy_bbox import Bbox

box = Bbox.from_coco((40, 20, 120, 80))

print(box.to_yolo(img_w=640, img_h=480))
# (0.15625, 0.125, 0.1875, 0.16666666666666666)

focus = box.expand_uniform(8).clip_to_img(img_w=640, img_h=480)
print(focus.to_tlbr())
# (32, 12, 168, 108)
```

!!! tip "A predictable mental model"
    Internally, every `Bbox` is stored as `(left, top, right, bottom)` in a top-left-origin coordinate system. Conversions happen at the edges of your application, while the geometry stays consistent inside it.

## Why Easy Bbox?

- **Small surface area:** one model and a few focused utilities.
- **No hidden image dependency:** coordinates are plain numbers; only Pydantic is required.
- **Format-aware:** named constructors and aliases make intent visible in code.
- **Composable:** methods return new boxes, so operations chain naturally.

<div class="result" markdown>

[Get started :material-arrow-right:](getting-started.md){ .md-button .md-button--primary }
[View the API :material-book-open-variant:](reference/api.md){ .md-button }

</div>
