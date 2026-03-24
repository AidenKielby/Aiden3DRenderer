# Renderer

Detailed guide to the `Renderer3D` class and configuration options.

Overview
- `Renderer3D` is the main entry point for creating interactive or looped 3D scenes rendered with Pygame. It implements a custom projection pipeline, multiple render modes (mesh/fill/gpu rasterize), a simple UI, and helpers for OBJ/DAE loading.

Constructor
- `Renderer3D(width=1000, height=1000, title="Aiden 3D Renderer", load_default_shapes=True)`

Important attributes
- `width`, `height` — output size in pixels (internally rounded to multiples of 16 for GPU block sizing).
- `camera` — `Camera` instance used for view transforms.
- `render_type` — one of `renderer_type.MESH`, `renderer_type.POLYGON_FILL`, `renderer_type.RASTERIZE`.
- `entities` — list of `Entity` instances attached to the scene.
- `vertices_faces_list` — list of meshes / OBJs to render.
- `grid_coords_list` — list of procedural grid shapes used by the polygon renderer.
- `texture_layers` — list of textures used by the rasterizer.
- `compute_shader` / `compute_shader_container` — GPU rasterization compute shader (None on unsupported platforms).
- `tri_buffer` — buffer used to upload triangle data to the compute shader.

Key methods
- `run()` — start the built-in game loop with pause/settings UI. Blocks until exit.
- `loopable_run()` — run a single iteration of rendering/input updates; useful when you want to drive your own loop.
- `set_render_type(renderer_type.*)` — switch active render mode.
- `set_texture_for_raster(path)` / `add_texture_for_raster(path)` — set or append raster textures used by GPU rasterizer.
- `toggle_depth_view(bool)` / `toggle_heat_map(bool)` — enable diagnostic rendering modes in `RASTERIZE`.
- `set_starting_shape(name_or_none)` / `set_use_default_shapes(bool)` — control default procedural shapes loaded at startup.

Notes & platform specifics
- The GPU rasterizer uses a compute shader requiring OpenGL 4.3. On macOS native drivers this may not be available; the code falls back to CPU paths.
- The rasterization internal resolution is intentionally smaller than the window size (`rasterization_size`) and is upscaled to the screen.
- `Renderer3D` will load shapes from `aiden3drenderer.shapes` when `load_default_shapes` is True.

Example

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D(width=1200, height=800)
renderer.render_type = renderer_type.POLYGON_FILL
renderer.run()
```
