<div align="center">

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/aiden3drenderer?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/aiden3drenderer)
[![PyPI version](https://img.shields.io/pypi/v/aiden3drenderer?color=green)](https://pypi.org/project/aiden3drenderer/)
[![Python Versions](https://img.shields.io/pypi/pyversions/aiden3drenderer)](https://pypi.org/project/aiden3drenderer/)
![Per Month](https://img.shields.io/pypi/dm/aiden3drenderer)
[![License: MIT](https://img.shields.io/pypi/l/aiden3drenderer)](https://github.com/AidenKielby/3D-mesh-Renderer/blob/main/LICENSE)
[![PyPI status](https://img.shields.io/pypi/status/aiden3drenderer)](https://pypi.org/project/aiden3drenderer/)
[![GitHub stars](https://img.shields.io/github/stars/AidenKielby/3D-mesh-Renderer?style=social)](https://github.com/AidenKielby/3D-mesh-Renderer/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/AidenKielby/3D-mesh-Renderer)](https://github.com/AidenKielby/3D-mesh-Renderer/commits/main)

</div>

# Aiden3DRenderer
A lightweight but capable 3D renderer for Python + Pygame with custom projection math, first-person camera controls, procedural geometry, OBJ support, basic physics, and an optional GPU raster path.

## Feature List (Clickable)

Every item below links to its explanation section.

- [**Custom 3D Projection**](#custom-3d-projection) - Projection pipeline implemented manually (no external 3D engine).
- [**First-Person Camera (6-DOF)**](#first-person-camera-6-dof) - Mouse look + keyboard movement with speed control.
- [**15+ Procedural Shape Generators**](#15-procedural-shape-generators) - Mountains, cities, fractals, knots, and more.
- [**Real-Time Rendering**](#real-time-rendering) - Designed for responsive live rendering workflows.
- [**Animated Terrains**](#animated-terrains) - Time-based procedural surfaces.
- [**Extensible Shape API**](#extensible-shape-api) - Register your own shapes with `@register_shape`.
- [**Multiple Object Support**](#multiple-object-support) - Render multiple meshes/shapes in one scene.
- [**Per-Shape Colors**](#per-shape-colors) - Custom colors for polygon/raster workflows.
- [**Simple Physics Engine**](#simple-physics-engine) - Basic forces and collisions for spheres/planes/camera.
- [**OBJ Loading**](#obj-loading) - Load and render `.obj` files with triangulation and UV parsing.
- [**Rasterization Paths**](#rasterization-paths) - CPU fill path + GPU compute-shader raster path.
- [**Three Render Modes**](#three-render-modes) - `MESH`, `POLYGON_FILL`, and `RASTERIZE`.
- [**Raster Debug Views**](#raster-debug-views) - Depth and heat-map diagnostics.
- [**Texture Mapping**](#texture-mapping) - UV texture sampling in raster mode.
- [**Multi-Texture Pipeline**](#multi-texture-pipeline) - Multiple texture layers selectable per OBJ.
 - [**Rasterization Paths**](#rasterization-paths) - CPU fill path + GPU compute-shader raster path.
 - [**Three Render Modes**](#three-render-modes) - `MESH`, `POLYGON_FILL`, and `RASTERIZE`.
 - [**Raster Debug Views**](#raster-debug-views) - Depth and heat-map diagnostics.
 - [**Texture Mapping**](#texture-mapping) - UV texture sampling in raster mode.
 - [**Multi-Texture Pipeline**](#multi-texture-pipeline) - Multiple texture layers selectable per OBJ.
 - [**Entities**](#entities) - Lightweight in-scene entities with scripted behaviour, bounding boxes, and basic collision support.
 - [**Custom Shaders**](#custom-shaders) - Helper wrapper for OpenGL compute shaders with SSBO/uniform helpers.
- [**Runtime Shape Management**](#runtime-shape-management) - Toggle built-in defaults while running.
- [**Skybox Rendering**](#skybox-rendering) - Generate cubemap skyboxes from UVs or cross atlas layouts.
- [**Pause + Settings UI**](#pause--settings-ui) - Tune mode, FOV, debug views, and lighting live.
- [**Video Renderer (Experimental)**](#video-renderer) - Render OBJ animation clips to video output.
- [**macOS GPU Note**](#macos-gpu-note) - Compute-shader limitation and VM workaround.

## Gallery

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="media/RenderShowcase.gif" alt="Ripple Animation" width="400"/>
        <br/>
        <b>Ripple Effect</b>
        <br/>
        <i>Expanding waves from center</i>
      </td>
      <td align="center">
        <img src="media/plateau_thing.png" alt="Mandelbulb Fractal" width="400"/>
        <br/>
        <b>Mandelbulb Slice</b>
        <br/>
        <i>3D fractal cross-section</i>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="media/Spiral.gif" alt="Turning Spiral" width="400"/>
        <br/>
        <b>Turning Spiral</b>
        <br/>
        <i>Screw-like surface animation</i>
      </td>
      <td align="center">
        <img src="media/City.png" alt="Simple City (laggy when solid render)" width="400"/>
        <br/>
        <b>Simple City</b>
        <br/>
        <i>Large procedural city terrain</i>
      </td>
      <tr>
      <td align="center">
        <img src="media/DualObjMesh.png" alt="Tree Mesh" width="400"/>
        <br/>
        <b>Tree Mesh</b>
        <br/>
        <i>Wireframe OBJ rendering</i>
      </td>
      <td align="center">
        <img src="media/DualObjFull.png" alt="Tree Solid Render" width="400"/>
        <br/>
        <b>Tree Solid Render</b>
        <br/>
        <i>Filled rendering from same scene</i>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="media/ColorTree.png" alt="Colored Tree" width="400"/>
        <br/>
        <b>Colored Tree</b>
        <br/>
        <i>Per-shape color update showcase</i>
      </td>
      <td align="center">
        <img src="media/PhysicsDemo.gif" alt="Physics Demo" width="400"/>
        <br/>
        <b>Physics Demo</b>
        <br/>
        <i>Collision and motion in scene</i>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="media/skull_with_skybox.png" alt="Skull and Skybox" width="400"/>
        <br/>
        <b>Skull + Skybox</b>
        <br/>
        <i>OBJ + environment background</i>
      </td>
      <td align="center">
        <img src="media/MinecraftBoatWireframe.png" alt="Minecraft Boat Wireframe" width="400"/>
        <br/>
        <b>Minecraft Boat Wireframe</b>
        <br/>
        <i>Complex model wireframe preview</i>
      </td>
    </tr>
  </table>
</div>

## Installation

```bash
pip install aiden3drenderer
```

Requirements:
- Python 3.11+
- Pygame 2.6.0+ (installed automatically)

## Quick Start

### Minimal Example

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.camera.position = [0, 0, 0]
renderer.render_type = renderer_type.POLYGON_FILL
renderer.run()
```

### Looped Run Example

Use `loopable_run()` when you want to integrate custom game logic each frame.

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.render_type = renderer_type.POLYGON_FILL

while True:
    # Custom logic here
    renderer.loopable_run()
```

### Runtime Pause/Settings

Press `Esc` during `run()` to open the runtime menu.

You can:
- Switch render mode (`MESH` / `POLYGON_FILL` / `RASTERIZE`)
- Toggle raster debug views (depth/heat)
- Adjust FOV
- Adjust lighting strictness
- Toggle OBJ render mode handling

## Feature Explanations

### Custom 3D Projection
The renderer uses a full world-to-screen pipeline implemented in Python:
1. Translate vertices into camera space.
2. Apply yaw/pitch/roll rotations.
3. Perspective divide by depth with FOV scaling.
4. Map to screen coordinates.

No external 3D engine is required for the core projection math.

### First-Person Camera (6-DOF)
Camera movement is designed for interactive exploration:
- Movement: `W/A/S/D`, `Space`, `Left Shift`
- Speed boost: `Left Ctrl`
- Rotation: right mouse drag + arrow key nudging
- FOV tweak: mouse wheel

### 15+ Procedural Shape Generators
Built-in generators include mathematical and stylized surfaces such as:
- Mountain, canyon, pyramid, torus, sphere
- Mobius strip, megacity, mandelbulb slice
- Klein bottle, trefoil knot
- Animated waves/ripples/spirals/alien terrain/double helix

### Real-Time Rendering
The engine is designed for live rendering loops and interactive scenes. Typical scenes can run smoothly at real-time frame rates depending on selected mode and geometry complexity.

### Animated Terrains
Animated shapes use the `frame` parameter inside shape generators. This enables time-driven deformation without changing the API shape contract.

### Extensible Shape API
Create custom shapes using `@register_shape`.

```python
from aiden3drenderer import Renderer3D, register_shape
import pygame

@register_shape("My Plane", key=pygame.K_p, is_animated=False, color=(200, 255, 150))
def generate_plane(grid_size=40, frame=0):
    return [
        [(1, 1, 1), (2, 1, 1), (3, 1, 1)],
        [(1, 1, 2), (2, 1, 2), (3, 1, 2)],
        [(1, 1, 3), (2, 1, 3), (3, 1, 3)],
    ]

renderer = Renderer3D()
renderer.run()
```

Important shape rule:
- Return a rectangular matrix (`list[list[tuple | None]]`) where all rows have the same length.

### Multiple Object Support
You can render multiple objects at once by appending several shape/OBJ entries to the active scene list.

### Per-Shape Colors
Shapes can define explicit base colors in registration, which are respected in filled/raster workflows.

### Simple Physics Engine
Physics module supports basic rigid-body style interactions:
- Sphere objects
- Plane colliders
- Gravity/forces
- Sphere-sphere and sphere-plane collision handling
- Camera physics wrapper support

For a full example, see the [Physics](#physics) section below.

### Entities

Lightweight in-scene `Entity` objects are provided to attach models to simple runtime behaviour. Key points:
- Entities wrap a model (vertices/faces) and expose a small API: `add_script(script_str)`, `toggle_gravity()`, `update()`, and helpers to add variables/functions accessible to scripts.
- Scripts are plain Python strings executed with `exec()` in a sandboxed-ish `variables` namespace; the default namespace contains `entity` and `renderer`.
- Built-in gravity script and collision helpers allow snapping, terminal velocity, and simple positional resolution using the renderer's `bounding_boxes`.
- Entities maintain `position`, `rotation`, `velocity`, a `bounding_box`, and `delta_time` and are updated each frame via `Entity.update()`.

Example:

```python
from aiden3drenderer import Renderer3D, Entity, obj_loader

renderer = Renderer3D()
obj = obj_loader.get_obj("./assets/alloy_forge_block.obj")
entity = Entity(obj, renderer)
entity.toggle_gravity()
renderer.entities.append(entity)

while True:
  for e in renderer.entities:
    e.update()
  renderer.loopable_run()
```

### OBJ Loading
OBJ workflow supports standard model loading with extra quality-of-life features:
- Load from file path
- Parse UV (`vt`) data for raster texturing
- Triangulate faces with more than 3 vertices
- Per-object offset and `texture_index` support

For full usage, see [OBJ Loading](#obj-loading).

### Rasterization Paths
Two fill/raster workflows are available:
- CPU software triangle filling (`POLYGON_FILL`)
- GPU compute-shader rasterization (`RASTERIZE`)

### Custom Shaders

`CustomShader` is a small helper around a ModernGL compute shader that parses buffer/uniform declarations and exposes simple helpers:
- Create with shader source and an optional ModernGL context: `CustomShader(shader_code, context=ctx)`.
- Allocate SSBO-style buffers via `set_buffer(name, element_count, element_size=None)` which binds storage buffers by layout binding.
- Write to buffers/uniforms with `write_to_buffer(name, bytes)` and `write_to_uniform(name, value_or_bytes)`.
- Read results back from buffers with `read_from_buffer(name, num_elements, element_type='vec3')` which returns a NumPy array.

Example usage:

```python
from aiden3drenderer.custom_shader import CustomShader
shader_src = """#version 430
layout(std430, binding=0) buffer mybuf { vec4 data[]; };
void main(){ /* ... */ }
"""

cs = CustomShader(shader_src, context=renderer.ctx)
cs.set_buffer('mybuf', element_count=1024, element_size=16)
# write raw bytes (numpy.tobytes()) and dispatch via cs.compute_shader
```

### Three Render Modes
Switch with `renderer.render_type`:
- `renderer_type.MESH`
- `renderer_type.POLYGON_FILL`
- `renderer_type.RASTERIZE`

### Raster Debug Views
When using `RASTERIZE` mode:
- `toggle_depth_view(True)` for depth visualization
- `toggle_heat_map(True)` for heat-map diagnostics

### Texture Mapping
Apply texture sampling in raster mode using image files and OBJ UV coordinates.

### Multi-Texture Pipeline
Add multiple texture layers and assign each OBJ to one via `texture_index`.

```python
from aiden3drenderer import Renderer3D, obj_loader, renderer_type

renderer = Renderer3D(width=1000, height=800)
renderer.render_type = renderer_type.RASTERIZE
renderer.using_obj_filetype_format = True

renderer.add_texture_for_raster("./assets/model1.png")  # index 0
renderer.add_texture_for_raster("./assets/model2.png")  # index 1

obj1 = obj_loader.get_obj("./assets/model1.obj", texture_index=0)
obj2 = obj_loader.get_obj("./assets/model2.obj", texture_index=1, offset=(6, 0, 0))

renderer.vertices_faces_list.append(obj1)
renderer.vertices_faces_list.append(obj2)
renderer.run()
```

### Runtime Shape Management
Enable or disable built-in shape set at runtime:

```python
renderer = Renderer3D(load_default_shapes=False)
renderer.set_use_default_shapes(True)
```

### Skybox Rendering
Skyboxes can be generated from:
- Explicit cubemap UV mappings
- Cross-layout atlas images via `generate_cross_type_cubemap_skybox(...)`

### Pause + Settings UI
`Esc` opens a pause/settings UI while running. Use it for fast iteration without restarting your app.

### Video Renderer
The package includes an experimental OBJ-to-video renderer:
- Uses the same projection concepts as live renderer
- Supports per-object transforms and rotation rates
- Suitable for simple pre-rendered clips

More details in [Video Renderer](#video-renderer).

### macOS GPU Note
`RASTERIZE` mode requires OpenGL 4.3 compute shaders, which are not available natively on macOS.
Use `MESH`/`POLYGON_FILL` on macOS, or see [VM Workaround for macOS](#vm-workaround-for-macos).

## Renderer Modes and Debugging

```python
from aiden3drenderer import Renderer3D, renderer_type

renderer = Renderer3D()
renderer.render_type = renderer_type.RASTERIZE
renderer.set_texture_for_raster("./assets/alloy_forge_block.png")
renderer.toggle_depth_view(True)
renderer.run()
```

## Creating Custom Shapes

Shape functions must return a rectangular vertex matrix. Jagged rows can cause `IndexError` during mesh traversal.

### Advanced Shape Example

```python
from aiden3drenderer import Renderer3D, register_shape
import pygame

@register_shape("My Pyramid", key=pygame.K_p, is_animated=False)
def generate_pyramid(grid_size=40, frame=0):
    matrix = []
    center = grid_size / 2

    for x in range(grid_size):
        row = []
        for y in range(grid_size):
            dx = abs(x - center)
            dy = abs(y - center)
            max_dist = max(dx, dy)
            height = max(0, 10 - max_dist)
            row.append((x, height, y))
        matrix.append(row)

    return matrix

renderer = Renderer3D()
renderer.run()
```

## Physics

### About

Physics in Aiden3DRenderer is intentionally lightweight and extensible.

You can:
- Create sphere and plane physics objects
- Apply forces and impulses
- Simulate collisions
- Attach a physics camera
- Manage everything through `PhysicsObjectHandler`

### Example: Two Colliding Spheres

```python
from aiden3drenderer import Renderer3D, physics, renderer_type


def main():
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")

    shape = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), (100, 0, 0), 5, 20, 20)
    shape.add_forces((-0.7, 0, 0))
    shape.anchor_position = [20, 0, 0]

    shape1 = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), (50, 0, 0), 5, 10, 20)
    shape1.add_forces((0.7, 0, 0))
    shape1.anchor_position = [0, 0, 0]

    obj_handler = physics.PhysicsObjectHandler()
    obj_handler.add_shape(shape)
    obj_handler.add_shape(shape1)

    renderer.set_starting_shape(None)
    renderer.camera.position = [0, 0, 0]
    renderer.render_type = renderer_type.POLYGON_FILL

    while True:
        obj_handler.handle_shapes()
        renderer.loopable_run()


if __name__ == "__main__":
    main()
```

### Example: Balls in a Box + Camera Physics

```python
from aiden3drenderer import Renderer3D, physics, renderer_type


def main():
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")
    obj_handler = physics.PhysicsObjectHandler()

    plane_color = (200, 200, 200)
    plane_size = 28
    grid_size = 8

    obj_handler.add_plane(renderer, [0, -14, 0], (0, 0, 0), plane_color, plane_size, grid_size)
    obj_handler.add_plane(renderer, [-14, 0, 0], (0, 0, 90), plane_color, plane_size, grid_size)
    obj_handler.add_plane(renderer, [14, 0, 0], (0, 0, 90), plane_color, plane_size, grid_size)
    obj_handler.add_plane(renderer, [0, 0, -14], (90, 0, 0), plane_color, plane_size, grid_size)
    obj_handler.add_plane(renderer, [0, 0, 14], (90, 0, 0), plane_color, plane_size, grid_size)

    ball_color = (100, 100, 255)
    ball_radius = 4
    ball_mass = 2.5
    ball_grid = 8

    ball1 = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), ball_color, ball_radius, ball_mass, ball_grid)
    ball1.anchor_position = [0, 0, 0]

    ball2 = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), ball_color, ball_radius, ball_mass, ball_grid)
    ball2.anchor_position = [9, 0, 0]

    gravity = (0, -0.18, 0)
    ball1.add_forces((1, 0, 1))

    camera = physics.CameraPhysicsObject(renderer, renderer.camera, 1, 10)
    obj_handler.add_camera(camera)

    obj_handler.add_shape(ball1)
    obj_handler.add_shape(ball2)

    renderer.set_starting_shape(None)
    renderer.render_type = renderer_type.POLYGON_FILL
    renderer.camera.base_speed = 1.2

    while True:
        ball1.add_forces(gravity)
        ball2.add_forces(gravity)
        camera.add_forces(tuple(v * 100 for v in gravity))
        obj_handler.handle_shapes()
        renderer.loopable_run()


if __name__ == "__main__":
    main()
```

## OBJ Loading

### Example

```python
from aiden3drenderer import Renderer3D, obj_loader, renderer_type


def main():
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")

    renderer.current_shape = None
    renderer.camera.position = [0, 0, 0]
    renderer.render_type = renderer_type.POLYGON_FILL
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/alloy_forge_block.obj", texture_index=0)
    renderer.vertices_faces_list.append(obj)

    renderer.run()


if __name__ == "__main__":
    main()
```

### Notes

- `obj_loader.get_obj(path, texture_index, offset=(x, y, z))` supports per-object texture selection and world-space offset.
- N-gon faces are triangulated automatically.
- UV coordinates (`vt`) are parsed for texture mapping in raster mode.
- Cross-layout skybox helper: `generate_cross_type_cubemap_skybox(radius, img_path)`.

## Video Renderer

A lightweight experimental renderer for creating video clips from OBJ scenes.

### Basic Usage

```python
from aiden3drenderer.video_renderer import VideoRenderer3D, VideoRendererObject

obj = VideoRendererObject("assets/alloy_forge_block.obj")
obj.rotations_per_seccond = [10, 25, 0]
obj.rotation = [0, 0, 0]

vr = VideoRenderer3D(width=800, height=600, fps=30, shapes=[obj])
vr.render("out.avi", duration_s=5, verbose=True)
```

### Multiple Objects

```python
from aiden3drenderer.video_renderer import VideoRenderer3D, VideoRendererObject

o1 = VideoRendererObject("assets/model1.obj")
o1.rotations_per_seccond = [0, 40, 0]

o2 = VideoRendererObject("assets/model2.obj")
o2.rotations_per_seccond = [10, 0, 5]
o2.anchor_pos = [4, 0, 8]

vr = VideoRenderer3D(width=1200, height=800, fps=24, shapes=[o2, o1])
vr.render("multiples.avi", duration_s=10, verbose=True)
```

Tips:
- Keep resolution/FPS moderate while this module is still being optimized.
- Minor seam/overdraw artifacts are known limitations at the moment.

## macOS GPU Note

GPU `RASTERIZE` mode needs GL 4.3 compute shaders, which are unavailable on native macOS drivers.

## VM Workaround for macOS

- [Install UTM](https://mac.getutm.app)
- [Download Ubuntu ISO](https://ubuntu.com/download/desktop)
- Create a Linux VM in UTM
- Install Python:

```bash
sudo apt update
sudo apt install python3.11
python3 --version
sudo apt install python3-pip
```

Then install the package inside the VM:

```bash
pip install aiden3drenderer
```

## Controls

### Camera Movement
- `W/A/S/D` - Move forward/left/backward/right
- `Space` - Move up
- `Left Shift` - Move down
- `Left Ctrl` - Speed boost (2x)
- Mouse wheel - Adjust camera FOV
- Arrow keys - Fine pitch/yaw adjustment
- Right mouse + drag - Look around

### Terrain Selection
- `1` - Mountain terrain
- `2` - Animated sine waves
- `3` - Ripple effect
- `4` - Canyon valley
- `5` - Stepped pyramid
- `6` - Spiral surface
- `7` - Torus
- `8` - Sphere
- `9` - Mobius strip
- `0` - Megacity
- `Q` - Alien landscape
- `E` - Double helix
- `R` - Mandelbulb slice
- `T` - Klein bottle
- `Y` - Trefoil knot

### Other
- `Escape` - Open/close pause menu in `run()` mode

## Terrain Descriptions

### Static Terrains

**Mountain** (`1`) - Smooth parabolic mountain with radial falloff.

**Canyon** (`4`) - U-shaped valley with sinusoidal variation.

**Pyramid** (`5`) - Stepped pyramid using Chebyshev distance.

**Torus** (`7`) - Classic donut shape from parametric equations.

**Sphere** (`8`) - UV sphere generated from spherical coordinates.

**Mobius Strip** (`9`) - Non-orientable surface with a single continuous side.

**Megacity** (`0`) - 80x80 procedural city (6400 vertices) with roads and building variation.

**Mandelbulb** (`R`) - 2D slice through a Mandelbulb-style fractal field.

**Klein Bottle** (`T`) - Non-orientable 4D-inspired surface projected into 3D.

**Trefoil Knot** (`Y`) - Tube mesh along a classic trefoil knot path.

### Animated Terrains

**Waves** (`2`) - Multi-frequency flowing sine surface.

**Ripple** (`3`) - Expanding circular wave with amplitude decay.

**Spiral** (`6`) - Rotating polar-coordinate surface animation.

**Alien Landscape** (`Q`) - Mixed procedural terrain with craters, spikes, and pulsation.

**Double Helix** (`E`) - Twin strand structure with phase offset and animation.

## Technical Details

### 3D Projection Pipeline
1. World coordinates
2. Camera translation
3. Camera rotation (yaw/pitch/roll)
4. Perspective projection with FOV
5. Screen-space mapping

### Rotation Equations

Yaw (Y-axis):
```text
x' = x*cos(theta) + z*sin(theta)
z' = -x*sin(theta) + z*cos(theta)
```

Pitch (X-axis):
```text
y' = y*cos(phi) - z*sin(phi)
z' = y*sin(phi) + z*cos(phi)
```

Roll (Z-axis):
```text
x' = x*cos(psi) - y*sin(psi)
y' = x*sin(psi) + y*cos(psi)
```

### Culling
Vertices behind the camera (`z <= 0.1`) are culled (`None`) to avoid invalid perspective division and visual artifacts.

## Performance Notes

- Most built-in terrains are intended to be playable in real-time.
- Large scenes (especially filled modes) are heavier; `MESH` mode is best for maximum speed.
- `Megacity` is one of the largest defaults and a good stress test.

## API Reference

### Renderer3D

```python
from aiden3drenderer import Renderer3D

renderer = Renderer3D(width=1200, height=800)
renderer.run()
```

Useful methods and attributes:
- `set_starting_shape(shape_name_or_none)`
- `set_use_default_shapes(bool)`
- `set_render_type(renderer_type.*)`
- `toggle_depth_view(bool)`
- `toggle_heat_map(bool)`
- `set_texture_for_raster(path)`
- `add_texture_for_raster(path)`
- `generate_cross_type_cubemap_skybox(radius, img_path)`
- `generate_cubemap_skybox(...)`
- `using_obj_filetype_format`
- `vertices_faces_list`
- `lighting_strictness`
 - `entities`: list of `Entity` objects attached to the scene (update them each frame or let your loop call them).
 - `CustomShader`: helper class (see `aiden3drenderer.custom_shader.CustomShader`) to run compute shaders and manage SSBO/uniform access.

### Camera

```python
from aiden3drenderer import Renderer3D

renderer = Renderer3D()
camera = renderer.camera

print(camera.position)   # [x, y, z]
print(camera.rotation)   # [pitch, yaw, roll]
print(camera.speed)
print(camera.base_speed)
```

### register_shape Decorator

```python
@register_shape(name, key=None, is_animated=False, color=None)
def generate_function(grid_size=40, frame=0):
    return matrix
```

Expected return type:
- `list[list[tuple[float, float, float] | None]]` (rectangular matrix)

## Package Structure

```text
aiden3drenderer/
|-- __init__.py
|-- renderer.py
|-- camera.py
|-- obj_loader.py
|-- physics.py
|-- shapes.py
`-- video_renderer.py

examples/
|-- basic_usage.py
|-- custom_shape_example.py
|-- obj_example.py
`-- physics_test.py
```

## Development

### Run from Source

```bash
git clone https://github.com/AidenKielby/3D-mesh-Renderer
cd 3D-mesh-Renderer
pip install -e .
python examples/basic_usage.py
```

### Build + Publish

```bash
pip install build twine
python -m build
python -m twine upload dist/*
```

## Credits

Created by Aiden.
Procedural terrain ideas were AI-assisted in places; core renderer/projection/camera and package engineering are authored manually.

## License

MIT
