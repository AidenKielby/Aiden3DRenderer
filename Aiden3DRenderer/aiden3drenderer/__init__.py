"""
Aiden3DRenderer - A lightweight 3D wireframe renderer

Example usage:
    from aiden3drenderer import Renderer3D, register_shape
    
    renderer = Renderer3D()
    renderer.run()
"""

__version__ = "1.2.1"
__author__ = "Aiden"

from .renderer import Renderer3D, register_shape
from .camera import Camera
from . import shapes
from . import physics
from  . import obj_loader

__all__ = [
    "Renderer3D",
    "register_shape",
    "Camera",
    "shapes",
    "physics",
    "obj_loader",
]
