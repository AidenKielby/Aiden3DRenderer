# OBJ Loader

Parses a subset of the Wavefront OBJ format and returns the renderer's internal model representation.

Signature
---------

`get_obj(file_path: str, texture_index: int, offset: tuple[float,float,float] = (0,0,0), scale: float = 1, type: str = 'normal') -> list`

Parameters
----------
- `file_path` (str): Path to the `.obj` file.
- `texture_index` (int): Index into the renderer texture array for this model's texture layer.
- `offset` (tuple): `(x,y,z)` applied to every vertex after scaling and centering.
- `scale` (float): Non-negative uniform scale (values < 0 are clamped to 0).
- `type` (str): Present for backwards compatibility; only `'normal'` is recognized.

Return value
------------

Returns the internal model format used by `Renderer3D`:

```
[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, texture_index]
```

- `vertices` — list of `[x,y,z]` floats (centered on geometric pivot and scaled).
- `vertex_faces` — list of 3-tuples of vertex indices.
- `tex_coords` — list of `[u,v]` UV coordinates found in `vt` lines.
- `texture_faces` — list of 3-tuples of UV indices corresponding to `vertex_faces` when `vt` data exists.

Behavior and limitations
------------------------

- Supports `v`, `vt`, and `f` with either `v/vt` or `v`-only face formats. Faces with more than three vertices are triangulated using a simple fan triangulation.
- Indices in OBJ files are converted from 1-based to 0-based.
- Very large OBJ files may allocate large NumPy arrays; callers should be mindful of memory use.

Exceptions
----------
- `FileNotFoundError` / `OSError` if the path cannot be opened.
- `ValueError` if numeric parsing fails on malformed lines.

Example
-------

```python
from aiden3drenderer import obj_loader, Renderer3D

model = obj_loader.get_obj('assets/alloy_forge_block.obj', texture_index=0, offset=(0,0,0), scale=1.0)
renderer = Renderer3D()
renderer.vertices_faces_list.append(model)
renderer.run()
```
