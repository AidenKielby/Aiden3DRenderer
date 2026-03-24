# DAE Loader

`dae_loader.get_dae(file_path, texture_index, offset=(0,0,0), scale=1)` parses COLLADA `.dae` files and extracts vertex positions, UVs, and triangulated faces.

Features
- Supports `triangles`, `polylist`, and `polygons` primitive types and will triangulate N-gons into triangles.
- Attempts to discover `POSITION` and `TEXCOORD` sources from COLLADA XML and respects accessor strides.
- Recenters the model around its geometric pivot and applies optional `offset` and `scale`.

Return
- Returns `[vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, texture_index]` — same format as `obj_loader.get_obj()` so the renderer treats them interchangeably.
