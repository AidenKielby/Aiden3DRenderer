# Renderer

## Purpose

Renderer3D is the central runtime orchestrator of this library. It owns:

- Window and input lifecycle through pygame
- Camera state and menu state
- Geometry ingestion and per-frame projection
- Three rendering backends:
  - renderer_type.MESH
  - renderer_type.POLYGON_FILL
  - renderer_type.RASTERIZE
- Optional post-processing compute shader chain

It is both a top-level app loop and a low-level rendering primitive.

## Public Surface in This Module

### register_shape

Signature:

    register_shape(name: str, key=None, is_animated: bool = False, color: tuple[int] = None)

Behavior:

- Registers a shape generator into a global CUSTOM_SHAPES map.
- The function is consumed by built-in generators in shapes.py and by user-defined generators.
- When is_animated is True, Renderer3D calls the shape function with a time keyword argument.

Inferred parameter types:

- name: str
- key: pygame key constant or None
- is_animated: bool
- color: tuple[int, int, int] or None

### class Renderer3D

Constructor signature:

    Renderer3D(
        width=1000,
        height=1000,
        title="Aiden 3D Renderer",
        load_default_shapes: bool = True,
        resizable_window: bool = True,
    )

Key constructor transformations and side effects:

- pygame.init is called immediately.
- Window dimensions are rounded up to multiples of 16.
- A display window is created at construction time.
- A standalone moderngl context is created.
- On non-macOS, a built-in compute shader is created and bound.
- On macOS, compute shader is disabled by design.
- Built-in shapes are imported and reloaded when load_default_shapes is True.
- Default material is loaded from packaged asset fonts/not_a_font_but_whatever.png.

## Internal Model Contract

Renderer3D consumes model lists with this canonical shape:

    [vertices, faces, uvs, uv_faces, object_type, material]

Variants in live code:

- SKYBOX objects store a numeric texture index in slot 5 instead of Material.
- BILLBOARD objects append slot 6 as size.

Mutation semantics:

- add_obj mutates obj[5] by replacing it with an updated Material containing texture_index.
- add_entity mutates entity.model[5] in the same way.

## Data Lifecycle

### 1) Ingestion

Geometry enters by one of these paths:

- add_obj for loader-produced models
- add_entity for entity-wrapped models
- generate_shape path for procedural grid shapes
- generate_cubemap_skybox and generate_sprite_bilboard for special objects

### 2) Projection and clipping

- Procedural grids are converted by shape_to_verticies_faces.
- Camera transforms run through project_3d_to_2d or project_3d_to_2d_flat.
- Near-plane handling for object-format triangles is performed by clip_triangle_near.

### 3) Backend rendering

- MESH: line rendering via pygame.draw.line.
- POLYGON_FILL: CPU triangle list build, depth sort, fill draw.
- RASTERIZE: triangle packing into tri_dtype buffer, compute dispatch, GPU texture readback, blit.

### 4) Optional post-process

- run_compute_shaders executes a user-provided shader pipeline over output texture.
- Each entry may declare dynamic uniform inputs as literal values or callables.

## Method Reference (Selected High-Impact Methods)

### add_obj

Signature:

    add_obj(self, obj, bounding_box=None)

Expected inputs:

- obj: list-like model with at least 6 entries.
- obj[5] must be a Material-like object with texture_path.
- bounding_box: optional precomputed bounding box structure.

Failure states:

- IndexError when obj is shorter than expected.
- AttributeError when obj[5] does not expose texture_path.
- Image and GL errors may bubble from add_material.

### add_material

Signature:

    add_material(self, material: Material)

Behavior:

- Calls add_texture_for_raster(material.texture_path).
- Writes returned texture layer index to material.texture_index.
- Returns the same material object.

Failure states:

- FileNotFoundError or OSError from missing texture path in Image.open.
- moderngl errors from texture-array allocation/binding on GPU path.

### set_texture_for_raster

Signature:

    set_texture_for_raster(self, img_path)

Behavior:

- Replaces all raster textures with a single layer texture array.
- Resets self.textures mapping.
- Returns first layer index on non-macOS.

Failure states:

- FileNotFoundError or OSError on image load failure.
- Attribute and GL errors if shader bindings are unavailable.
- On macOS branch, function does not build compute-shader texture bindings.

### add_texture_for_raster

Signature:

    add_texture_for_raster(self, img_path)

Behavior:

