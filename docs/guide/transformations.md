# Transformations

Transformations never mutate the source box. This makes pipelines easy to read and safe to reuse.

```python
from easy_bbox import Bbox

original = Bbox.from_tlbr((100, 50, 300, 250))
result = (
    original
    .shift(horizontal_shift=20, vertical_shift=-10)
    .scale(0.8)
    .expand_uniform(12)
    .clip_to_img(img_w=400, img_h=300)
)
```

## Move and resize

| Method | Effect |
| --- | --- |
| `shift(x, y)` | Moves every edge by the requested offset. |
| `scale(factor)` | Scales width and height around the box center. |
| `scale_area(factor)` | Scales area by `factor`, preserving the center; dimensions use `sqrt(factor)`. |

A scale factor of `0` produces a point at the center. Negative scale factors are rejected.

## Add space

`expand_uniform(padding)` adds the same padding to all four sides. `expand(left, top, right, bottom)` gives each side its own padding:

```python
box.expand_uniform(16)
box.expand(left=8, top=4, right=24, bottom=12)
```

`pad_to_square()` adds the minimum symmetric padding needed to make the box square. `pad_to_aspect_ratio(target_ratio)` does the same for a requested `width / height` ratio.

## Keep a box inside an image

```python
safe = box.clip_to_img(img_w=640, img_h=480)
```

This clamps left/top to zero and right/bottom to the image dimensions. It is particularly handy after augmentation or padding.

!!! warning "Clipping does not reject empty results"
    If a box is completely outside the image, clamping can result in a zero-area box at an image edge. Check `area` or `overlaps()` if your application requires visible boxes.
