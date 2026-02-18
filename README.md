# Aiden3DRenderer

A lightweight 3D wireframe renderer built with Pygame featuring custom projection, first-person camera controls, and 15+ procedural terrain generators.

## Features

- **Custom 3D projection** - Perspective projection without using external 3D libraries
- **First-person camera** - Full 6-DOF camera movement with mouse look
- **15+ procedural generators** - Mountains, cities, fractals, and mathematical surfaces
- **Real-time rendering** - 60 FPS wireframe rendering
- **Animated terrains** - Several terrains feature time-based animations
- **Extensible API** - Easy to create and register custom shapes with decorators

## Gallery

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="media/RenderShowcase.gif" alt="Ripple Animation" width="400"/>
        <br/>
        <b>Ripple Effect</b>
        <br/>
        <i>Expanding waves from center</i>
      </td>
      <td align="center">
        <img src="media/plateau_thing.png" alt="Mandelbulb Fractal" width="400"/>
        <br/>
        <b>Mandelbulb Slice</b>
        <br/>
        <i>3D fractal cross-section</i>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="media/Spiral.gif" alt="Turning Spiral" width="400"/>
        <br/>
        <b>Turning Spiral</b>
        <br/>
        <i>Screw like shape spinning</i>
      </td>
      <td align="center">
        <img src="media/City.png" alt="Simple City (laggy when solid render)" width="400"/>
        <br/>
        <b>Simple City (laggy when solid render)</b>
        <br/>
        <i>City preset in solid render</i>
      </td>
    </tr>
  </table>
</div>

## Installation

```bash
pip install aiden3drenderer
```

Requires Python 3.11+ and automatically installs Pygame 2.6.0+

## Quick Start

### Running the Demo

```python
from aiden3drenderer import Renderer3D

# Create and run the renderer with all built-in shapes
renderer = Renderer3D()
renderer.run()
```

### Creating Custom Shapes

```python
from aiden3drenderer import Renderer3D, register_shape
import pygame

# Register a custom shape with a decorator
@register_shape("My Pyramid", key=pygame.K_p, is_animated=False)
def generate_pyramid(grid_size=40, frame=0):
    """Generate a simple pyramid."""
    matrix = []
    center = grid_size / 2
    
    for x in range(grid_size):
        row = []
        for y in range(grid_size):
            # Distance from center
            dx = abs(x - center)
            dy = abs(y - center)
            max_dist = max(dx, dy)
            
            # Height decreases with distance
            height = max(0, 10 - max_dist)
            row.append(height)
        matrix.append(row)
    
    return matrix

# Run the renderer (your shape will be available on 'P' key)
renderer = Renderer3D()
renderer.run()
```

## Controls

### Camera Movement
- **W/A/S/D** - Move forward/left/backward/right
- **Space** - Move up
- **Left Shift** - Move down
- **Left Ctrl** - Speed boost (2x)
- **Arrow Keys** - Fine pitch/yaw adjustment
- **Right Mouse + Drag** - Look around (pitch and yaw)

### Terrain Selection
- **1** - Mountain terrain
- **2** - Animated sine waves
- **3** - Ripple effect
- **4** - Canyon valley
- **5** - Stepped pyramid
- **6** - Spiral surface
- **7** - Torus (donut)
- **8** - Sphere
- **9** - Möbius strip
- **0** - Megacity (80×80 procedural city)
- **Q** - Alien landscape
- **E** - Double helix (DNA-like)
- **R** - Mandelbulb fractal slice
- **T** - Klein bottle
- **Y** - Trefoil knot

### Other
- **Escape** - Quit application

## Terrain Descriptions

### Static Terrains

**Mountain** (1) - Smooth parabolic mountain with radial falloff

**Canyon** (4) - U-shaped valley with sinusoidal variations

**Pyramid** (5) - Stepped pyramid using Chebyshev distance

**Torus** (7) - Classic donut shape using parametric equations

**Sphere** (8) - UV sphere using spherical coordinates

**Möbius Strip** (9) - Non-orientable surface with a single side

**Megacity** (0) - 80×80 grid with hundreds of procedurally generated buildings
- Buildings get taller toward the center
- 8×8 block system with roads
- Random antenna towers on some buildings
- Most complex terrain (6400 vertices)

