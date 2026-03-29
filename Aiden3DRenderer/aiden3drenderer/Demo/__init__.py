"""Demo subpackage for aiden3drenderer.

This makes `aiden3drenderer.Demo` a proper package and re-exports the demo() function.
"""

from .silly_skull import demo, demo_inv

__all__ = ["demo", "demo_inv"]
