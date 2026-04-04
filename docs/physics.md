# Physics

High-level physics utilities used by demos and example code. This module provides simple rigid-body-like primitives (`ShapePhysicsObject`) and a `PhysicsObjectHandler` that advances physics and projects shapes into the renderer each frame.

Class: ShapePhysicsObject
-------------------------

Constructor
	ShapePhysicsObject(renderer: Renderer3D, shape: str, rotation: tuple[float], color: tuple[int], size: float, mass: float, grid_size: float)

- `shape` must be one of `"sphere"` or `"plane"`; other values raise `ValueError`.
- For `plane` the object is created using `shapes.generate_plane(...)` and a `plane_normal` / `plane_point` are computed for collision.

Key methods
	- `rotate_xyz(pos, rx, ry, rz)` — rotate a point by Euler angles.
	- `add_forces(force: tuple[float])` — accumulate a force vector.
	- `set_forces(force: tuple[float])` — set forces absolutely.
	- `update_velocity_from_forces()` — simple Euler integration: v += (forces / mass) * timeStep.
	- `update_pos_from_velocity()` — anchor_position += velocity.
	- `apply_anchor_position_to_grid_coords()` — returns a copy of `grid_coords` translated by `anchor_position` for rendering.
	- `add_shape_to_renderer()` — append the translated grid coords to `renderer.grid_coords_list` (so the renderer can project and draw it).
	- `add_color_to_renderer()` — append color hints for triangle rendering.
	- `detect_collision(shapes)` — naive pairwise sphere/plane overlap tests; calls `handle_collision` when collisions are found.
	- `handle_collision(other_shape, n)` — resolve collisions with either sphere or plane.

Class: CameraPhysicsObject
-------------------------

Thin wrapper that links a `Camera` to physics. Provides a hitbox (`hitbox_size`) and `detect_colission` that resolves collisions between the camera box and physics shapes.

Class: PhysicsObjectHandler
---------------------------

Manages lists of `ShapePhysicsObject` and `CameraPhysicsObject` instances and advances them in `handle_shapes()`:

- For each shape: integrate velocity, update position, detect collisions, append the object's projected mesh to the renderer, then clear forces.
- For each camera: update anchor position, detect collisions, and write the camera position back to the renderer.

Exceptions and pitfalls
----------------------

- The physics is intentionally simple (Euler integration, naive collision tests) and not suitable for production physics. It is intended for demo/sandbox usage.
- `ValueError` is raised by the constructor if `shape` is not recognized.

Example
-------

```python
from aiden3drenderer import physics, Renderer3D

renderer = Renderer3D(width=900, height=700, title='Physics Sandbox')
handler = physics.PhysicsObjectHandler()
plane = handler.add_plane(renderer, (0,-1,0), (0,0,0), (200,200,200), size=20, grid_size=20)
ball = physics.ShapePhysicsObject(renderer, 'sphere', (0,0,0), (255,0,0), size=1, mass=1.0, grid_size=8)
handler.add_shape(ball)

while True:
	ball.add_forces((0, -0.18, 0))
	handler.handle_shapes()
	renderer.loopable_run()
```

Note: current source has a known `loopable_run()` QUIT-event bug; if you need stable window-close behavior, use `run()` based integration until that source path is fixed.
