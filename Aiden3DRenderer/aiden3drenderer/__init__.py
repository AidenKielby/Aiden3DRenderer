"""
Aiden3DRenderer - A lightweight 3D wireframe renderer

Example usage:
    from aiden3drenderer import Renderer3D, register_shape
    
    renderer = Renderer3D()
    renderer.run()
"""

__version__ = "1.8.3"
__author__ = "Aiden"

from .renderer import Renderer3D, register_shape, renderer_type, object_type
from .camera import Camera
from . import physics
from . import obj_loader
from . import dae_loader
from .video_renderer import VideoRenderer3D, VideoRendererObject
from .button import Button
from .entity import Entity

__all__ = [
    "Renderer3D",
    "register_shape",
    "renderer_type",
    "object_type",
    "Camera",
    "physics",
    "obj_loader",
    "dae_loader",
    "VideoRenderer3D",
    "VideoRendererObject",
    "Button",
    "Entity",
]
