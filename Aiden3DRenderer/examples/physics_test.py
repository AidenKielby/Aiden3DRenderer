"""
Basic usage example for Aiden3DRenderer

This demonstrates the simplest way to use the renderer.
"""
from aiden3drenderer import Renderer3D, register_shape, physics
import pygame
import math


def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")

    shape = physics.ShapePhysicsObject(renderer, "sphere", (0,0,0), (100, 0, 0), 5, 20, 20)
    shape.add_forces((-0.7, 0, 0))
    shape.anchor_position = [20, 0, 0]

    shape1 = physics.ShapePhysicsObject(renderer, "sphere", (0,0,0), (50, 0, 0), 5, 10, 20)
    shape1.add_forces((0.7, 0, 0))
    shape1.anchor_position = [0, 0, 0]

    shape2 = physics.ShapePhysicsObject(renderer, "plane", (0,0,270), (0, 100, 0), 20, 20, 20)
    shape2.anchor_position = [40, 0, 0]

    shape3 = physics.ShapePhysicsObject(renderer, "plane", (0,0,270), (0, 50, 0), 10, 10, 20)
    shape3.anchor_position = [-10, 0, 0]

    obj_handler = physics.PhysicsObjectHandler()

    obj_handler.add_shape(shape)
    obj_handler.add_shape(shape1)
    obj_handler.add_shape(shape2)
    obj_handler.add_shape(shape3)

    # Set starting shape (optional)
    renderer.set_starting_shape(None)

    renderer.camera.position = [0, 0 ,0]
    renderer.is_mesh = False
    # Run the renderer

    while True:
        obj_handler.handle_shapes()
        renderer.loopable_run()


if __name__ == "__main__":
    main()
