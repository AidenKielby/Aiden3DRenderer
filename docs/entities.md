# Entities

This guide describes the `Entity` helper used to attach runtime behaviour and simple physics/collision to meshes.

Overview
- `Entity` wraps a model (vertices + faces) and exposes per-entity state: `position`, `rotation`, `velocity`, `bounding_box`, and `delta_time`.
- Entities can hold executable Python `scripts` (strings) that run via `exec()` in a namespace exposing `entity` and `renderer` by default.

Key API
- `Entity(model, renderer, start_velocity=[0,0,0], starting_rotation=[0,0,0], bounding_box=None)` — constructor.
- `add_script(script_str)` — append a Python script string to run each update.
- `toggle_gravity()` — enable/disable built-in gravity script.
- `update()` — apply velocity, center vertices, rotate, sync bounding box, and execute scripts.
- `check_for_collison(bounding_boxes=None)` — AABB overlap test against renderer bounding boxes; returns indices of collisions.
- `sync_bounding_box()` — regenerate bounding box from model vertices using the renderer's `bounding_box` helper.

Scripting details
- Scripts run with `exec(script, variables)` where `variables` contains `entity` (the Entity instance) and `renderer` (the Renderer3D instance).
- You can add custom variables/functions using `add_entity_variable(name, variable)` and `add_entity_function(name, function)`.
- Example gravity script (built-in) demonstrates velocity clamping, collision detection, and positional snapping.

Bounding boxes & collisions
- Entities expect AABB-style bounding boxes. The renderer populates `renderer.bounding_boxes` which `Entity.check_for_collison()` compares against.
- Collision resolution in the built-in gravity script chooses the shallowest overlap axis and snaps the entity to prevent sinking.

Example

```python
from aiden3drenderer import Renderer3D, Entity, obj_loader

renderer = Renderer3D()
obj = obj_loader.get_obj('./assets/alloy_forge_block.obj')
entity = Entity(obj, renderer)
entity.toggle_gravity()
renderer.entities.append(entity)

while True:
    for e in renderer.entities:
        e.update()
    renderer.loopable_run()
```

Notes & best practices
- Scripts executed via `exec()` run in-process and can execute arbitrary code — treat input scripts as trusted only.
- Keep `delta_time`-dependent logic consistent by reading `entity.delta_time` or `renderer.delta_time`.
- If you need more sophisticated physics, consider extending or replacing the built-in gravity script with custom logic in `add_script()`.
