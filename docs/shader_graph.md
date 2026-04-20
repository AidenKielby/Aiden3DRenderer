# Shader Graph

The `aiden3drenderer.ShaderGraph` package provides a DearPyGui node editor that generates GLSL source strings and can export them into Python files.

This page covers all currently shipped ShaderGraph source files:

- `ShaderGraph/__init__.py`
- `ShaderGraph/shader_type.py`
- `ShaderGraph/shader_target.py`
- `ShaderGraph/element.py`
- `ShaderGraph/elements.py`
- `ShaderGraph/gui.py`

## Public entrypoint

The package exposes a console script:

- `shader-graph` -> `aiden3drenderer.ShaderGraph.gui:run`

`run()` behavior:

- Imports DearPyGui (`dearpygui.dearpygui`) at module import time.
- Raises `RuntimeError` with install guidance when DearPyGui is unavailable.
- Builds the node editor UI and starts the DearPyGui render loop.

## Core data model

### ShaderType (`shader_type.py`)

Enum of shader value kinds used by ports and node typing:

- Scalars: `float`, `int`, `bool`
- Vectors: `vec2`, `vec3`, `vec4`
- Matrices: `mat2`, `mat3`, `mat4`
- Texture: `sampler2D`
- Wildcard: `any`

`ShaderType.from_str(label: str) -> ShaderType`

- Converts string labels to enum values.
- Raises `ValueError` for unknown labels.

### ShaderTarget (`shader_target.py`)

Container for target-specific GLSL generation strategy.

Constructor fields:

- `name`: target identifier (`compute_glsl`, `fragment_glsl`, `vertex_glsl`)
- `header`: GLSL version/header block
- `globals_block`: top-level declarations
- `main_wrapper`: callable that wraps node body text into a full shader
- `entry_inputs`: optional list of required graph inputs
- `restricted_elements`: names that are blocked from body emission

Caveat:

- `restricted_elements` has a mutable default (`[]`) in constructor signature. Reusing defaults across instances can cause shared-state surprises.

### Element and ElementType (`element.py`)

`ElementType` classifies node behavior:

- `FUNCTION`
- `UNIFORM_LAYOUT`
- `MAIN_FUNCTION_EXECUTABLE`
- `OUTPUT_ONLY`
- `USER_DEFINED`

`Element` is the node payload used by UI and shader serialization.

Fields:

- `name`: display and logical name
- `inputs`: list of `ShaderType`
- `outputs`: list of `ShaderType`
- `variable_name`: generated variable stem
- `function`: GLSL snippet template
- `type`: `ElementType`
- `category`: sidebar grouping

### Built-in element library (`elements.py`)

Defines prebuilt `Element` instances used by the GUI catalog. Categories include:

- Uniform/IO nodes (`srcTex`, `imageStore`, coordinates)
- Math and comparison nodes (`add`, `subtract`, `multiply`, `divide`, `lessThan`, `greaterThan`)
- Vector nodes (`dot`, `cross`, `normalize`, length)
- Texture nodes (`sampleTex`, `getPixelAt`, `texSize`)
- Conversion utilities (`to_vec_*`, `from_vec_*`, scalar casts)

## Graph compilation flow (`gui.py`)

Main pipeline:

1. Node graph is edited in DearPyGui and connections are tracked globally.
2. `get_correct_ordering()` performs backward traversal from output nodes to derive execution order.
3. `graph_to_shader(target)` emits target-specific shader code:
   - header
   - global declarations
   - generated `main` body wrapped by target wrapper
4. `export_shader()` writes or updates a triple-quoted shader variable inside a Python file.

Target presets:

- `compute_glsl`: includes `destTex` image output and `srcTex` sampler input.
- `fragment_glsl`: emits `FragColor` fragment shader output.
- `vertex_glsl`: emits `gl_Position` output using `MVP` and `aPos`.

## Failure states and risks

- Missing dependency: DearPyGui not installed -> `RuntimeError` from `run()`.
- File export errors (`export_shader`): bad path or permissions -> `FileNotFoundError`, `PermissionError`, or `OSError`.
- Source rewrite behavior uses regex matching to replace existing shader variables in a target file; malformed surrounding code or non-standard assignment forms may prevent replacement and trigger insertion instead.
- Type compatibility checks are permissive with `ShaderType.ANY`; incorrect runtime GLSL typing can still compile-fail later.
- Global mutable state (`changes`, `connections`, `link_map`, `taken_variable_names`) persists for the life of the GUI session.

## Performance context

- Graph ordering is linear in nodes plus edges, approximately O(V + E).
- Export string generation is lightweight relative to UI rendering.
- Runtime cost is dominated by DearPyGui drawing and interactive node graph manipulation, not shader text assembly.

## Practical usage

Run from an environment with shadergraph extras installed:

```bash
shader-graph
```

Or call directly from Python:

```python
from aiden3drenderer.ShaderGraph.gui import run

run()
```

If dependency installation is needed:

```bash
pip install "aiden3drenderer[shadergraph]"
```
