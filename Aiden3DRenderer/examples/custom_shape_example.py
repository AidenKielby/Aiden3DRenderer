"""
Custom shape example for Aiden3DRenderer

This shows how to create your own custom 3D shapes.
"""
import math
import pygame
from aiden3drenderer import Renderer3D, register_shape


# Create a custom animated wave shape
@register_shape("my_custom_wave", pygame.K_c, is_animated=True)
def my_wave(size=30, time=0):
    """Custom wave pattern that pulses and rotates"""
    grid = []
    for x in range(size):
        row = []
        for z in range(size):
            # Create a radial pattern
            center = size / 2
            dx = x - center
            dz = z - center
            dist = math.sqrt(dx**2 + dz**2)
            
            # Combine circular waves with linear progression
            y = math.sin(dist * 0.5 - time * 2) * 3
            y += math.cos(x * 0.3 + time) * math.sin(z * 0.3 + time) * 2
            
            row.append((x, y, z))
        grid.append(row)
    return grid


# Create a custom static shape - a flower
@register_shape("flower", pygame.K_f, is_animated=False)
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
    # Create renderer
    renderer = Renderer3D(title="Custom Shapes Demo")
    
    # Start with our custom wave
    renderer.current_shape = "my_custom_wave"
    
    print("Controls:")
    print("1-9, 0: Built-in shapes")
    print("F: Flower shape")
    print("C: Custom wave")
    print("")
    print("WASD: Move, Space/Shift: Up/Down")
    print("Right mouse drag: Look around")
    
    # Run
    renderer.run()


if __name__ == "__main__":
    main()
