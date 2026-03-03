"""
Aiden3DRenderer - A lightweight 3D wireframe renderer

Example usage:
    from aiden3drenderer import Renderer3D, register_shape
    
    renderer = Renderer3D()
    renderer.run()
"""

__version__ = "1.3.5"
__author__ = "Aiden"

from .renderer import Renderer3D, register_shape, renderer_type
from .camera import Camera
from . import physics
from . import obj_loader
from .video_renderer import VideoRenderer3D, VideoRendererObject

__all__ = [
    "Renderer3D",
    "register_shape",
    "renderer_type",
    "Camera",
    "physics",
    "obj_loader",
    "VideoRenderer3D",
    "VideoRendererObject",
]
