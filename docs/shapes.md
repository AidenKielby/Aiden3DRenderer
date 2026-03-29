# Shapes & Custom Shape API

This document explains the `@register_shape` API and the built-in procedural shapes.

Registering shapes
- Use the `register_shape(name, key=None, is_animated=False, color=None)` decorator to add a shape to the runtime menu.
- Shape generator signature: `def func(grid_size=40, frame=0): -> list[list[tuple|None]]` — return a rectangular matrix of vertex tuples or `None`.
- Example:

```python
from aiden3drenderer import register_shape
import pygame

@register_shape('MyPlane', key=pygame.K_p, is_animated=False, color=(200,255,150))
def my_plane(grid_size=40, frame=0):
    return [[(x,0,z) for x in range(grid_size)] for z in range(grid_size)]
```

Built-in shapes
- The package includes many built-in generators in `aiden3drenderer.shapes` (mountain, waves, ripple, torus, sphere, mobius, megacity, mandelbulb, etc.).

Rules & best practices
- The returned matrix must be rectangular (every row the same length) to avoid `IndexError` during traversal.
- Animated shapes should use the `frame` or `time` parameter to produce time-varying coordinates.
- Shapes may return `None` in cells to indicate holes/culling.
