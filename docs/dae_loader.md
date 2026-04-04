# DAE Loader

Parses COLLADA `.dae` files (reads geometry primitives: `triangles`, `polylist`, `polygons`) into the renderer's internal model format.

Signature
---------

`get_dae(file_path: str, material: Material, offset: tuple[float,float,float] = (0,0,0), scale: float = 1) -> list`

Compatibility note
------------------

`get_dae` now returns a `Material` object at model index `5`, matching `obj_loader.get_obj` and `Renderer3D.add_obj` expectations.

Notes
-----

- The function uses `lxml.etree` for XML parsing. If the `lxml` package is not installed the import will fail at module import time.
- The loader finds `source` elements with float arrays and uses the `accessor` `stride` attribute to split arrays into components (3 for positions, typically 2 for UVs).
- Faces are triangulated for polygons with >3 vertices.

Return value
------------

Returns the same internal model format used by the renderer:

```
[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, material]
```

Additional behavior
-------------------

- Uses `max(scale, 0)` so negative scales are clamped to `0`.
- If no vertices are found, the function returns an empty vertex list and any parsed faces/UV data without raising by default.

Exceptions
----------
- `OSError` / `FileNotFoundError` if the file cannot be opened.
- `lxml.etree.XMLSyntaxError` when parsing malformed XML.

Example
-------

```python
from aiden3drenderer import dae_loader, Renderer3D, Material

mat = Material('dae_mat', 'assets/model_texture.png', texture_index=0)
model = dae_loader.get_dae('assets/model.dae', material=mat, offset=(0,0,0), scale=1.0)

renderer = Renderer3D()
renderer.add_obj(model)
renderer.run()
```