**Mandelbulb** (R) - 2D slice of 3D Mandelbulb fractal
- Uses power-8 formula
- Height based on iteration count

**Klein Bottle** (T) - 4D object projected into 3D
- Non-orientable surface
- No inside or outside

**Trefoil Knot** (Y) - Mathematical knot in 3D space
- Classic topology example
- Tube follows trefoil path

### Animated Terrains

**Waves** (2) - Multiple overlapping sine waves
- Three different wave frequencies
- Constantly flowing motion

**Ripple** (3) - Expanding ripple from center
- Exponential amplitude decay
- Simulates water drop impact

**Spiral** (6) - Rotating spiral pattern
- Polar coordinate mathematics
- Hypnotic rotation

**Alien Landscape** (Q) - Complex multi-feature terrain
- Crater with parabolic profile  
- Crystalline spike formations
- Rolling hills
- Procedural "vegetation" spikes
- Pulsating energy field

**Double Helix** (E) - DNA-like structure
- Two intertwined strands
- 180° phase offset between strands
- Rotates over time

## Technical Details

### 3D Projection Pipeline

1. **World coordinates** - Raw vertex positions
2. **Camera translation** - Subtract camera position
3. **Camera rotation** - Apply yaw, pitch, roll transformations
4. **Perspective projection** - Divide by Z-depth with FOV
5. **Screen mapping** - Convert to pixel coordinates

### Rotation Matrices

Yaw (Y-axis):
```
x' = x·cos(θ) + z·sin(θ)
z' = -x·sin(θ) + z·cos(θ)
```

Pitch (X-axis):
```
y' = y·cos(φ) - z·sin(φ)
z' = y·sin(φ) + z·cos(φ)
```

Roll (Z-axis):
```
x' = x·cos(ψ) - y·sin(ψ)
y' = x·sin(ψ) + y·cos(ψ)
```

### Culling

Points behind the camera (z ≤ 0.1) are set to `None` to prevent rendering artifacts and negative depth division.

## Performance

- **60 FPS** stable on most terrains
- **Megacity** (6400 vertices) - Largest terrain, still maintains 60 FPS
- Wireframe rendering only - no filled polygons for performance

## API Reference

### Renderer3D

Main renderer class that handles the 3D projection and rendering loop.

```python
from aiden3drenderer import Renderer3D

renderer = Renderer3D(
    width=1200,      # Window width in pixels
    height=800,      # Window height in pixels
    fov=800          # Field of view (higher = less perspective)
)
renderer.run()
```

### Camera

Camera class for position and rotation control (automatically created by Renderer3D).

```python
from aiden3drenderer import Camera

# Access camera through renderer
renderer = Renderer3D()
camera = renderer.cam

# Camera attributes
camera.pos          # [x, y, z] position
camera.facing       # [yaw, pitch, roll] in radians
camera.speed        # Movement speed (default: 0.5)
```

### register_shape Decorator

Register custom shape generators that appear in the renderer.

```python
@register_shape(name, key=None, is_animated=False)
def generate_function(grid_size=40, frame=0):
    """
    Args:
        name (str): Display name for the shape
        key (pygame.K_*): Keyboard key to trigger shape (optional)
        is_animated (bool): Whether shape changes over time
        
    Returns:
        list[list[float]]: grid_size x grid_size matrix of heights
    """
    return matrix
```

## Package Structure

```
aiden3drenderer/
├── __init__.py          # Package exports
├── renderer.py          # Renderer3D class and projection
├── camera.py            # Camera class for movement/rotation
└── shapes.py            # 15+ built-in shape generators

examples/
├── basic_usage.py       # Simple demo
└── custom_shape_example.py  # Custom shape tutorial
```

## Development

### Running from Source

```bash
git clone https://github.com/yourusername/aiden3drenderer.git
cd aiden3drenderer
pip install -e .
python examples/basic_usage.py
```

### Building the Package

```bash
pip install build twine
python -m build
python -m twine upload dist/*
```

## Credits

Created by Aiden. Procedural generation functions created with AI assistance. All rendering, projection, and camera code written manually.

## License

Free to use and modify.
