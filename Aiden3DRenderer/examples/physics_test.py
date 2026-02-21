"""
Basic usage example for Aiden3DRenderer

This demonstrates the simplest way to use the renderer.
"""
from aiden3drenderer import Renderer3D, physics


def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")

    obj_handler = physics.PhysicsObjectHandler()

    plane_color = (200, 200, 200)
    plane_size = 28  # Slightly larger box
    grid_size = 8    # Slightly higher resolution
    obj_handler.add_plane(renderer, [0, -14, 0], (0, 0, 0),   plane_color, plane_size, grid_size)  # floor
    obj_handler.add_plane(renderer, [-14, 0, 0], (0, 0, 90),  plane_color, plane_size, grid_size)  # left
    obj_handler.add_plane(renderer, [14, 0, 0],  (0, 0, 90),  plane_color, plane_size, grid_size)  # right
    obj_handler.add_plane(renderer, [0, 0, -14], (90, 0, 0),  plane_color, plane_size, grid_size)  # back
    obj_handler.add_plane(renderer, [0, 0, 14],  (90, 0, 0),  plane_color, plane_size, grid_size)  # front

    # Create two balls (spheres) inside the box
    ball_color = (100, 100, 255)
    ball_radius = 4   # Slightly larger balls
    ball_mass = 2.5
    ball_grid = 8     # Slightly higher resolution

    ball1 = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), ball_color, ball_radius, ball_mass, ball_grid)
    ball1.anchor_position = [0, 0, 0]
    
    ball2 = physics.ShapePhysicsObject(renderer, "sphere", (0, 0, 0), ball_color, ball_radius, ball_mass, ball_grid)
    ball2.anchor_position = [9, 0, 0]

    # Gravity force (downwards)
    gravity = (0, -0.18, 0)
    ball1.add_forces((1,0,1))

    camera = physics.CameraPhysicsObject(renderer, renderer.camera, 1, 10)

    obj_handler.add_camera(camera)

    # Add balls
    obj_handler.add_shape(ball1)
    obj_handler.add_shape(ball2)

    renderer.set_starting_shape(None)
    renderer.is_mesh = False
    renderer.camera.base_speed = 1.2

    while True:
        
        ball1.add_forces(gravity)
        ball2.add_forces(gravity)
        camera.add_forces(gravity*100)
        obj_handler.handle_shapes()
        renderer.loopable_run()


if __name__ == "__main__":
    main()
