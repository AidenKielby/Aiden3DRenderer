from aiden3drenderer import Renderer3D, register_shape
import pygame
import math

@register_shape("Tree S", key=pygame.K_i, is_animated=False, color=(100, 200, 100))
def generate_tree_sphere(grid_size=40, trunk_height=20):
    """Generate the sphere (leaves) part of the tree."""
    sphere_radius = grid_size * 0.3
    sphere_center_y = trunk_height + sphere_radius
    n_lat = grid_size // 2
    n_lon = grid_size
    sphere_matrix = []
    for i in range(n_lat):
        lat = math.pi * i / (n_lat - 1)
        y = sphere_center_y + sphere_radius * math.cos(lat)
        row = []
        for j in range(n_lon):
            lon = 2 * math.pi * j / n_lon
            x = grid_size / 2 + sphere_radius * math.sin(lat) * math.cos(lon)
            z = grid_size / 2 + sphere_radius * math.sin(lat) * math.sin(lon)
            row.append((x, y, z))
        # Add extra point to wrap around
        row.append(row[0])
        sphere_matrix.append(row)
    return sphere_matrix

@register_shape("Tree c", key=pygame.K_i, is_animated=False, color=(210, 180, 140))
def generate_tree_cylinder(grid_size=40):
    """Generate the cylinder (trunk) part of the tree."""
    trunk_height = grid_size * 0.5
    trunk_radius = grid_size * 0.08
    n_trunk = grid_size // 2
    n_lon = grid_size
    trunk_matrix = []
    for i in range(n_trunk):
        y = trunk_height * i / (n_trunk - 3)
        row = []
        for j in range(n_lon):
            theta = 2 * math.pi * j / n_lon
            x = grid_size / 2 + trunk_radius * math.cos(theta)
            z = grid_size / 2 + trunk_radius * math.sin(theta)
            row.append((x, y, z))
        # Add extra point to wrap around
        row.append(row[0])
        trunk_matrix.append(row)
    return trunk_matrix

"""@register_shape("Tree (Sphere+Cylinder)", key=pygame.K_i, is_animated=False, color=(100, 100, 100))
def generate_tree(grid_size=40, frame=0):
    trunk_matrix = generate_tree_cylinder(grid_size)
    trunk_height = grid_size * 0.5
    sphere_matrix = generate_tree_sphere(grid_size, trunk_height)
    return trunk_matrix + sphere_matrix"""

# Run the renderer (your shape will be available on 'T' key)

if __name__ == "__main__":
    renderer = Renderer3D()
    font = None
    try:
        pygame.font.init()
        font = pygame.font.SysFont(None, 32)
    except Exception:
        pass

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            renderer.camera.handle_mouse_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    renderer.is_mesh = not renderer.is_mesh

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        renderer.loopable_run()

        # Draw toggle instructions
        if font:
            text = font.render(f"Press M to toggle mesh mode (Currently: {'Mesh' if renderer.is_mesh else 'Wireframe'})", True, (0,0,0))
            renderer.screen.blit(text, (20, 20))
        pygame.display.update()
    pygame.quit()
