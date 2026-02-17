"""
Built-in 3D shapes for Aiden3DRenderer
"""
import math
import random
import pygame
from .renderer import register_shape


@register_shape("mountain", pygame.K_1, is_animated=False)
def generate_mountain(grid_size=20):
    """Generate a mountain terrain"""
    gridCoords = []
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            center_x = grid_size / 2
            center_z = grid_size / 2
            dist = math.sqrt((x - center_x)**2 + (z - center_z)**2)
            
            max_height = 8
            mountain_radius = grid_size / 3
            if dist < mountain_radius:
                y = max_height * (1 - (dist / mountain_radius)**2)
            else:
                y = 0
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("waves", pygame.K_2, is_animated=True)
def generate_waves(grid_size=30, time=0):
    """Generate animated sine wave terrain"""
    gridCoords = []
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Multiple sine waves for interesting patterns
            y = math.sin(x * 0.5 + time) * 2
            y += math.cos(z * 0.5 + time) * 2
            y += math.sin((x + z) * 0.3 + time * 0.5) * 1.5
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("ripple", pygame.K_3, is_animated=True)
def generate_ripple(grid_size=25, time=0):
    """Generate ripple effect from center"""
    gridCoords = []
    center_x = grid_size / 2
    center_z = grid_size / 2
    
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            dist = math.sqrt((x - center_x)**2 + (z - center_z)**2)
            y = math.sin(dist - time * 3) * 3 * math.exp(-dist / 10)
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("canyon", pygame.K_4, is_animated=False)
def generate_canyon(grid_size=30):
    """Generate a canyon/valley terrain"""
    gridCoords = []
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Create valley in the middle
            center_x = grid_size / 2
            dist_from_center_x = abs(x - center_x)
            
            # U-shaped valley
            y = -((dist_from_center_x / 5) ** 2) + 5
            
            # Add some noise
            y += math.sin(z * 0.5) * 0.5
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("pyramid", pygame.K_5, is_animated=False)
def generate_pyramid(grid_size=15):
    """Generate a stepped pyramid"""
    gridCoords = []
    center = grid_size / 2
    
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Distance from center (chebyshev distance for square pyramid)
            dist = max(abs(x - center), abs(z - center))
            
            # Step height based on distance
            y = max(0, (grid_size / 2) - dist)
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("spiral", pygame.K_6, is_animated=True)
def generate_spiral(grid_size=25, time=0):
    """Generate a spiral shape"""
    gridCoords = []
    center_x = grid_size / 2
    center_z = grid_size / 2
    
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            dx = x - center_x
            dz = z - center_z
            
            # Convert to polar coordinates
            angle = math.atan2(dz, dx)
            dist = math.sqrt(dx**2 + dz**2)
            
            # Spiral formula
            y = math.sin(angle * 3 + dist * 0.5 + time) * 3
            
            row.append((x, y, z))
        gridCoords.append(row)
    return gridCoords


@register_shape("torus", pygame.K_7, is_animated=False)
def generate_torus(resolution=30):
    """Generate a 3D torus (donut shape)"""
    gridCoords = []
    R = 5  # Major radius
    r = 2  # Minor radius
    
    for u_idx in range(resolution):
        row = []
        for v_idx in range(resolution):
            u = (u_idx / resolution) * 2 * math.pi
            v = (v_idx / resolution) * 2 * math.pi
            
            x = (R + r * math.cos(v)) * math.cos(u)
            y = r * math.sin(v)
            z = (R + r * math.cos(v)) * math.sin(u)
            
            row.append((x + 15, y + 5, z + 15))
        gridCoords.append(row)
    return gridCoords


@register_shape("sphere", pygame.K_8, is_animated=False)
def generate_sphere(resolution=20):
    """Generate a sphere"""
    gridCoords = []
    radius = 5
    
    for theta_idx in range(resolution):
        row = []
        for phi_idx in range(resolution):
            theta = (theta_idx / resolution) * math.pi
            phi = (phi_idx / resolution) * 2 * math.pi
            
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.cos(theta)
            z = radius * math.sin(theta) * math.sin(phi)
            
            row.append((x + 10, y + 5, z + 10))
        gridCoords.append(row)
    return gridCoords


