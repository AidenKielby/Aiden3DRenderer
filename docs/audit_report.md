# Audit Report — Full Library Audit

Date: 2026-04-03

Scope
-----

This report summarizes a deep, manual audit of the `Aiden3DRenderer` package source (package root `aiden3drenderer/`) and the existing `docs/` material. I compared the live Python source to the docs and updated the `docs/` files to reflect the code's real behavior.

Package metadata source
-----------------------

The repository currently uses `setup.py` for packaging metadata and console entry points. No `pyproject.toml` file exists in the project root.

Method
------

- Read `aiden3drenderer/__init__.py` to identify public surface area.
- Opened each module referenced in `__all__` and traced public functions and classes to understand inputs, outputs, side effects, and exceptions.
- Compared each `docs/*.md` file with code and updated the docs to match the implementation.

Summary of changes
------------------

- Rewrote `api.md`, `renderer.md`, `camera.md`, `shapes.md`, `entities.md`, `obj_loader.md`, `dae_loader.md`, `physics.md`, `custom_shaders.md`, `video_renderer.md`, `button.md`, `bounding_box.md`, and `object_type.md` to match the current code.
- Added `material.md` to document the `Material` class now exported by `aiden3drenderer.__init__`.
- Corrected stale usage snippets in `tutorials.md` to use the current `obj_loader.get_obj(file_path, material, ...)` API.

Source-to-doc relationship map
------------------------------

- `aiden3drenderer/renderer.py` -> `docs/renderer.md`
- `aiden3drenderer/camera.py` -> `docs/camera.md`
- `aiden3drenderer/material.py` -> `docs/material.md`
- `aiden3drenderer/obj_loader.py` -> `docs/obj_loader.md`
- `aiden3drenderer/dae_loader.py` -> `docs/dae_loader.md`
- `aiden3drenderer/entity.py` -> `docs/entities.md`
- `aiden3drenderer/physics.py` -> `docs/physics.md`
- `aiden3drenderer/custom_shader.py` -> `docs/custom_shaders.md`
- `aiden3drenderer/video_renderer.py` -> `docs/video_renderer.md`
- `aiden3drenderer/bounding_box.py` -> `docs/bounding_box.md`
- `aiden3drenderer/object_type.py` -> `docs/object_type.md`
- `aiden3drenderer/button.py` -> `docs/button.md`
- `aiden3drenderer/shapes.py` -> `docs/shapes.md`
- `aiden3drenderer/__init__.py` -> `docs/api.md` (public API export map)

High‑drift findings (priority fixes)
----------------------------------

1. VideoRenderer / OBJ loader signature mismatch
   - `video_renderer.VideoRenderer3D.__init__` calls `get_obj(shape_path)` and unpacks to two variables.
   - Current `obj_loader.get_obj` requires `material: Material` and returns a 6-item model list (`[verts, faces, uvs, uv_faces, object_type, material]`).
   - This is a runtime-breaking incompatibility; constructor and `add_shape` paths are affected.

2. DAE loader / Renderer integration mismatch
   - `dae_loader.get_dae` returns `texture_index` (int) at model index `5`.
   - `Renderer3D.add_obj` expects index `5` to be `Material` and calls `add_material(material)`, which accesses `material.texture_path`.
   - Result: DAE output is not directly compatible with `add_obj` without conversion.

3. Public API drift: newly exported `Material` class was undocumented
   - `aiden3drenderer.__init__` exports `Material`, but docs previously had no dedicated page or API link.
   - This is now resolved by adding `docs/material.md` and linking from `api.md` and `index.md`.

4. Silent exception handling and broad try/except usage
   - Many non-critical paths use bare `except:` which hides useful errors (e.g., texture load failures, moderngl errors). Recommendation: tighten except clauses and log exceptions to stderr to aid debugging.

5. Security: `Entity.use_scripts()` executes arbitrary Python via `exec()`
   - This is an intentional design but must be highlighted. Docs now include a security warning.

6. Platform-specific behavior for compute shaders
   - The compute shader path is disabled on macOS (`sys.platform == 'darwin'`). The docs now call this out and warn about OpenGL 4.3 requirements.

Other observations
------------------

- `CustomShader` uses a heuristic GLSL parser which works for the project's shaders but is not robust for complex declarations.
- `VideoRenderer3D.render()` performs per-pixel CPU rasterization; its performance characteristics are documented in the updated docs.

Recommended follow-ups (non-blocking)
------------------------------------

- Replace broad `except:` blocks with targeted exception handling and add logging (or re-raise after logging) for recoverable errors.
- Add unit tests for loader functions (`obj_loader`, `dae_loader`) and for the `CustomShader` parser to prevent regression.
- Consider sanitizing or removing `exec`-based scripting and replacing it with a safer callback interface.

Files changed
-------------

- Updated: `docs/api.md`, `docs/renderer.md`, `docs/camera.md`, `docs/shapes.md`, `docs/entities.md`, `docs/object_type.md`, `docs/obj_loader.md`, `docs/dae_loader.md`, `docs/physics.md`, `docs/custom_shaders.md`, `docs/video_renderer.md`, `docs/button.md`, `docs/bounding_box.md`, `docs/tutorials.md`, `docs/index.md`
- Added: `docs/material.md`
- Added: `docs/audit_report.md`

Next steps
----------

- Patch `video_renderer.py` to use `Material` and consume the new `get_obj` return shape.
- Decide whether `dae_loader.get_dae` should return a `Material` (to match OBJ flow) or whether `Renderer3D.add_obj` should accept both `Material` and `texture_index`.
- Add focused tests for public signatures and loader behavior to prevent future docs drift.
