# OBJ Loader

Parses a subset of the Wavefront OBJ format and returns the renderer's internal model representation.

Signature
---------

`get_obj(file_path: str, material: Material, offset: tuple[float,float,float] = (0,0,0), scale: float = 1, type: str = 'normal') -> list`

Parameters
----------
- `file_path` (str): Path to the `.obj` file.
- `material` (`Material`): Material object associated with this mesh. The loader carries this object in the returned model tuple.
- `offset` (tuple): `(x,y,z)` applied to every vertex after scaling and centering.
- `scale` (float): Non-negative uniform scale (values < 0 are clamped to 0).
- `type` (str): Present for backwards compatibility; only `'normal'` is recognized.

Return value
------------

Returns the internal model format used by `Renderer3D`:

```
[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, material]
```

- `vertices` — list of `[x,y,z]` floats (centered on geometric pivot and scaled).
- `vertex_faces` — list of 3-tuples of vertex indices.
- `tex_coords` — list of `[u,v]` UV coordinates found in `vt` lines.
- `texture_faces` — list of 3-tuples of UV indices corresponding to `vertex_faces` when `vt` data exists.

The loader computes the mesh pivot as `(min + max) / 2` and applies scale/offset around that pivot.

Behavior and limitations
------------------------

- Supports `v`, `vt`, and `f` with either `v/vt` or `v`-only face formats. Faces with more than three vertices are triangulated using a simple fan triangulation.
- Indices in OBJ files are converted from 1-based to 0-based.
- Very large OBJ files may allocate large NumPy arrays; callers should be mindful of memory use.
- If `type` is not recognized, the function prints a warning and still returns the normal object layout.

Exceptions
----------
- `FileNotFoundError` / `OSError` if the path cannot be opened.
- `ValueError` if numeric parsing fails on malformed lines.
- `ValueError` from NumPy reductions if no vertices are parsed (empty/invalid OBJ data).

Example
-------

```python
from aiden3drenderer import obj_loader, Material, Renderer3D

material = Material(
	name='alloy',
	texture_path='assets/alloy_forge_block.png',
	texture_index=0,
)

model = obj_loader.get_obj('assets/alloy_forge_block.obj', material=material, offset=(0,0,0), scale=1.0)
renderer = Renderer3D()
renderer.add_obj(model)
renderer.run()
```
