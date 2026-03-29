# Custom Shaders

`CustomShader` is a lightweight helper for working with ModernGL compute shaders and storage buffers (SSBO-like usage). It is designed for advanced users who need custom GPU work (e.g., rasterization compute paths, physics offload, or GPGPU experiments).

Overview
- Parses GLSL compute shader source to discover `buffer` and `uniform` declarations (simple heuristic parser).
- Wraps a ModernGL `compute_shader` object and exposes helpers to allocate buffers, write/read data, and set uniforms.

Important: `moderngl` and OpenGL 4.3+ are required for compute shaders. On macOS native drivers, compute shader support is limited; use non-GPU paths there.

Key API
- `CustomShader(shader_code: str, context=None)` — create helper; if `context` is omitted it constructs a standalone context.
- `set_buffer(buffer_name: str, element_count, element_size: int = None)` — allocates a storage buffer bound to the layout binding discovered in the shader. If `element_size` is omitted, the helper infers a fallback size from common GLSL types.
- `write_to_buffer(buffer_name: str, data_bytes)` — writes raw bytes into the allocated buffer (use `numpy.tobytes()` to convert arrays).
- `write_to_uniform(uniform_name: str, data_bytes)` — write a uniform value on the compute shader.
- `read_from_buffer(buffer_name: str, num_elements, element_type='vec3')` — returns a NumPy array of the requested element type read from the buffer.

Supported/assumed types
- The parser recognizes basic GLSL types (`float`, `vec2`, `vec3`, `vec4`) and uses a small mapping to compute byte sizes for allocations. For complex or custom structs prefer manual buffer sizing via `element_size`.

Example: basic workflow

```python
from aiden3drenderer.custom_shader import CustomShader
import numpy as np

shader_src = """
#version 430
layout(std430, binding = 0) buffer dataBuf { vec4 items[]; };
layout(local_size_x = 64) in;
void main(){ uint i = gl_GlobalInvocationID.x; items[i] = vec4(i);
}
"""

cs = CustomShader(shader_src, context=renderer.ctx)
cs.set_buffer('dataBuf', element_count=1024, element_size=16)
arr = np.arange(1024, dtype='f4').reshape(-1,1)
cs.write_to_buffer('dataBuf', arr.tobytes())
# dispatch the compute shader directly
cs.compute_shader.run(group_x=16)
res = cs.read_from_buffer('dataBuf', 1024, element_type='vec4')
```

Notes & caveats
- The internal GLSL parser is simple and sometimes fragile; prefer explicit `element_size` sizes when in doubt.
- `read_from_buffer` uses `numpy.frombuffer(..., dtype='f4')` to interpret buffer contents — ensure your data layout matches.
- The helper binds buffers by the `binding` layout qualifier found in the shader; make sure your shader uses explicit bindings.
