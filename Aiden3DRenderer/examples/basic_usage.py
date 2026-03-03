"""
Basic usage example for Aiden3DRenderer

This demonstrates the simplest way to use the renderer.
"""
from aiden3drenderer import Renderer3D, register_shape, renderer_type
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


@register_shape("hyperboloid_1sheet", pygame.K_z, is_animated=False, color=(120, 120, 120))
def hyperboloid_1sheet(
    resolution_u=48,
    resolution_v=28,
    a=1.0,
    b=1.0,
    c=1.25,
    v_min=-1.0,
    v_max=1.0,
):
    """Hyperboloid of one sheet: x^2/a^2 + y^2/b^2 - z^2/c^2 = 1"""
    grid = []

    for u_idx in range(resolution_u):
        row = []
        for v_idx in range(resolution_v):
            u = (u_idx / resolution_u) * 2 * math.pi
            v = v_min + (v_idx / max(1, resolution_v - 1)) * (v_max - v_min)

            cosh_v = math.cosh(v)
            sinh_v = math.sinh(v)

            x = a * cosh_v * math.cos(u)
            y = b * cosh_v * math.sin(u)
            z = c * sinh_v

            row.append((x * 4 + 15, z * 4 + 10, y * 4 + 15))
        grid.append(row)

    return grid

def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = "waves"

    renderer.camera.position = [0, 0 ,0]
    renderer.render_type = renderer_type.MESH
    # Run the renderer

    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()
