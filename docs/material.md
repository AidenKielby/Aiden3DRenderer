# Material

Purpose
-------

`Material` is a lightweight container for texture/material properties and a parser for the package's simple `.mat` text format. It is exported at package level (`from aiden3drenderer import Material`).

Why this class exists
---------------------

The renderer and model-loading flow primarily use tuple/list-based geometry structures. `Material` provides a structured object for storing texture path, color, transparency, and alpha metadata that can be attached to higher-level loading pipelines.

Class: Material
---------------

Constructor
    Material(
        name: str,
        texture_path: str,
        texture_index: int,
        base_color: tuple[float] = (155, 0, 0),
        transparent: bool = False,
        alpha: float = 1.0,
    )

Constructor behavior
    - Stores provided fields directly.
    - Writes the transparency flag to `self.is_trasparent` (spelling preserved from source).

Public fields after construction
    - `name` (str)
    - `texture_path` (str)
    - `texture_index` (int)
    - `base_color` (tuple[float])
    - `is_trasparent` (bool)
    - `alpha` (float)

Method: get_material_from_file(file_path: str)
-----------------------------------------------

Parses a `.mat` file and mutates the current `Material` instance.

Expected format (inferred from parser)
    - First line: material name in quotes or plain text.
    - Subsequent lines: `key=value` entries.
    - Supported keys: `TexturePath`, `BaseColor`, `Transparent`, `Alpha`.

Signature
    get_material_from_file(file_path: str) -> None

Exceptions (traced from source)
    - `SyntaxError`: raised when `file_path` does not end with `.mat`.
    - `FileNotFoundError`: raised by `open(file_path, "r")` if file is missing.
    - `ValueError`: possible when parsing `BaseColor` values as integers or `Alpha` as int.

Implementation caveats (important)
----------------------------------

- `Transparent` parsing uses `bool(string_value)`, which means non-empty strings such as `"False"` evaluate to `True` in Python.
- The constructor stores transparency in `is_trasparent`, while file parsing assigns to `self.transparent`; both attributes may exist on one instance.
- `Alpha` is parsed as `int` in file loading even though constructor type hint uses `float`.

Real-world usage
----------------

```python
from aiden3drenderer import Material

mat = Material(
    name="default",
    texture_path="./assets/cup.png",
    texture_index=0,
    base_color=(255, 255, 255),
    transparent=False,
    alpha=1.0,
)

mat.get_material_from_file("./assets/example.mat")
print(mat.name, mat.texture_path, mat.base_color, mat.alpha)
```

Related pages
-------------

- [Renderer](renderer.md)
- [OBJ Loader](obj_loader.md)
- [Audit Report](audit_report.md)