@register_shape("mobius", pygame.K_9, is_animated=False)
def generate_mobius_strip(resolution=30):
    """Generate a Möbius strip"""
    gridCoords = []
    
    for u_idx in range(resolution):
        row = []
        for v_idx in range(resolution):
            u = (u_idx / resolution) * 2 * math.pi
            v = (v_idx / resolution - 0.5) * 2  # -1 to 1
            
            # Möbius strip parametric equations
            x = (2 + v * math.cos(u / 2)) * math.cos(u)
            y = v * math.sin(u / 2)
            z = (2 + v * math.cos(u / 2)) * math.sin(u)
            
            row.append((x + 15, y + 5, z + 15))
        gridCoords.append(row)
    return gridCoords


@register_shape("megacity", pygame.K_0, is_animated=False)
def generate_megacity(grid_size=80):
    """Generate a massive futuristic city with procedural buildings"""
    gridCoords = []
    random.seed(42)  # Consistent generation
    
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Create city blocks
            block_x = x // 8
            block_z = z // 8
            in_block_x = x % 8
            in_block_z = z % 8
            
            # Roads (empty spaces between blocks)
            is_road = (in_block_x == 0 or in_block_x == 7 or in_block_z == 0 or in_block_z == 7)
            
            if is_road:
                y = 0
            else:
                # Generate building heights with variation
                building_seed = block_x * 1000 + block_z
                random.seed(building_seed)
                
                # Distance from center affects building height
                center = grid_size / 2
                dist_from_center = math.sqrt((x - center)**2 + (z - center)**2)
                center_factor = max(0, 1 - dist_from_center / (grid_size / 2))
                
                # Random building height (taller in center)
                base_height = random.random() * 25 * center_factor + 3
                
                # Add some variation within the building
                variation = math.sin(in_block_x * 2) * math.cos(in_block_z * 2) * 0.5
                
                # Some buildings have antennas
                if random.random() > 0.7 and in_block_x == 3 and in_block_z == 3:
                    y = base_height + 5
                else:
                    y = base_height + variation
            
            row.append((x, y, z))
        gridCoords.append(row)
    
    random.seed()  # Reset random seed
    return gridCoords


@register_shape("alien", pygame.K_q, is_animated=True)
def generate_alien_landscape(grid_size=60, time=0):
    """Generate an otherworldly alien landscape with multiple features"""
    gridCoords = []
    
    for x in range(grid_size):
        row = []
        for z in range(grid_size):
            # Multiple overlapping features
            center_x = grid_size / 2
            center_z = grid_size / 2
            
            # Feature 1: Large crater
            crater_dist = math.sqrt((x - center_x)**2 + (z - center_z)**2)
            crater = 0
            if crater_dist < 20:
                crater = -(crater_dist - 20)**2 / 40 + 10
            
            # Feature 2: Crystalline spikes
            spike_pattern = abs(math.sin(x * 0.8) * math.cos(z * 0.8))
            spikes = spike_pattern ** 3 * 15
            
            # Feature 3: Rolling hills
            hills = math.sin(x * 0.3) * 3 + math.cos(z * 0.4) * 2.5
            
            # Feature 4: Alien vegetation (thin tall structures)
            veg_noise = (math.sin(x * 2.3 + z * 1.7) + 1) / 2
            if veg_noise > 0.85:
                vegetation = (veg_noise - 0.85) * 40
            else:
                vegetation = 0
            
            # Feature 5: Pulsating energy field
            pulse_dist = math.sqrt((x - center_x + 15)**2 + (z - center_z + 15)**2)
            pulse = math.sin(pulse_dist * 0.5 - time * 2) * 2 * math.exp(-pulse_dist / 20)
            
            # Combine all features
            y = crater + spikes * 0.3 + hills + vegetation + pulse
            
            row.append((x, y, z))
        gridCoords.append(row)
    
    return gridCoords


