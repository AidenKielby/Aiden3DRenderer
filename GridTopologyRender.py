from librosa import ex
import pygame
from pygame import QUIT
import sys
import math
import random

pygame.init()

WIDTH = 1000
HEIGHT = 1000
HALF_W = WIDTH // 2
HALF_H = HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#pygame.event.set_grab(True) 
#pygame.mouse.set_visible(False)

# Terrain generation functions (these are the only things made by AI)
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
            
            # Add connecting rungs periodically
            if i % 5 == 0 and j in [0, 10]:
                # This creates the cross-connections
                pass
            
            row.append((x + 30, y + 10, z_pos))
        gridCoords.append(row)
    
    return gridCoords

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

# Back to made by me

def ddd_to_dd(matrix: list[list[tuple[float]]], fov, cameraPos: tuple[float], cameraFacing: tuple[float]):
    i = []
    m = 50
    for xIdx in range(len(matrix)):
        xList = matrix[xIdx]
        l = []
        for yIdx in range(len(xList)):
            point = xList[yIdx]
            x = point[0]
            y = point[1]
            z = point[2]

            x -= (cameraPos[0])
            y -= (cameraPos[1])
            z -= (cameraPos[2])

            x1 = x * math.cos(cameraFacing[1]) + z * math.sin(cameraFacing[1])
            y1 = y
            z1 = -x * math.sin(cameraFacing[1]) + z * math.cos(cameraFacing[1])

            x2 = x1
            y2 = y1 * math.cos(cameraFacing[0]) - z1 * math.sin(cameraFacing[0])
            z2 = y1 * math.sin(cameraFacing[0]) + z1 * math.cos(cameraFacing[0])

            x3 = x2 * math.cos(cameraFacing[2]) - y2 * math.sin(cameraFacing[2])
            y3 = x2 * math.sin(cameraFacing[2]) + y2 * math.cos(cameraFacing[2])
            z3 = z2

            if z3 <= 0.1:
                l.append(None)
                continue

            f = 1 / math.tan(fov / 2)

            dd_x = (x3 * f) / -z3
            dd_y = (y3 * f) / -z3

            px = dd_x * HALF_W + HALF_W
            py = dd_y * HALF_H + HALF_H

            #print(dd_x, dd_y, cameraPos)
            l.append((px, py))
        i.append(l)

    return i
    

def render(screen, matrix: list[list[tuple[float]]]):
    for xIdx in range(len(matrix)):
        xList = matrix[xIdx]
        for yIdx in range(len(xList)):
            point = xList[yIdx]
            if point is not None:
                points = []
                points.append((point[0], point[1]))


                try:
                    if xIdx < len(matrix) - 1:
                        points.append(matrix[xIdx+1][yIdx])
                    if yIdx < len(xList) - 1:
                        points.append(matrix[xIdx][yIdx+1])
                except(IndexError):
                    continue

                for p in points:
                    if p is not None:
                        pygame.draw.line(screen, (0,0,0), point, p, 2)


def generateShape(terrain_type):
    if terrain_type == "mountain":
        gridCoords = generate_mountain(20)
        needsRegen = False
    elif terrain_type == "waves":
        gridCoords = generate_waves(30, animation_time)
        needsRegen = True
    elif terrain_type == "ripple":
        gridCoords = generate_ripple(25, animation_time)
        needsRegen = True
    elif terrain_type == "canyon":
        gridCoords = generate_canyon(30)
        needsRegen = False
    elif terrain_type == "pyramid":
        gridCoords = generate_pyramid(15)
        needsRegen = False
    elif terrain_type == "spiral":
        gridCoords = generate_spiral(25, animation_time)
        needsRegen = True
    elif terrain_type == "torus":
        gridCoords = generate_torus(30)
        needsRegen = False
    elif terrain_type == "sphere":
        gridCoords = generate_sphere(20)
        needsRegen = False
    elif terrain_type == "mobius":
        gridCoords = generate_mobius_strip(30)
        needsRegen = False
    elif terrain_type == "megacity":
        gridCoords = generate_megacity(80)
        needsRegen = False
    elif terrain_type == "alien":
        gridCoords = generate_alien_landscape(60, animation_time)
        needsRegen = True
    elif terrain_type == "helix":
        gridCoords = generate_double_helix(60, animation_time)
        needsRegen = True
    elif terrain_type == "mandelbulb":
        gridCoords = generate_mandelbulb_slice(50, 0, 10)
        needsRegen = False
    elif terrain_type == "klein":
        gridCoords = generate_klein_bottle(40)
        needsRegen = False
    elif terrain_type == "trefoil":
        gridCoords = generate_trefoil_knot(50)
        needsRegen = False
    
    return gridCoords, needsRegen

