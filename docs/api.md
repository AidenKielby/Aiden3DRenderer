# API Reference

This reference documents the public surface of the `aiden3drenderer` package (the names imported into package root by `aiden3drenderer.__init__`). Each page links to a focused module reference with precise signatures, return values, and observed runtime exceptions.

Quick links (primary user-facing modules):

- [Renderer](renderer.md) — `Renderer3D`, `register_shape`, `renderer_type`
- [Camera](camera.md) — `Camera`
- [Material](material.md) — `Material`
- [OBJ Loader](obj_loader.md) — `get_obj`
- [DAE Loader](dae_loader.md) — `get_dae`
- [Entities](entities.md) — `Entity`
- [Physics](physics.md) — `ShapePhysicsObject`, `PhysicsObjectHandler`, `CameraPhysicsObject`
- [Shapes](shapes.md) — built-in `@register_shape` functions (procedural shapes)
- [Math Shape](math_shape.md) — `MathShape` equation-based shape registration helper
- [Custom Shaders](custom_shaders.md) — `CustomShader` (compute shader helper)
- [Video Renderer](video_renderer.md) — `VideoRenderer3D`, `VideoRendererObject` (see audit notes)
- [Demo Module](demo.md) — packaged demo entrypoints (`demo`, `demo_inv`, `demo_mac`)
- [Bounding Boxes](bounding_box.md) — `get_bounding_box`
- [Object Types](object_type.md) — `object_type` enum
- [Button](button.md) — `Button` UI helper

Public surface (as imported into package root by aiden3drenderer.__init__):

- `Renderer3D` — main application renderer class. See [Renderer](renderer.md).
- `register_shape` — decorator used by the built-in `shapes` module to register procedural shapes.
- `renderer_type` — enum used to select rendering backend (mesh, polygon-fill, rasterize).
- `object_type` — enum describing object semantics (OBJ, SKYBOX, BILLBOARD).
- `Camera` — camera controls and input handling. See [Camera](camera.md).
- `Material` — material container and `.mat` file parser. See [Material](material.md).
- `MathShape` — equation-driven shape registration helper. See [Math Shape](math_shape.md).
- `physics`, `obj_loader`, `dae_loader`, `bounding_box` — loader/utility modules; see their pages.
- `VideoRenderer3D`, `VideoRendererObject` — helper for offline video rendering (high-drift; see [audit_report](audit_report.md)).
- Console-script demo entrypoints are defined in `setup.py` and currently map to `aiden3drenderer.Demo.silly_skull`. See [Demo Module](demo.md).

Export caveat
-------------

`MathShape` is currently imported at package root in `__init__.py`, but it is missing from `__all__`. Direct imports work (`from aiden3drenderer import MathShape`), but wildcard imports (`from aiden3drenderer import *`) will not include it until `__all__` is updated.

Packaging metadata note
-----------------------

This repository currently defines package metadata in `setup.py` (version, dependencies, console scripts). No `pyproject.toml` file is present.

Current observed package version is `1.11.1` in both `aiden3drenderer/__init__.py` and `setup.py`.

If a page mentions an exception or platform requirement (OpenGL, lxml, PIL/Pillow), that reflects an explicit raise in the code path or a dependency used by the implementation.