@register_shape("helix", pygame.K_e, is_animated=True)
def generate_double_helix(length=60, time=0):
    """Generate a DNA-like double helix structure"""
    gridCoords = []
    
    for i in range(length):
        row = []
        for j in range(20):
            angle = (j / 10) * math.pi  # 0 to 2π
            z_pos = i
            
            # Two intertwined helices
            if j < 10:
                # First strand
                radius = 5
                x = radius * math.cos(angle + z_pos * 0.3 + time)
                y = radius * math.sin(angle + z_pos * 0.3 + time)
            else:
                # Second strand (opposite phase)
                radius = 5
                x = radius * math.cos(angle + z_pos * 0.3 + time + math.pi)
                y = radius * math.sin(angle + z_pos * 0.3 + time + math.pi)
            
            row.append((x + 30, y + 10, z_pos))
        gridCoords.append(row)
    
    return gridCoords


@register_shape("mandelbulb", pygame.K_r, is_animated=False)
def generate_mandelbulb_slice(resolution=50, z_slice=0, max_iterations=10):
    """Generate a 2D slice of a 3D Mandelbulb fractal"""
    gridCoords = []
    
    for x_idx in range(resolution):
        row = []
        for y_idx in range(resolution):
            # Map to Mandelbulb coordinate space
            x = (x_idx / resolution - 0.5) * 3
            y = (y_idx / resolution - 0.5) * 3
            z = z_slice
            
            # Calculate Mandelbulb iterations
            x0, y0, z0 = x, y, z
            iteration = 0
            
            for _ in range(max_iterations):
                r = math.sqrt(x**2 + y**2 + z**2)
                if r > 2:
                    break
                
                theta = math.atan2(math.sqrt(x**2 + y**2), z)
                phi = math.atan2(y, x)
                
                # Power 8 Mandelbulb formula
                r8 = r ** 8
                x = r8 * math.sin(8 * theta) * math.cos(8 * phi) + x0
                y = r8 * math.sin(8 * theta) * math.sin(8 * phi) + y0
                z = r8 * math.cos(8 * theta) + z0
                
                iteration += 1
            
            # Use iteration count as height
            height = iteration * 2
            
            row.append((x_idx, height, y_idx))
        gridCoords.append(row)
    
    return gridCoords


@register_shape("klein", pygame.K_t, is_animated=False)
def generate_klein_bottle(resolution=40):
    """Generate a Klein bottle - a non-orientable surface"""
    gridCoords = []
    
    for u_idx in range(resolution):
        row = []
        for v_idx in range(resolution):
            u = (u_idx / resolution) * 2 * math.pi
            v = (v_idx / resolution) * 2 * math.pi
            
            # Klein bottle parametric equations
            r = 4 * (1 - math.cos(u) / 2)
            
            if u < math.pi:
                x = 6 * math.cos(u) * (1 + math.sin(u)) + r * math.cos(u) * math.cos(v)
                y = 16 * math.sin(u) + r * math.sin(u) * math.cos(v)
            else:
                x = 6 * math.cos(u) * (1 + math.sin(u)) + r * math.cos(v + math.pi)
                y = 16 * math.sin(u)
            
            z = r * math.sin(v)
            
            row.append((x + 30, y + 20, z + 30))
        gridCoords.append(row)
    
    return gridCoords


@register_shape("trefoil", pygame.K_y, is_animated=False)
def generate_trefoil_knot(resolution=50):
    """Generate a trefoil knot - a classic mathematical knot"""
    gridCoords = []
    
    for t_idx in range(resolution):
        row = []
        for r_idx in range(15):
            t = (t_idx / resolution) * 2 * math.pi
            
            # Trefoil knot parametric equations
            x = math.sin(t) + 2 * math.sin(2 * t)
            y = math.cos(t) - 2 * math.cos(2 * t)
            z = -math.sin(3 * t)
            
            # Add thickness
            theta = (r_idx / 15) * 2 * math.pi
            radius = 0.5
            
            # Normal vector calculation (simplified)
            nx = math.cos(t)
            ny = math.sin(t)
            
            x_thick = x + radius * math.cos(theta) * nx
            y_thick = y + radius * math.cos(theta) * ny
            z_thick = z + radius * math.sin(theta)
            
            row.append((x_thick * 5 + 25, y_thick * 5 + 15, z_thick * 5 + 25))
        gridCoords.append(row)
    
    return gridCoords
