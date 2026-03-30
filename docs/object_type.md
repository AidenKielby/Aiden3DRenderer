# object_type

Simple enum used by the codebase to tag object semantics passed to the renderer and loaders.

Members
-------

- `object_type.OBJ` — Regular geometry loaded from OBJ/DAE or generated procedurally.
- `object_type.SKYBOX` — Skybox geometry; treated specially when rasterizing (uses `skyTex`).
- `object_type.BILLBOARD` — Screen‑facing sprite; projection code builds a quad facing the camera.

Usage
-----

This enum is part of the model tuple returned by `obj_loader.get_obj()` and `dae_loader.get_dae()`: the fifth element is an `object_type` value used by `Renderer3D` to pick projection and shading behaviour.

See also: [OBJ Loader](obj_loader.md), [DAE Loader](dae_loader.md), [Renderer](renderer.md).
