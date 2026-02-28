
from aiden3drenderer import Renderer3D, obj_loader
import pygame
import math

def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = None

    renderer.camera.position = [0, 1, -2]
    renderer.is_mesh = True
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/trident.obj")
    #print(obj)

    renderer.vertices_faces_list.append(obj)
    # Run the renderer

    renderer.run()


if __name__ == "__main__":
    main()
