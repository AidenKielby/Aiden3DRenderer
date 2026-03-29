# Physics

Overview
- The `physics` module provides small helpers for simulating basic rigid-body style interactions mainly used for demo scenes: `ShapePhysicsObject`, `CameraPhysicsObject`, and `PhysicsObjectHandler`.

ShapePhysicsObject
- Constructor: `ShapePhysicsObject(renderer, shape, rotation, color, size, mass, grid_size)` where `shape` is `'sphere'` or `'plane'`.
- Common methods: `add_forces(force)`, `set_forces(force)`, `update_velocity_from_forces()`, `update_pos_from_velocity()`, `detect_collision(shapes)`.
- Visual helpers: `add_shape_to_renderer()` and `add_color_to_renderer()` push the computed vertex grid and colors into the renderer for visualization.

CameraPhysicsObject
- Wraps a `Camera` with physical properties (mass/height/hitbox) so the camera can be moved by physics forces and collide with shapes.

PhysicsObjectHandler
- Manage many physics shapes and camera wrappers. Use `add_shape()`, `add_camera()`, and `handle_shapes()` each frame to update physics and push visual geometry to the renderer.

Example pattern

```python
from aiden3drenderer import Renderer3D, physics

renderer = Renderer3D()
obj_handler = physics.PhysicsObjectHandler()

ball = physics.ShapePhysicsObject(renderer, 'sphere', (0,0,0), (100,100,255), 4, 2.5, 8)
ball.anchor_position = [0,0,0]
obj_handler.add_shape(ball)

while True:
    ball.add_forces((0,-0.18,0))
    obj_handler.handle_shapes()
    renderer.loopable_run()
```