- Appends a texture layer to array if path is new.
- If dimensions differ, new image is resized to first layer dimensions.
- Returns existing index for duplicate path.

Failure states:

- Same image and GL failure modes as set_texture_for_raster.

### set_rasterization_size

Signature:

    set_rasterization_size(self, size: tuple[int, int])

Behavior:

- Rounds both dimensions to multiples of 16.
- Reallocates output textures and clear buffer on non-macOS.

### render_shape_from_obj_format

Signature:

    render_shape_from_obj_format(self, matrix, texture_p)

Behavior by mode:

- RASTERIZE:
  - Converts triangles into structured NumPy tri buffer
  - Runs compute shader dispatch
  - Optionally runs chained post shaders
  - Reads back texture and scales to window
- POLYGON_FILL:
  - CPU clip/project, depth sort, fill polygons
- MESH:
  - CPU clip/project, draw triangle edges

Failure states:

- AttributeError when malformed model tuple is supplied.
- Potential moderngl errors in buffer upload, image binding, dispatch, readback.
- Internal broad exception handlers can swallow post-process failures.

### run

Signature:

    run(self)

Behavior:

- Infinite event/render loop until window close.
- Updates entities each frame and temporarily appends entity model to vertices_faces_list.
- Handles pause/settings UI and draw mode toggles.

Failure states:

- sys.exit is called from menu quit callback.
- Potential IndexError risk in cleanup loop when deleting multiple entity indices in ascending order.

### loopable_run

Signature:

    loopable_run(self)

Behavior:

- Single-frame variant of run for host-driven game loops.

Failure states:

- QUIT event branch assigns running = False without local definition in this method.
- This can raise NameError during QUIT handling.
- Same entity-index cleanup risk as run.

## Performance and Memory Context

### Procedural grid path

- shape_to_verticies_faces processes HxW grid points.
- Time complexity: O(H*W)
- Face count approaches 2*(H-1)*(W-1) for dense grids.
- Memory growth is linear in vertices and faces.

### CPU projection path

- project_3d_to_2d and project_3d_to_2d_flat are O(V), where V is number of input vertices.
- They aggressively emit None for clipped points to reduce downstream work.

### POLYGON_FILL mode

- Triangle list creation is O(T).
- Painter-order sort is O(T log T).
- Draw cost scales with number of visible triangles and rasterized area.

### RASTERIZE mode

- CPU preprocessing to build tri buffer is O(T).
- Built-in compute shader loops over all triangles for each pixel tile invocation.
- Effective shader work scales with pixel count times triangle count.
- GPU to CPU readback each frame copies raster buffer back to system memory before blit.
- Practical tuning knob: set_rasterization_size or set_rasterization_downsize.

## Real-World Usage Example

This example reflects realistic scene setup with textured model, skybox, billboard, and rasterization tuning.

```python
from aiden3drenderer import Renderer3D, renderer_type, obj_loader, dae_loader, Material

renderer = Renderer3D(width=1280, height=720, title="Scene Demo", load_default_shapes=False)
renderer.set_render_type(renderer_type.RASTERIZE)
renderer.using_obj_filetype_format = True
renderer.set_rasterization_downsize(0.6)

ship_mat = Material("ship", "./assets/ship.png", None)
ship = obj_loader.get_obj("./assets/ship.obj", material=ship_mat, scale=2.0)
renderer.add_obj(ship)

prop_mat = Material("prop", "./assets/prop.png", None)
prop = dae_loader.get_dae("./assets/prop.dae", material=prop_mat, offset=(2, 0, 1), scale=1.0)
renderer.add_obj(prop)

renderer.generate_cross_type_cubemap_skybox(40, "./assets/kisspng_skybox2.png")

sprite_mat = Material("marker", "./assets/pixelart_guy.png", None)
renderer.generate_sprite_bilboard(sprite_mat, pos=(0, 1.5, 3), size=1.2)

renderer.camera.position = [0, 1.5, -6]
renderer.camera.base_speed = 0.08
renderer.run()
```

## Empirical Verification Notes

- The module is heavily consumed by examples and demo entrypoints.
- Legacy example call sites still exist that pass old loader arguments in some files.
- Treat docs in this page as source-of-truth over outdated examples.

## Cross References

- [Camera](camera.md)
- [OBJ Loader](obj_loader.md)
- [DAE Loader](dae_loader.md)
- [Material](material.md)
- [Custom Shaders](custom_shaders.md)
- [Entities](entities.md)
- [Audit Report](audit_report.md)
