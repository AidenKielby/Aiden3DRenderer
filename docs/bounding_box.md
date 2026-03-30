# Bounding Box

`get_bounding_box(vertices, offset=(0,0,0)) -> list`

Compute an axis-aligned bounding box (AABB) for a list of 3D vertices and return a small model representing the box suitable for rendering.

Parameters
----------
- `vertices`: Iterable of 3-tuples/lists `(x,y,z)`.
- `offset`: Optional `(x,y,z)` translation applied to the box's vertices.

Return value
------------

Returns a model in the renderer's internal format: `[box_vertices, box_faces, [], [], object_type.OBJ]` where `box_vertices` are eight corner points and `box_faces` lists triangle indices.

Implementation details
----------------------

- Very small extents on any axis are padded by 0.3 units (the code checks for axis thickness < 1e-2) to avoid zero-volume AABBs which would fail overlap tests.

Example
-------

```python
from aiden3drenderer import bounding_box
model = bounding_box.get_bounding_box([(0,0,0),(1,1,1)])
```
