# Math Shape

Equation-driven shape registration helper for procedural math surfaces.

This module adds a high-level utility class, MathShape, that turns a math expression string into a renderer shape registered through register_shape.

## Class: MathShape

Constructor signature:

    MathShape(
        name: str,
        pygame_key: int,
        function: str,
        color: tuple[int, int, int] = (100, 20, 200),
        grid_size: int = 20,
        y_range=(-10, 10),
        y_resolution=0.2,
        centered=True,
        is_animated=False,
    )

### Constructor behavior

- Stores configuration on the instance.
- Immediately calls register_self(), which registers a new shape in the global renderer shape registry.

This means object construction has a global side effect: it mutates CUSTOM_SHAPES via register_shape.

## Methods

### register_self

Signature:

    register_self(self)

Behavior:

- Defines an inner shape function with defaults captured from the instance.
- Decorates that function with register_shape(self.name, self.key, self.is_animated, self.color).
- The registered shape function calls generate_shape_from_equation(...).

Important note:

- If another shape with the same name is registered later, it will overwrite the previous entry in the global shape registry.

### generate_shape_from_equation

Signature:

    generate_shape_from_equation(
        self,
        equation: str,
        grid_size=30,
        y_range=(-10, 10),
        y_resolution=0.2,
        time=0,
        centered=True,
    )

Behavior:

- Builds a math evaluation environment from Python math module symbols plus abs, max, min, pow.
- Iterates over grid_size x grid_size points in x/z.
- Supports two evaluation modes:
  - Explicit mode: equation does not contain y, or contains =. Evaluates once per x/z to compute y.
  - Implicit scan mode: equation contains y and does not contain =. Scans y_range at y_resolution to find y minimizing abs(equation).
- Returns a grid list of (x, y, z) tuples, compatible with renderer shape workflow.

Implicit mode details:

- steps = int((y_max - y_min) / y_resolution)
- First near-zero break threshold is abs(value) < 0.01
- If no best y is found, falls back to y = 0

## Failure states and exceptions

The module does not wrap exceptions from eval or parameter math. Typical failure modes:

- SyntaxError, NameError, TypeError, ZeroDivisionError from equation evaluation.
- ZeroDivisionError when y_resolution is 0 in implicit mode.
- TypeError or ValueError if y_range or numeric parameters are malformed.

Security warning:

- Equations are executed with eval. Never pass untrusted equation strings.

## Performance context

- Explicit mode runtime: O(grid_size^2)
- Implicit mode runtime: O(grid_size^2 * steps), where steps is roughly (y_max - y_min) / y_resolution
- Memory usage: O(grid_size^2) for returned grid coordinates

For dense implicit surfaces, runtime can grow quickly. Increase y_resolution or reduce grid_size to stabilize frame generation cost.

## Real-world usage

Animated explicit wave surface:

```python
import pygame
from aiden3drenderer import Renderer3D, MathShape

MathShape(
    name="psy_waves",
    pygame_key=pygame.K_f,
    function="sin(x*0.4 + t)*2 + cos(z*0.4 + t)*2 + sin((x+z)*0.2 + t)*1.5",
    color=(120, 220, 255),
    grid_size=40,
    centered=True,
    is_animated=True,
)

renderer = Renderer3D(width=1000, height=700)
renderer.set_starting_shape("psy_waves")
renderer.run()
```

Implicit surface example (equation uses y and no equals sign):

```python
import pygame
from aiden3drenderer import Renderer3D, MathShape

MathShape(
    name="sphere_implicit",
    pygame_key=pygame.K_i,
    function="x*x + y*y + z*z - 25",
    color=(255, 180, 120),
    grid_size=36,
    y_range=(-8, 8),
    y_resolution=0.1,
)

renderer = Renderer3D(width=1000, height=700)
renderer.set_starting_shape("sphere_implicit")
renderer.run()
```

## Cross references

- [Renderer](renderer.md)
- [Shapes](shapes.md)
- [Tutorials](tutorials.md)
- [Audit Report](audit_report.md)
