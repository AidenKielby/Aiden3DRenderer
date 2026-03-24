# Usage & Controls

This page summarizes common configuration, runtime options, and controls.

Render modes
- `renderer_type.MESH` — fast wireframe-like mode showing edges.
- `renderer_type.POLYGON_FILL` — CPU fill path with triangle rasterization.
- `renderer_type.RASTERIZE` — GPU compute shader raster path (requires OpenGL 4.3+).

Runtime settings
- Toggle depth/heat diagnostic views in raster mode with `toggle_depth_view()` / `toggle_heat_map()`.
- `lighting_strictness` influences per-triangle light multiplier used in rasterization.
- `render_distance` controls how far objects are projected and rendered.

Textures
- Use `set_texture_for_raster(path)` or `add_texture_for_raster(path)` to supply texture layers for raster mode.
- OBJ UVs are parsed by `obj_loader.get_obj()` and used automatically by the rasterizer when present.

Controls
- `W/A/S/D` — Move camera forward/left/back/right
- `Space` — Move camera up
- `Left Shift` — Move camera down
- `Left Ctrl` — Speed boost
- Mouse wheel — Change camera FOV
- Arrow keys — Fine pitch/yaw adjustments
- Right mouse + drag — Mouse look
- `Esc` — Open pause/settings menu (when using `run()`)

Renderer fields you may want to tune
- `camera.base_speed` — base movement speed
- `camera.fov` — field of view (degrees)
- `rasterization_size` — internal GPU render buffer size (power-of-two friendly)
- `texture_layers` — list of loaded textures for raster mode

Platform notes
- On macOS compute shaders may not be available — `RASTERIZE` mode is only for OpenGL 4.3+ capable systems.
