# Tutorials & Examples

This page collects short, focused tutorials to get you productive quickly.

Quick Start — Minimal Renderer

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.camera.position = [0, 0, 0]
renderer.render_type = renderer_type.POLYGON_FILL
renderer.run()
```

Loopable Run — Integrate game logic

Use `loopable_run()` in a manual loop when you want to perform per-frame updates before the renderer draws.

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.render_type = renderer_type.POLYGON_FILL

while True:
    # update game state, physics, AI, input, etc.
    renderer.loopable_run()
```

Load and display an OBJ

```python
from aiden3drenderer import Renderer3D, obj_loader, renderer_type, Material

renderer = Renderer3D(width=1000, height=1000)
renderer.render_type = renderer_type.POLYGON_FILL
renderer.using_obj_filetype_format = True

mat = Material('demo', './assets/alloy_forge_block.png', texture_index=0)
obj = obj_loader.get_obj('./assets/alloy_forge_block.obj', material=mat)
renderer.add_obj(obj)
renderer.run()
```

Add an `Entity` with gravity

```python
from aiden3drenderer import Renderer3D, Entity, obj_loader, Material

renderer = Renderer3D()
mat = Material('entity_mat', './assets/alloy_forge_block.png', texture_index=0)
obj = obj_loader.get_obj('./assets/alloy_forge_block.obj', material=mat)
entity = Entity(obj, renderer)
entity.toggle_gravity()
renderer.entities.append(entity)

while True:
    for e in renderer.entities:
        e.update()
    renderer.loopable_run()
```

Use the GPU rasterizer (when available)

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.set_render_type(renderer_type.RASTERIZE)
renderer.toggle_depth_view(True)
renderer.run()
```

Compute shader example outline

- Write a GLSL compute shader using `layout(std430, binding = X) buffer ...` and explicit `binding` on `uniform` samplers.
- Build a `CustomShader` with the source and call `set_buffer` to allocate SSBOs.
- Write your input arrays via `write_to_buffer` and dispatch the compute shader with `compute_shader.run(...)`.
- Read results back via `read_from_buffer`.
