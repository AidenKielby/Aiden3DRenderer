# Custom Shader

`CustomShader` is a lightweight helper for working with GLSL compute shaders using ModernGL. It extracts buffer and uniform declarations from the provided shader source, creates a `moderngl` compute shader, and exposes helpers for allocating SSBO-like buffers and uploading/downloading data.

Constructor
-----------

`CustomShader(shader_code: str, context = None)`

- `shader_code` — GLSL compute shader source (string). The code should contain `layout(..., binding = N)` annotations for `buffer` and `uniform` declarations to allow `get_buffers()` and `get_uniforms()` to infer bindings.
- `context` — optional `moderngl.Context`; if omitted a standalone ModernGL context is created.

Primary methods
---------------

`get_buffers() -> list`
	- Parses the GLSL source and returns a list of buffer descriptors discovered in the shader. Each descriptor is `[buffer_name, var_type, var_name, is_list, binding]`.

`get_uniforms() -> list`
	- Returns a list of uniform declarations discovered in the shader as `[type_name, var_name, binding]`.

`set_buffer(buffer_name: str, element_count: int, element_size: Optional[int] = None) -> None`
	- Allocate a GL storage buffer for the named buffer. If `element_size` is not provided the helper uses a conservative size lookup for GLSL types (`float`, `vec2`, `vec3`, `vec4`).
	- Raises `NameError` if the named buffer isn't present in the shader.

`write_to_buffer(buffer_name: str, data_bytes: bytes) -> None`
	- Write raw bytes into an allocated buffer. Raises `NameError` if the buffer hasn't been allocated.

`read_from_buffer(buffer_name: str, num_elements: int, element_type: str = 'vec3') -> numpy.ndarray`
	- Read back a buffer and reshape it into a NumPy array of shape `(num_elements, stride)`. `element_type` controls stride interpretation. Raises `NameError` if buffer is not allocated.

`add_texture(texture_path: str, location: int, texture_name: str) -> moderngl.Texture`
	- Load an image with `PIL.Image` and create a GL texture bound to `location`. The method updates shader uniforms to point to the texture unit and returns the `Texture` object.
	- Raises `FileNotFoundError` if the image path isn't found.

`write_to_uniform(uniform_name: str, data_bytes) -> None`
	- Assign a value to a shader uniform by name. Raises `NameError` if the uniform isn't present in the shader source.

Implementation notes and caveats
--------------------------------

- The GLSL parser is intentionally simple and uses regex-based heuristics. It works reliably for common layout/uniform declarations but may fail on complex or multi-line declarations.
- `vec3` is padded to 16 bytes in the helper's `glsl_type_to_bytes` table to match `std430` alignment used by SSBOs in GLSL.
- The helper does not implement a full reflection API — it is a convenience wrapper appropriate for the compute shaders included in the package.

Example (allocate an SSBO)
--------------------------

```python
from aiden3drenderer import CustomShader
shader_src = open('my_compute.glsl').read()
cs = CustomShader(shader_src)
cs.set_buffer('triangle_data', element_count=10000, element_size=80)
# write bytes: cs.write_to_buffer('triangle_data', data_bytes)
```

See also: [Renderer](renderer.md) where a built-in compute shader is used for the rasterizer.
