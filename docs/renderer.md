# Renderer

Purpose
-------

`Renderer3D` is the primary application-class that wires together input (pygame), CPU fallbacks, and an optional ModernGL-based rasterization path (compute-shader). It implements three rendering backends:

- `renderer_type.MESH` — simple wireframe lines (fast, CPU)
- `renderer_type.POLYGON_FILL` — CPU triangle fill path
- `renderer_type.RASTERIZE` — ModernGL / compute-shader rasterization (requires OpenGL 4.3+; disabled on macOS)

Architectural overview (why)
----------------------------

The renderer exposes both an interactive runtime (`run()` / `loopable_run()`) for live applications and a low-level API that allows callers to provide vertex/face data in the library's internal format:

```
[vertices, faces, uvs, uv_faces, object_type, texture_index]
```

This design separates model loading (OBJ/DAE), per-frame projection, and the final rasterization step so advanced users can preprocess geometry, run off-line passes, or chain compute shaders.

Important platform notes
------------------------

- The compute-shader rasterizer is automatically disabled on macOS (the code checks `sys.platform == 'darwin'`).
- ModernGL is used with a standalone context; a working OpenGL driver is required for rasterization.
- The renderer initializes `pygame` (display, fonts). Creating `Renderer3D` has side effects on process windowing.

register_shape(name: str, key=None, is_animated: bool = False, color: tuple[int] = None)
-----------------------------------------------------------------------

Decorator used by the `shapes` module to register procedural shapes. When a function is decorated it is available via `Renderer3D.generate_shape()` and (when `load_default_shapes=True`) is auto-loaded at construction.

Signature
    register_shape(name: str, key=None, is_animated: bool = False, color: tuple[int] = None)

Behavior
    - `name` (str): identifier used by `Renderer3D.set_starting_shape` and keyboard selection.
    - `key` (pygame key constant or None): If provided and the renderer is polling keys, pressing that key selects the shape.
    - `is_animated` (bool): When True the shape function is called with `time` each frame; otherwise called with no args.
    - `color` (tuple[int,int,int] or None): optional base color used for triangle color lists.

Example
```
from aiden3drenderer import register_shape
@register_shape('myshape', pygame.K_m, is_animated=False, color=(100,150,200))
def myshape(grid_size=20):
    # return grid matrix: list[list[(x,y,z)]]
    ...
```

class Renderer3D
----------------

Constructor
    Renderer3D(width: int = 1000,
               height: int = 1000,
               title: str = "Aiden 3D Renderer",
               load_default_shapes: bool = True,
               resizable_window: bool = True)

Key instance attributes
    - `camera` (`Camera`): camera control instance.
    - `render_type` (`renderer_type`): current rendering backend.
    - `vertices_faces_list` (list): user-supplied geometry in the internal format.
    - `texture_layers` (list): raw image arrays used by the rasterizer.
    - `compute_shader` / `compute_shader_container` (`CustomShader`): only present when compute shaders are enabled.
    - `rasterization_size` (tuple[int,int]): internal buffer size used by compute shader path (rounded to 16 multiples).

Important notes on construction
    - The constructor calls `pygame.init()` and opens a window; creating the object is not side-effect free.
    - If `load_default_shapes=True` the package's `shapes` module is imported and decorated shapes are registered.

