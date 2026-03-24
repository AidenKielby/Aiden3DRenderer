# Object Types

`object_type` is a small `Enum` describing how the renderer should treat a mesh:

- `object_type.OBJ` — regular 3D mesh with vertex positions and faces.
- `object_type.SKYBOX` — special-cased skybox meshes / textures.
- `object_type.BILLBOARD` — 2D billboard objects (planar sprites).

Most loader helpers return the enum value as part of the mesh tuple so renderers can switch behavior when necessary.
