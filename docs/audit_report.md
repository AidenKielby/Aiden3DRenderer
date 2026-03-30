# Audit Report — Full Library Audit

Date: 2026-03-29

Scope
-----

This report summarizes a deep, manual audit of the `Aiden3DRenderer` package source (package root `aiden3drenderer/`) and the existing `docs/` material. I compared the live Python source to the docs and updated the `docs/` files to reflect the code's real behavior.

Method
------

- Read `aiden3drenderer/__init__.py` to identify public surface area.
- Opened each module referenced in `__all__` and traced public functions and classes to understand inputs, outputs, side effects, and exceptions.
- Compared each `docs/*.md` file with code and updated the docs to match the implementation.

Summary of changes
------------------

- Rewrote `api.md`, `renderer.md`, `camera.md`, `shapes.md`, `entities.md`, `obj_loader.md`, `dae_loader.md`, `physics.md`, `custom_shaders.md`, `video_renderer.md`, `button.md`, `bounding_box.md`, and `object_type.md` to match the current code.

High‑drift findings (priority fixes)
----------------------------------

1. VideoRenderer / OBJ loader signature mismatch
   - `aiden3drenderer.video_renderer.VideoRenderer3D.__init__` calls `get_obj(shape_path)` without the `texture_index` argument required by `aiden3drenderer.aiden3drenderer.obj_loader.get_obj(file_path, texture_index, ...)`.
   - Some built artifacts in `build/lib` contain an older `obj_loader` signature without `texture_index`; this explains why examples in the repo sometimes work. Fix: update the constructor to call `get_obj(shape_path, 0)` or change `obj_loader.get_obj` to accept an optional `texture_index` with a default.

2. Silent exception handling and broad try/except usage
   - Many non-critical paths use bare `except:` which hides useful errors (e.g., texture load failures, moderngl errors). Recommendation: tighten except clauses and log exceptions to stderr to aid debugging.

3. Security: `Entity.use_scripts()` executes arbitrary Python via `exec()`
   - This is an intentional design but must be highlighted. Docs now include a security warning.

4. Platform-specific behavior for compute shaders
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

- Updated: `docs/api.md`, `docs/renderer.md`, `docs/camera.md`, `docs/shapes.md`, `docs/entities.md`, `docs/object_type.md`, `docs/obj_loader.md`, `docs/dae_loader.md`, `docs/physics.md`, `docs/custom_shaders.md`, `docs/video_renderer.md`, `docs/button.md`, `docs/bounding_box.md`
- Added: `docs/audit_report.md`

Next steps
----------

- I can: (A) open a follow-up patch to fix the `video_renderer.py` / `obj_loader.py` signature mismatch; (B) tighten exception handling in strategic places; or (C) run tests and smoke the renderer on this machine. Which would you like me to prioritize?
