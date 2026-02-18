"""
Aiden3DRenderer - A lightweight 3D wireframe renderer

Example usage:
    from aiden3drenderer import Renderer3D, register_shape
    
    renderer = Renderer3D()
    renderer.run()
"""

__version__ = "0.1.3"
__author__ = "Aiden"

from .renderer import Renderer3D, register_shape
from .camera import Camera
from . import shapes

__all__ = [
    "Renderer3D",
    "register_shape",
    "Camera",
    "shapes",
]
