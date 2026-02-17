# Grid Topology Renderer

## Features

- **Custom 3D projection** - Perspective projection without using external 3D libraries
- **First-person camera** - Full 6-DOF camera movement with mouse look
- **15+ procedural generators** - Mountains, cities, fractals, and mathematical surfaces
- **Real-time rendering** - 60 FPS wireframe rendering
- **Animated terrains** - Several terrains feature time-based animations

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
  </table>
</div>


## Requirements

```bash
pip install pygame
```

Tested with Python 3.11.9 and Pygame 2.6.1

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

## Code Structure

- **Generation functions** (`generate_*`) - Procedural terrain generators
- **ddd_to_dd()** - 3D to 2D projection with camera transformations
- **render()** - Draw wireframe connections between grid points
- **Main loop** - Event handling, camera updates, frame rendering

## Credits

Procedural generation functions created with AI assistance. All rendering, projection, and camera code written manually.

## License

Free to use and modify.
