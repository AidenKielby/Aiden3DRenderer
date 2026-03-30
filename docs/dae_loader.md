# DAE Loader

Parses COLLADA `.dae` files (reads geometry primitives: `triangles`, `polylist`, `polygons`) into the renderer's internal model format.

Signature
---------

`get_dae(file_path: str, texture_index: int, offset: tuple[float,float,float] = (0,0,0), scale: float = 1) -> list`

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
from aiden3drenderer import dae_loader, Renderer3D

model = dae_loader.get_dae('assets/model.dae', texture_index=0, offset=(0,0,0), scale=1.0)
renderer = Renderer3D()
renderer.vertices_faces_list.append(model)
renderer.run()
```
