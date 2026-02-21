"""
Basic usage example for Aiden3DRenderer

This demonstrates the simplest way to use the renderer.
"""
from aiden3drenderer import Renderer3D, register_shape
import pygame
import math

@register_shape("flower", pygame.K_1, is_animated=False, color=(100, 100, 100))
def flower(resolution=30):
    """Flower-shaped 3D surface"""
    grid = []
    
    for u_idx in range(resolution):
        row = []
        for v_idx in range(resolution):
            u = (u_idx / resolution) * 2 * math.pi
            v = (v_idx / resolution) * math.pi - math.pi / 2
            
            # Flower petal equations
            r = 2 + math.sin(5 * u)  # 5 petals
            
            x = r * math.cos(v) * math.cos(u)
            y = r * math.cos(v) * math.sin(u)
            z = r * math.sin(v)
            
            row.append((x * 5 + 15, z * 5 + 10, y * 5 + 15))
        grid.append(row)
    
    return grid

def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = "waves"

    renderer.camera.position = [0, 0 ,0]
    renderer.is_mesh = False
    # Run the renderer

    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()