Selected methods (signature, behavior, exceptions)
    add_obj(obj: list, bounding_box: Optional[list] = None) -> None
        Append an already-parsed object (format returned by `obj_loader.get_obj` / `get_dae`) to the renderer. If `bounding_box` is provided it is appended to `renderer.bounding_boxes`.

    add_entity(entity: Entity) -> None
        Append an `Entity` instance; `run()` will call `entity.update()` each frame.

    set_rasterization_size(size: tuple[int,int]) -> None
        Set internal raster buffer size. Each dimension is rounded up to the next multiple of 16. Reallocates ModernGL textures when available.

    toggle_depth_view(b: bool) -> None
    toggle_heat_map(b: bool) -> None
        Toggle diagnostic views for the compute-shader rasterizer. If compute shaders are not available these flags are stored but do not run.

    set_render_type(type: renderer_type) -> None
        Switch between `renderer_type.MESH`, `renderer_type.POLYGON_FILL`, and `renderer_type.RASTERIZE`.

    set_texture_for_raster(img_path: str) -> None
        Load a single RGBA image and create a `moderngl.TextureArray` used by the rasterizer. Under the hood uses `PIL.Image.open`.

        Raises:
            - `FileNotFoundError` or `OSError` if the image path cannot be opened.
            - `moderngl.Error` if texture creation fails (backend specific).

    add_texture_for_raster(img_path: str) -> Optional[int]
        Add another layer to the rasterizer texture array. Returns the new layer index when successful.

    generate_cubemap_skybox(radius: int, texture_path: str, left_uvs, right_uvs, top_uvs, bottom_uvs, forward_uvs, backward_uvs) -> None
        Convenience to create a skybox mesh that uses `skybox_texture` (bound separately). Will call `Image.open` and may raise if the file is missing.

    generate_sprite_bilboard(texture_path: str, pos=(0,0,0), size: float = 1) -> None
        Adds a `BILLBOARD` object and registers the provided texture into the texture array.

    project_3d_to_2d(...), project_3d_to_2d_flat(...)
        Core projection helpers. They return lists parallel to input geometry where off-screen or unclippable vertices are replaced with `None`.

    render_shape_from_obj_format(matrix, texture_p) -> None
        The compute-shader path: converts projected triangles into the `tri_dtype` SSBO layout, uploads the buffer, dispatches the shader, then converts the texture back to a pygame Surface.

        Observed runtime caveats:
            - `tri_dtype` size is precomputed and the code attempts to reuse a large reserved buffer. If the number of triangles exceeds the reserved size, behavior depends on the GPU driver and may raise `moderngl.Error`.
            - Many internal operations use `try/except` and silently ignore failures — the renderer attempts to remain tolerant of optional features.

    run() -> None
        Enter the main event loop. Handles input, updates entities, projects geometry, chooses the active renderer, draws UI overlays, and blocks until the window closes or `sys.exit()` is called (e.g., Quit button triggers `sys.exit()`).

    loopable_run() -> None
        Run a single frame worth of the renderer loop (useful when embedding the renderer into a larger game loop). Similar behavior to `run()` but does not loop.

Error and exception hygiene
--------------------------

- Many file/driver operations rely on external libraries (PIL, moderngl, numpy). Typical exceptions include `FileNotFoundError`, `OSError`, and `moderngl.Error` when running raster code.
- The code often catches exceptions broadly (bare `except:`) in non-critical paths. When a call is swallowed you may find a missing texture or shader silently disabled — check console logs and returned values.

Real‑world usage
----------------

Minimal interactive example:

```python
from aiden3drenderer import Renderer3D, renderer_type, obj_loader

renderer = Renderer3D(width=800, height=600)
renderer.set_render_type(renderer_type.POLYGON_FILL)

# Load an OBJ and append it in the library's internal format
obj = obj_loader.get_obj('./assets/alloy_forge_block.obj', texture_index=0)
renderer.add_obj(obj)

renderer.run()
```

Notes about loading models
-------------------------

- `obj_loader.get_obj(file_path, texture_index, ...)` and `dae_loader.get_dae(...)` both return the internal format used by the renderer: `[vertices, faces, uvs, uv_faces, object_type.OBJ, texture_index]`.
- When using the rasterizer, ensure textures supplied with `set_texture_for_raster` / `add_texture_for_raster` are the same resolution and RGBA.

Cross references
----------------

- See [Camera](camera.md) for camera controls and input mapping.
- See [OBJ Loader](obj_loader.md) and [DAE Loader](dae_loader.md) for model import details.
- See [Custom Shaders](custom_shaders.md) for building compute shaders and using SSBOs with the renderer.

High‑drift note
---------------

This module is a large surface with many helper functions. The docs and the implementation were reconciled in this audit — however some example code elsewhere (notably `video_renderer.py`) appears to call model loaders with incompatible signatures. See [audit_report](audit_report.md) for known mismatches and suggested fixes.
