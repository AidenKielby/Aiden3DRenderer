# Audit Report — Full Library Audit

Date: 2026-04-04

Scope
-----

This report documents a manual, source-first audit of package code in `aiden3drenderer/` against docs in `docs/`.

Supreme-directive compliance
----------------------------

- Manual source reading only (no audit automation scripts).
- No source (`.py`) edits were made.
- Documentation changes are based on directly observed runtime code paths and signatures.

Public surface and packaging truth
----------------------------------

- Public API source: `aiden3drenderer/__init__.py`
   - Root imports include `Renderer3D`, `register_shape`, `renderer_type`, `object_type`, `Camera`, `Material`, `MathShape`, `Entity`, `CustomShader`, `VideoRenderer3D`, `VideoRendererObject`, plus utility modules.
   - `__version__` is `1.11.1`.
- Packaging metadata source: `setup.py` (also version `1.11.1`).
- No `pyproject.toml` is present in the repository root.

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
- `aiden3drenderer/math_shape.py` -> `docs/math_shape.md`
- `aiden3drenderer/video_renderer.py` -> `docs/video_renderer.md`
- `aiden3drenderer/bounding_box.py` -> `docs/bounding_box.md`
- `aiden3drenderer/object_type.py` -> `docs/object_type.md`
- `aiden3drenderer/button.py` -> `docs/button.md`
- `aiden3drenderer/shapes.py` -> `docs/shapes.md`
- `aiden3drenderer/Demo/silly_skull.py` -> `docs/demo.md`
- `aiden3drenderer/__init__.py` + `setup.py` -> `docs/api.md`

Highest-drift findings (current)
--------------------------------

1. VideoRenderer / OBJ loader contract mismatch (runtime-breaking)
   - `VideoRenderer3D.__init__` and `VideoRenderer3D.add_shape` call `get_obj(shape_path)` and unpack 2 values.
   - Current `obj_loader.get_obj` requires `material` and returns 6 values.
   - Effect: constructor/add-shape paths can fail before rendering with `TypeError` or unpacking errors.

2. `loopable_run` QUIT-event path uses undefined local
   - In `Renderer3D.loopable_run`, handling `QUIT` executes `running = False` but no local `running` is initialized in that function.
   - Effect: QUIT event can raise `NameError` in loopable mode.

3. VideoRenderer rotation-rate semantics do not match field name
   - Source computes `rot_per_f = rotations_per_seccond * fps`.
   - The name suggests per-second input, but multiplying by FPS creates very large per-frame increments.
   - Effect: rotations are typically much faster than implied by public field naming.

4. Broad exception swallowing in renderer/shader integration
   - Multiple non-critical paths use broad exception catches.
   - Effect: failures can be silently ignored, increasing debugging difficulty.

5. `Entity` script execution is intentionally unsafe by design
   - `Entity.use_scripts()` executes attached script strings with `exec`.
   - Effect: untrusted scripts are a security risk and should never be loaded.

6. Packaged demo entrypoints currently use stale loader argument shape
   - `Demo/silly_skull.py` calls `obj_loader.get_obj(path, renderer.add_texture_for_raster(...), ...)`.
   - Current `get_obj` expects `material: Material`.
   - Effect: packaged `aiden3d-demo` entrypoints may fail at runtime until source is updated.

7. Public API export list drift (`MathShape`)
   - `__init__.py` imports `MathShape` at package root.
   - `__all__` currently omits `MathShape`.
   - Effect: direct import works, but wildcard import will not include `MathShape`.

Drift resolved in this docs pass
--------------------------------

- DAE docs were stale relative to current source.
  - Current source now accepts/returns `Material` in `dae_loader.get_dae` model index `5`.
  - Updated docs now reflect parity with `obj_loader` and `Renderer3D.add_obj` model contracts.
- Previously orphaned demo module coverage was added.
   - `Demo/silly_skull.py` behavior and current mismatch status are now documented in `docs/demo.md`.
- Newly added source module `math_shape.py` is now documented.
   - Added `docs/math_shape.md` and wired API/navigation links.

Files updated in this correction pass
-------------------------------------

- `docs/api.md`
- `docs/dae_loader.md`
- `docs/object_type.md`
- `docs/renderer.md`
- `docs/usage.md`
- `docs/video_renderer.md`
- `docs/audit_report.md`
- `docs/demo.md`
- `docs/math_shape.md`
- `docs/tutorials.md`
- `docs/physics.md`
- `docs/index.md`
- `docs/shapes.md`
- `mkdocs.yml`

Recommended remediation sequence
-------------------------------

1. Fix `video_renderer.py` to pass `Material` into `get_obj` and handle the 6-item return model.
2. Fix `Renderer3D.loopable_run` QUIT handling to avoid undefined `running` usage.
3. Clarify or correct VideoRenderer rotation semantics (`rotations_per_seccond` vs per-frame increment math).
4. Replace broad exception catches with targeted exceptions plus logging in shader and texture paths.
