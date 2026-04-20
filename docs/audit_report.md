# Audit Report — Full Library Audit

Date: 2026-04-19

## Scope

This report documents a manual, source-first forensic audit of package code in `aiden3drenderer/` against `docs/`.

Audit method used for each module:

1. Static logic extraction from source.
2. Empirical verification from first-party tests when available.
3. Dependency mapping from in-repo usages.
4. Drift detection against current docs pages.

## Evidence quality note

The repository-level `tests/` directory contains no active first-party test modules in this snapshot (only `__pycache__/`).

Empirical behavior was therefore validated from:

- package source code
- packaged demo module
- first-party `examples/` call sites

## Public surface and packaging truth

- Public API root: `aiden3drenderer/__init__.py`
- Package version: `1.12.11` in both `aiden3drenderer/__init__.py` and `setup.py`
- Console scripts:
  - `aiden3d-demo` -> `aiden3drenderer.Demo.silly_skull:demo`
  - `inverted-aiden3d-demo` -> `aiden3drenderer.Demo.silly_skull:demo_inv`
  - `aiden3d-mac` -> `aiden3drenderer.Demo.silly_skull:demo_mac`
  - `shader-graph` -> `aiden3drenderer.ShaderGraph.gui:run`
- No `pyproject.toml` is present.

## Phase 1 — Matrix of Divergence (Pre-rewrite)

Status legend:

- `[ALIGNED]` code and docs match
- `[DRIFTED]` docs existed but diverged from runtime/source truth
- `[ORPHANED]` code existed without dedicated documentation coverage

| Source file | Documentation target | Pre-rewrite status | Notes |
| --- | --- | --- | --- |
| `aiden3drenderer/__init__.py` | `docs/api.md` | `[DRIFTED]` | Version/export notes were stale; `MathShape` caveat outdated. |
| `setup.py` | `docs/api.md` | `[DRIFTED]` | Version section in docs was stale. |
| `aiden3drenderer/bounding_box.py` | `docs/bounding_box.md` | `[ALIGNED]` | Signature and return contract matched. |
| `aiden3drenderer/button.py` | `docs/button.md` | `[ALIGNED]` | Behavior and public methods matched. |
| `aiden3drenderer/camera.py` | `docs/camera.md` | `[ALIGNED]` | Input behavior and fields matched. |
| `aiden3drenderer/custom_shader.py` | `docs/custom_shaders.md` | `[ALIGNED]` | Method surface and exceptions matched. |
| `aiden3drenderer/dae_loader.py` | `docs/dae_loader.md` | `[ALIGNED]` | Material-based return contract matched. |
| `aiden3drenderer/entity.py` | `docs/entities.md` | `[ALIGNED]` | `exec` scripting risk and update flow documented accurately. |
| `aiden3drenderer/material.py` | `docs/material.md` | `[ALIGNED]` | Field/method caveats matched source behavior. |
| `aiden3drenderer/math_shape.py` | `docs/math_shape.md` | `[ALIGNED]` | Type/complexity/security notes matched. |
| `aiden3drenderer/object_type.py` | `docs/object_type.md` | `[ALIGNED]` | Enum members and loader contracts matched. |
| `aiden3drenderer/obj_loader.py` | `docs/obj_loader.md` | `[ALIGNED]` | Signature and return model matched current code. |
| `aiden3drenderer/physics.py` | `docs/physics.md` | `[ALIGNED]` | Core classes/methods and integration flow matched. |
| `aiden3drenderer/renderer.py` | `docs/renderer.md` | `[ALIGNED]` | High-impact methods and known failure states matched current source. |
| `aiden3drenderer/shapes.py` | `docs/shapes.md` | `[DRIFTED]` | `generate_mandelbulb_slice` defaults/params were stale. |
| `aiden3drenderer/video_renderer.py` | `docs/video_renderer.md` | `[ALIGNED]` | Docs correctly captured known loader mismatch drift in runtime code. |
| `aiden3drenderer/Demo/__init__.py` | `docs/demo.md` | `[ALIGNED]` | Package wrapper behavior minimal and covered. |
| `aiden3drenderer/Demo/silly_skull.py` | `docs/demo.md` | `[DRIFTED]` | Docs still claimed an old loader mismatch that no longer exists. |
| `aiden3drenderer/ShaderGraph/__init__.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |
| `aiden3drenderer/ShaderGraph/shader_type.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |
| `aiden3drenderer/ShaderGraph/shader_target.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |
| `aiden3drenderer/ShaderGraph/element.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |
| `aiden3drenderer/ShaderGraph/elements.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |
| `aiden3drenderer/ShaderGraph/gui.py` | (none) | `[ORPHANED]` | No dedicated docs page existed. |

## Rewrite actions completed (docs-only)

- Added new page: `docs/shader_graph.md` to cover the entire `ShaderGraph` subpackage.
- Updated `docs/api.md` with current version, entrypoints, and corrected export caveat.
- Updated `docs/demo.md` to remove stale mismatch claims and document current real failure modes.
- Updated `docs/shapes.md` to match current `generate_mandelbulb_slice` signature/defaults.
- Updated navigation and landing pages:
  - `mkdocs.yml`
  - `docs/index.md`

## Highest-risk runtime findings (still in source)

These are source-runtime risks, not documentation errors:

1. `VideoRenderer3D` loader contract mismatch remains in source.
   - `video_renderer.py` calls `get_obj(shape_path)` and unpacks two values.
   - `obj_loader.get_obj` currently requires `material` and returns six fields.

2. `Renderer3D.loopable_run` QUIT-event path still uses undefined local `running`.
   - On QUIT events this can raise `NameError`.

3. Example drift exists in several `examples/` scripts.
   - Some examples still use old loader argument shapes (`texture_index=` style) inconsistent with current loaders.

## Current post-rewrite doc status summary

- Orphaned package modules documented: `ShaderGraph/*`
- Drifted docs corrected: API, Demo, Shapes, top-level nav/index
- Remaining docs are aligned to current source behavior as observed in this audit pass
