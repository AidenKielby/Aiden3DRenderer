# API Reference

This reference documents the public surface of the `aiden3drenderer` package (the names exported by `aiden3drenderer.__init__`). Each page links to a focused module reference with precise signatures, return values, and observed runtime exceptions.

Quick links (primary user-facing modules):

- [Renderer](renderer.md) — `Renderer3D`, `register_shape`, `renderer_type`
- [Camera](camera.md) — `Camera`
- [OBJ Loader](obj_loader.md) — `get_obj`
- [DAE Loader](dae_loader.md) — `get_dae`
- [Entities](entities.md) — `Entity`
- [Physics](physics.md) — `ShapePhysicsObject`, `PhysicsObjectHandler`, `CameraPhysicsObject`
- [Shapes](shapes.md) — built-in `@register_shape` functions (procedural shapes)
- [Custom Shaders](custom_shaders.md) — `CustomShader` (compute shader helper)
- [Video Renderer](video_renderer.md) — `VideoRenderer3D`, `VideoRendererObject` (see audit notes)
- [Bounding Boxes](bounding_box.md) — `get_bounding_box`
- [Object Types](object_type.md) — `object_type` enum
- [Button](button.md) — `Button` UI helper

Public surface (as exported by aiden3drenderer.__init__):

- `Renderer3D` — main application renderer class. See [Renderer](renderer.md).
- `register_shape` — decorator used by the built-in `shapes` module to register procedural shapes.
- `renderer_type` — enum used to select rendering backend (mesh, polygon-fill, rasterize).
- `object_type` — enum describing object semantics (OBJ, SKYBOX, BILLBOARD).
- `Camera` — camera controls and input handling. See [Camera](camera.md).
- `physics`, `obj_loader`, `dae_loader`, `bounding_box` — loader/utility modules; see their pages.
- `VideoRenderer3D`, `VideoRendererObject` — helper for offline video rendering (high-drift; see [audit_report](audit_report.md)).

If a page mentions an exception or platform requirement (OpenGL, lxml, PIL/Pillow), that reflects an explicit raise in the code path or a dependency used by the implementation.