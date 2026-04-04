# object_type

Simple enum used by the codebase to tag object semantics passed to the renderer and loaders.

Members
-------

- `object_type.OBJ` — Regular geometry loaded from OBJ/DAE or generated procedurally.
- `object_type.SKYBOX` — Skybox geometry; treated specially when rasterizing (uses `skyTex`).
- `object_type.BILLBOARD` — Screen‑facing sprite; projection code builds a quad facing the camera.

Usage
-----

This enum is part of the model tuple returned by loaders: the fifth element is an `object_type` value used by `Renderer3D` to pick projection and shading behaviour.

- OBJ loader shape: `[vertices, faces, uvs, uv_faces, object_type, material]`
- DAE loader shape: `[vertices, faces, uvs, uv_faces, object_type, texture_index]` (currently not directly compatible with `Renderer3D.add_obj` without conversion)

See also: [OBJ Loader](obj_loader.md), [DAE Loader](dae_loader.md), [Renderer](renderer.md).
