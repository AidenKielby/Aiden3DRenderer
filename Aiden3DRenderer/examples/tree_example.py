from aiden3drenderer import Renderer3D, register_shape
import pygame
import math

@register_shape("Tree (Sphere+Cylinder)", key=pygame.K_i, is_animated=False, color=(100, 100, 100))
def generate_tree(grid_size=40, frame=0):
    """Generate a tree: sphere (leaves) on top of a cylinder (trunk)."""
    # Parameters
    sphere_radius = grid_size * 0.3
    trunk_height = grid_size * 0.5
    trunk_radius = grid_size * 0.08
    sphere_center_y = trunk_height + sphere_radius
    n_lat = grid_size // 2  # latitude divisions for sphere
    n_lon = grid_size       # longitude divisions for sphere/cylinder
    n_trunk = grid_size // 2  # vertical divisions for trunk

    # --- Sphere (leaves) ---
    sphere_matrix = []
    for i in range(n_lat):
        lat = math.pi * i / (n_lat - 1)  # 0 to pi
        y = sphere_center_y + sphere_radius * math.cos(lat)
        row = []
        for j in range(n_lon):
            lon = 2 * math.pi * j / n_lon  # 0 to 2pi
            x = grid_size / 2 + sphere_radius * math.sin(lat) * math.cos(lon)
            z = grid_size / 2 + sphere_radius * math.sin(lat) * math.sin(lon)
            row.append((x, y, z))
        sphere_matrix.append(row)

    # --- Cylinder (trunk) ---
    trunk_matrix = []
    for i in range(n_trunk):
        y = trunk_height * i / (n_trunk - 1)
        row = []
        for j in range(n_lon):
            theta = 2 * math.pi * j / n_lon
            x = grid_size / 2 + trunk_radius * math.cos(theta)
            z = grid_size / 2 + trunk_radius * math.sin(theta)
            row.append((x, y, z))
        trunk_matrix.append(row)

    # Stack trunk below sphere
    full_matrix = trunk_matrix + sphere_matrix
    return full_matrix

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
