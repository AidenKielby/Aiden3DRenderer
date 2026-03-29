# Bounding Boxes

`bounding_box.get_bounding_box(vertices, offset=(0,0,0))` constructs an axis-aligned bounding box mesh from a list of vertices.

Details
- Returns a mesh in the same `[vertices, faces, tex_coords, texture_faces, object_type]` format used across the package.
- Pads zero-thickness axes slightly to avoid degenerate AABB overlaps.

Usage

```python
from aiden3drenderer.bounding_box import get_bounding_box
box = get_bounding_box(model_vertices, offset=(0,0,0))
```