cameraPos = [40, 10, 40]
cameraRot = [0, 0, 0] #[0] = pitch, [1] = yaw, [2] = roll
speed = 0.1
baseSpeed = 0.1
speedMult = 2
last_facing = cameraRot[:]

needsRegen = False
terrain_type = "megacity"  
animation_time = 0
pos1 = (HALF_W,HALF_H)
holdingMouse = False

wasGenerated = False
lastTerrainType = None

clock = pygame.time.Clock()
clock.tick(60)

while True:
    screen.fill((255, 255, 255))

    animation_time += 0.01
    if terrain_type != lastTerrainType or needsRegen:
        gridCoords, needsRegen = generateShape(terrain_type)
        lastTerrainType = terrain_type
    
    # Generate terrain based on type
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                pos1 = event.pos
                last_facing = cameraRot[:]
                holdingMouse = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                holdingMouse = False
    keys = pygame.key.get_pressed()

    if holdingMouse:
        mp = pygame.mouse.get_pos()
        x_dif = mp[0]-pos1[0]
        y_dif = mp[1]-pos1[1]
        cameraRot[0] = last_facing[0] + y_dif*0.002
        cameraRot[1] = last_facing[1] + x_dif*0.002

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    forward_x = math.sin(cameraRot[1])
    forward_z = -math.cos(cameraRot[1])
    right_x = math.cos(cameraRot[1])
    right_z = math.sin(cameraRot[1])

    if keys[pygame.K_w]:
        cameraPos[0] -= forward_x * speed
        cameraPos[2] -= forward_z * speed
    if keys[pygame.K_s]:
        cameraPos[0] += forward_x * speed
        cameraPos[2] += forward_z * speed
    if keys[pygame.K_a]:
        cameraPos[0] += right_x * speed
        cameraPos[2] += right_z * speed
    if keys[pygame.K_d]:
        cameraPos[0] -= right_x * speed
        cameraPos[2] -= right_z * speed

    if keys[pygame.K_SPACE]:
        cameraPos[1] += speed
    if keys[pygame.K_LSHIFT]:
        cameraPos[1] -= speed

    if keys[pygame.K_DOWN]:
        cameraRot[0] = cameraRot[0] - 0.001  # Pitch up
    if keys[pygame.K_UP]:
        cameraRot[0] = cameraRot[0] + 0.001  # Pitch down
    if keys[pygame.K_RIGHT]:
        cameraRot[1] = cameraRot[1] + 0.001  # Yaw left
    if keys[pygame.K_LEFT]:
        cameraRot[1] = cameraRot[1] - 0.001  # Yaw right

    if keys[pygame.K_1]:
        terrain_type = "mountain"
    if keys[pygame.K_2]:
        terrain_type = "waves"
    if keys[pygame.K_3]:
        terrain_type = "ripple"
    if keys[pygame.K_4]:
        terrain_type = "canyon"
    if keys[pygame.K_5]:
        terrain_type = "pyramid"
    if keys[pygame.K_6]:
        terrain_type = "spiral"
    if keys[pygame.K_7]:
        terrain_type = "torus"
    if keys[pygame.K_8]:
        terrain_type = "sphere"
    if keys[pygame.K_9]:
        terrain_type = "mobius"
    if keys[pygame.K_0]:
        terrain_type = "megacity"
    if keys[pygame.K_q]:
        terrain_type = "alien"
    if keys[pygame.K_e]:
        terrain_type = "helix"
    if keys[pygame.K_r]:
        terrain_type = "mandelbulb"
    if keys[pygame.K_t]:
        terrain_type = "klein"
    if keys[pygame.K_y]:
        terrain_type = "trefoil"
    
    if keys[pygame.K_LCTRL]:
        speed = baseSpeed * speedMult
    else:
        speed = baseSpeed
    
    #print(cameraPos)
    m = ddd_to_dd(gridCoords, math.radians(100), (cameraPos[0], cameraPos[1], cameraPos[2]), (cameraRot[0], cameraRot[1], cameraRot[2]))
    render(screen, m)

    pygame.display.update()
    clock.tick(60)