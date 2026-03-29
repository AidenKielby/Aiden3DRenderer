# OBJ Loader

`obj_loader.get_obj()` is a small OBJ parser used by the renderer and video tools. It supports vertex positions, UVs (`vt`) and automatically triangulates faces.

Function
- `get_obj(file_path: str, texture_index: int, offset=(0,0,0), scale=1, type='normal')`

Return value
- Returns a list: `[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, texture_index]` where:
  - `vertices` is a list of `[x,y,z]` floats (pivot-centered).
  - `vertex_faces` is a list of 3-tuples of vertex indices (triangulated faces).
  - `tex_coords` is a list of `[u,v]` coordinates parsed from `vt` lines.
  - `texture_faces` is a list of 3-tuples of texture coordinate indices aligned with `vertex_faces` when present.

Notes
- Faces with more than 3 vertices are triangulated using a fan triangulation which preserves vertex winding.
- The loader recenters the model around its geometric pivot so rotations occur about the model center by default.

Example

```python
from aiden3drenderer.obj_loader import get_obj

verts, faces, uvs, texfaces, typ, tex_idx = get_obj('./assets/model.obj', texture_index=0, offset=(0,0,0), scale=1)
```
