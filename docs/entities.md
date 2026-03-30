# Entity — runtime object wrapper

Purpose
-------

`Entity` is a small runtime wrapper around a model (the same internal `[verts, faces, ...]` format used elsewhere) that provides position/rotation/velocity, optional scripted behaviour (via embedded Python), and automatic bounding-box synchronization.

Constructor
-----------

`Entity(model, renderer, start_velocity: list[float] = [0,0,0], starting_rotation: list[float] = [0,0,0], bounding_box = None)`

- `model` — a model in the renderer's internal format (`[vertices, faces, uvs, uv_faces, object_type, texture_index]`).
- `renderer` — `Renderer3D` instance used for collision queries and rendering context.
- `bounding_box` — optional precomputed bounding box structure.

Security note (important)
-------------------------

`Entity` supports attaching scripts (strings of Python) which are executed via `exec()` inside a prepared globals dict. This enables flexible per-entity behaviors (e.g., gravity script included by default), but it is an explicit security risk: do NOT execute untrusted scripts.

Major methods & behavior
------------------------

- `add_script(script: str)` — append a script string to `self.scripts`. Scripts are executed every `update()` call by `use_scripts()`.
- `check_for_collison(bounding_boxes: Optional[list] = None) -> list[int]` — AABB-based collision test against a list of bounding boxes (defaults to `renderer.bounding_boxes`). Returns indices of colliding boxes.
- `sync_bounding_box()` — Recomputes the entity's `bounding_box` from `self.model[0]` using `bounding_box.get_bounding_box`.
- `toggle_gravity()` — toggles a built-in gravity script; when enabled it appends the library's `GRAVITY_SCRIPT` to `self.scripts`.
- `apply_velocity()` — moves `position` by `velocity * delta_time`. If a collision is detected immediately after movement it reverts the positional change (simple positional resolution).
- `center_vertices()` — returns vertices translated to current `position` so the entity's model is centered at `position`.
- `rotate()` — applies Euler rotation deltas to the model vertices and updates `self.model[0]`.
- `use_scripts()` — executes each script in `self.scripts` with `self.variables` as globals. Default variables include `entity` and `renderer`.
- `update()` — high-level per-frame update: sets `delta_time`, applies velocity, recenters vertices, rotates, syncs bounding box, runs scripts, and updates `last_rotation`.
- `get_entity() -> list` — returns the underlying model structure (suitable for passing to `Renderer3D.add_obj`).

Exceptions and pitfalls
----------------------

- Scripts executed by `use_scripts()` can raise arbitrary exceptions — they are not sandboxed. The renderer does not attempt to catch script-level exceptions inside `use_scripts()`.
- `sync_bounding_box()` will call into `bounding_box.get_bounding_box`; malformed models (empty vertex lists) may raise `ValueError` or `IndexError` from NumPy operations.

Example
-------

```python
from aiden3drenderer import Entity, obj_loader, Renderer3D

renderer = Renderer3D()
obj = obj_loader.get_obj('./assets/alloy_forge_block.obj', texture_index=0)
entity = Entity(obj, renderer)
entity.toggle_gravity()
renderer.add_entity(entity)
renderer.run()
```

See also: [Physics](physics.md) for higher-level physics objects and handlers.
