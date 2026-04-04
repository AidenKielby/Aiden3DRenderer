# DAE Loader

Parses COLLADA `.dae` files (reads geometry primitives: `triangles`, `polylist`, `polygons`) into the renderer's internal model format.

Signature
---------

`get_dae(file_path: str, texture_index: int, offset: tuple[float,float,float] = (0,0,0), scale: float = 1) -> list`

Compatibility warning
---------------------

`Renderer3D.add_obj` currently expects a `Material` object at model index `5`. `get_dae` currently returns an integer `texture_index` at index `5`, so raw `get_dae` output is not directly compatible with `add_obj` without conversion.

Notes
-----

- The function uses `lxml.etree` for XML parsing. If the `lxml` package is not installed the import will fail at module import time.
- The loader finds `source` elements with float arrays and uses the `accessor` `stride` attribute to split arrays into components (3 for positions, typically 2 for UVs).
- Faces are triangulated for polygons with >3 vertices.

Return value
------------

Returns the same internal model format used by the renderer:

```
[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, texture_index]
```

Exceptions
----------
- `OSError` / `FileNotFoundError` if the file cannot be opened.
- `lxml.etree.XMLSyntaxError` when parsing malformed XML.

Example
-------

```python
from aiden3drenderer import dae_loader, Renderer3D, Material

model = dae_loader.get_dae('assets/model.dae', texture_index=0, offset=(0,0,0), scale=1.0)

# Convert index 5 to Material to match Renderer3D.add_obj expectations.
model[5] = Material('dae_mat', 'assets/model_texture.png', texture_index=model[5])

renderer = Renderer3D()
renderer.add_obj(model)
renderer.run()
```
