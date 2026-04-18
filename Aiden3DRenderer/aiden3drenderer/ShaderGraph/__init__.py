"""Demo subpackage for aiden3drenderer.

This makes `aiden3drenderer.Demo` a proper package and re-exports the demo() function.
"""

from .gui import run

__all__ = ["run"]
