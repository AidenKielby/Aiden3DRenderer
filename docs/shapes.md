# Shapes — built-in procedural generators

The `shapes` module contains a set of procedural generators registered with `register_shape`. Each generator returns a 2D grid (list of rows) where every cell is either a 3‑tuple `(x, y, z)` or `None`. These grids are consumed by `Renderer3D` (when default shapes are enabled) and can also be used directly by callers.

Registration pattern
--------------------

All functions are decorated with the package-level `@register_shape(name, key, is_animated, color)` decorator. That makes them available to the renderer and assigns an optional keyboard shortcut.

Common return format
---------------------

Each function returns `grid_coords: list[list[tuple[float, float, float] | None]]`.

Built-in shape generators (signature and short description)
---------------------------------------------------------

- `generate_mountain(grid_size: int = 20)` — procedural mountain heightfield.
- `generate_waves(grid_size: int = 30, time: float = 0)` — animated sine-wave terrain.
- `generate_ripple(grid_size: int = 25, time: float = 0)` — radial ripple from center, animated.
- `generate_canyon(grid_size: int = 30)` — U-shaped valley terrain with small noise.
- `generate_pyramid(grid_size: int = 15)` — stepped square pyramid.
- `generate_spiral(grid_size: int = 25, time: float = 0)` — spiral-shaped heightfield (animated).
- `generate_torus(resolution: int = 30)` — parametric torus (donut) mesh.
- `generate_sphere(resolution: int = 20, radius: float = 5)` — sphere sampled into latitude/longitude rows.
- `generate_mobius_strip(resolution: int = 30)` — Möbius strip parametric surface.
- `generate_megacity(grid_size: int = 80)` — procedural city block generator.
- `generate_alien_landscape(grid_size: int = 60, time: float = 0)` — composite animated alien terrain.
- `generate_double_helix(length: int = 60, time: float = 0)` — DNA-like double helix (animated).
- `generate_mandelbulb_slice(resolution: int = 50, z_slice: float = 0, max_iterations: int = 10)` — approximate 3D fractal slice.
- `generate_klein_bottle(resolution: int = 40)` — Klein bottle parametric surface.
- `generate_trefoil_knot(resolution: int = 50)` — trefoil knot geometry.
- `generate_plane(size: int = 5, rot_x: float = 0, rot_y: float = 0, rot_z: float = 0)` — flat grid centered at origin; rotations are in radians.

Example: register and use a custom shape
----------------------------------------

```python
from aiden3drenderer import register_shape, Renderer3D
import pygame

@register_shape('hill', pygame.K_h, is_animated=False, color=(200,150,100))
def my_hill(grid_size=20):
	grid = []
	for x in range(grid_size):
		row = []
		for z in range(grid_size):
			y = max(0, 5 - ((x - grid_size/2)**2 + (z - grid_size/2)**2)**0.5)
			row.append((x, y, z))
		grid.append(row)
	return grid

renderer = Renderer3D()
renderer.set_starting_shape('hill')
renderer.run()
```

Notes
-----

- Generators are purely functional and return their grid; they do not mutate renderer state themselves.
- `is_animated=True` implies the renderer will call the function with a `time` keyword argument each frame.
- For equation-driven dynamic shape registration, see [Math Shape](math_shape.md).
